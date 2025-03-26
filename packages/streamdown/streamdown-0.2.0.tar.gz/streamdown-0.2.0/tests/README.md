#### server.py

For every model API endpoint you want to use, you must implement an `EndpointHandler`. This class handles incoming
requests, processes them, sends them to the model API server, and finally returns an HTTP response.
`EndpointHandler` has several abstract functions that must be implemented. Here, we implement two, one
for `/generate`, and one for `/generate_stream`:

```python

"""
AuthData is a dataclass that represents Authentication data sent from Autoscaler to client requesting a route.
When a user requests a route from autoscaler, see Vast's Serverless documentation for how routing and AuthData
work.
When a user receives a route for this PyWorker, they'll call PyWorkers API with the following JSON:
{
    auth_data: AuthData,
    payload : InputData # defined above
}
"""
from aiohttp import web

from lib.data_types import EndpointHandler, JsonDataException
from lib.server import start_server
from .data_types import InputData

# This class is the implementer for the '/generate' endpoint of model API
@dataclasses.dataclass
class GenerateHandler(EndpointHandler[InputData]):

    @property
    def endpoint(self) -> str:
        # the API endpoint
        return "/generate"

    @classmethod
    def payload_cls(cls) -> Type[InputData]:
        """this function should just return ApiPayload subclass used by this handler"""
        return InputData

    def generate_payload_json(self, payload: InputData) -> Dict[str, Any]:
        """
        defines how to convert `InputData` defined above, to
        JSON data to be sent to the model API. This function too is a simple dataclass -> JSON, but
        can be more complicated, See comfyui for an example
        """
        return dataclasses.asdict(payload)

    def make_benchmark_payload(self) -> InputData:
        """
        defines how to generate an InputData for benchmarking. This needs to be defined in only
        one EndpointHandler, the one passed to the backend as the benchmark handler. Here we use the .for_test()
        method on InputData. However, in some cases you might need to fine tune your InputData used for
        benchmarking to closely resemble the average request users call the endpoint with in order to get best
        autoscaling performance
        """
        return InputData.for_test()

    async def generate_client_response(
        self, client_request: web.Request, model_response: ClientResponse
    ) -> Union[web.Response, web.StreamResponse]:
        """
        defines how to convert a model API response to a response to PyWorker client
        """
        _ = client_request
        match model_response.status:
            case 200:
                log.debug("SUCCESS")
                data = await model_response.json()
                return web.json_response(data=data)
            case code:
                log.debug("SENDING RESPONSE: ERROR: unknown code")
                return web.Response(status=code)


```

We also handle `GenerateStreamHandler` for streaming responses. It is identical to `GenerateHandler`, except for
the endpoint name and how we create a web response, as it is a streaming response:

```python
class GenerateStreamHandler(EndpointHandler[InputData]):
    @property
    def endpoint(self) -> str:
        return "/generate_stream"

    @classmethod
    def payload_cls(cls) -> Type[InputData]:
        return InputData

    def generate_payload_json(self, payload: InputData) -> Dict[str, Any]:
        return dataclasses.asdict(payload)

    def make_benchmark_payload(self) -> InputData:
        return InputData.for_test()

    async def generate_client_response(
        self, client_request: web.Request, model_response: ClientResponse
    ) -> Union[web.Response, web.StreamResponse]:
        match model_response.status:
            case 200:
                log.debug("Streaming response...")
                res = web.StreamResponse()
                res.content_type = "text/event-stream"
                await res.prepare(client_request)
                async for chunk in model_response.content:
                    await res.write(chunk)
                await res.write_eof()
                log.debug("Done streaming response")
                return res
            case code:
                log.debug("SENDING RESPONSE: ERROR: unknown code")
                return web.Response(status=code)


```

You can now instantiate a Backend and use it to handle requests.

```python
from lib.backend import Backend, LogAction

# the url and port of model API
MODEL_SERVER_URL = "http://0.0.0.0:5001"


# This is the log line that is emitted once the server has started
MODEL_SERVER_START_LOG_MSG = "server has started"
MODEL_SERVER_ERROR_LOG_MSGS = [
    "Exception: corrupted model file"  # message in the logs indicating the unrecoverable error
]

backend = Backend(
    model_server_url=MODEL_SERVER_URL,
    # location of model log file
    model_log_file=os.environ["MODEL_LOG"],
    # for some model backends that can only handle one request at a time, be sure to set this to False to
    # let PyWorker handling queueing requests.
    allow_parallel_requests=True,
    # give the backend an EndpointHandler instance that is used for benchmarking
    # number of benchmark run and number of words for a random benchmark run are given
    benchmark_handler=GenerateHandler(benchmark_runs=3, benchmark_words=256),
    # defines how to handle specific log messages. See docstring of LogAction for details
    log_actions=[
        (LogAction.ModelLoaded, MODEL_SERVER_START_LOG_MSG),
        (LogAction.Info, '"message":"Download'),
        *[
            (LogAction.ModelError, error_msg)
            for error_msg in MODEL_SERVER_ERROR_LOG_MSGS
        ],
    ],
)

# this is a simple ping handler for PyWorker
async def handle_ping(_: web.Request):
    return web.Response(body="pong")

# this is a handler for forwarding a health check to model API
async def handle_healthcheck(_: web.Request):
    healthcheck_res = await backend.session.get("/healthcheck")
    return web.Response(body=healthcheck_res.content, status=healthcheck_res.status)

routes = [
    web.post("/generate", backend.create_handler(GenerateHandler())),
    web.post("/generate_stream", backend.create_handler(GenerateStreamHandler())),
    web.get("/ping", handle_ping),
    web.get("/healthcheck", handle_healthcheck),
]

if __name__ == "__main__":
    # start server, called from start_server.sh
    start_server(backend, routes)
```
