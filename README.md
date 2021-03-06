
# Crocus

A small and experimental async web microframework built on top of aiohttp (required python 3.5+).

## Documentation

http://crocus.readthedocs.org/

## Examples

Check the examples folder for a full application sample.

### Basic

```python

from crocus import Crocus

app = Crocus()

async def response_middleware(req, res):
  res.header('content-type', 'application/json')


async def request_middleware(req, res):
  req.some_value = 'custom value'


async def search_products(req, res):
  data = {
    'total': 1,
    'data': [
      'name': 'redbull',
      'qty': 10
    ]
  }
  res.write(json.dumps(data))
  res.end()


app.use(response_middleware, request_middleware)
app.get('/products', search_products)


if __name__ == '__main__':
  app.run(host='127.0.0.1', port=5000)
```

# License

Crocus is licensed under the MIT open source license.