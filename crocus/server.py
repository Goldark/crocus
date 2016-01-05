import aiohttp.server
from crocus.request import Request
from crocus.response import Response
from crocus.helpers import RouteDict, DynamicObject


class Server(aiohttp.server.ServerHttpProtocol):
  def __init__(self, *args, **kwargs):
    super(Server, self).__init__(*args, **kwargs)
    self.handlers = kwargs.get('handlers', RouteDict())
    self.middlewares = kwargs.get('middlewares', [])
    self.config = kwargs.get('config', DynamicObject())
  
  async def handle_request(self, message, payload):
    encoding = self.config.default_encoding
    req_input = {
      'method': message.method,
      'path': message.path,
      'headers': message.headers,
      'encoding': self.config.default_encoding,
      'app': self.config
    }
    body = await payload.read()
    if body:
      req_input['body'] = body
    request = Request(**req_input)
    await request.prepare()
    handler_key = '%s:%s' % (request.method.lower(), request.path)
    (handler, params) = self.handlers.get(handler_key)
    response = Response(
      self.writer, 200, http_version=message.version
    )
    response.encoding = encoding
    response.header('Content-Type', 'text/plain')
    if handler is None:
      response.status = 404
      not_found_params = (request.method.encode(encoding), request.path.encode(encoding))
      response.write('%s %s NOT FOUND' % not_found_params)
      return await response.end()
    request.params = DynamicObject.from_dict(params)
    for item in self.middlewares:
      middleware = await item(request, response)
      if middleware == Response.FINISH_CODE:
        return middleware
    return await handler(request, response)
