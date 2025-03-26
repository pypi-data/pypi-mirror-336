# OBOFramework: Python Web Framework built for learning purpose

![purpose](https://img.shields.io/badge/:purpose-learning-green.svg)
![PyPI - Version](https://img.shields.io/pypi/v/oboframework)


OBOFramework: Python Web Framework built for learning purpose
It's a WSGI framework and can be used with any WSGI application server such as Gunicorn

## Installation

```shell
pip install oboframework
```

## How to use oboframework

### Basic usage

```python
from oboframework import OBOFramework

app = OBOFramework()
@app.route('/home', allowed_methods=['get'])
def home(request, response):
    response.text = "Hello from the HOME page"


@app.route('/hello/{name}')
def hello(request, response, name):
    response.text = f"Hello, {name}!"


@app.route("/books")
class Books:
    def get(self, request, response):
        response.text = "Books Page"

    def post(self, request, response):
        response.text = "Endpoint to create a book"


def new_handler(request, response):
    response.text = "New handler"

app.add_route("/new-handler", new_handler)


@app.route("/template")
def template_handler(request, response):
    response.html = app.template(
        "index.html", 
        context={"title": "Awesome Framework", "name": "OBOFramework"}
        )
```

## Unit Tests

The recommended way to writing unit tests is with [pytest](https://docs.pytest.org/en/latest/). 
There are two built in fixtures that you may want to use when unit tests with OBOFramework.
The first one is `app` which is an instance of the main `API` class:

```python


def test_route_overlap_throws_exception(app):
    @app.route('/')
    def home(request, response):
        response.text = "Hello Home Page"

    with pytest.raises(AssertionError):
        @app.route('/')
        def home2(request, response):
            response.text = "Hello Home Page"
```
The other one is `client` that you can use to send HTTP requests to your handlers.
It is based on the famous [request](https://requests.readthedocs.io/) and it should feel very familiar:

```python

def test_parameterized_route(app, client):
    @app.route("/{name}")
    def hello(request, response, name):
        response.text = f"Hello {name}"

    assert client.get("http://testserver/otajon").text == "Hello otajon"
```

## Templates

The default template for templates is `templates`. You can change it when initializing your the main `API()` class:

```python
app = API(templates_dir="templates_dir_name")
```

Then you can use HTML files in that folder like so in a handler:

```python
@app.route("/showe/templates")
def handler_with_templates(request, response):
    response.text = app.template(
        "example.html", content={"title": "Awesome Framework", "body": "Welcome to the awesome framework"}
    )
```

## Static Files

Just like templates, the default folder for static files is `static` and you can override it:

```python
app = API(static_dir="static_dir_name")
```

Then you can use the files inside this folder in HTML files:

```html
<!DOCTYPE html>
<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{ title }}</title>

        <link href="/static/main.css" rel="stylesheet" type="text/css">
    </head>

    <body>
        <h1>{{ body }}</h1>
        <p>This is a paragraph</p>
    </body>
    </html>
```

## Middleware

You can create custom middlewares classes by inheriting from the `middleware.Middleware` classes and overriding its two methods that are called before and after each request:

```python
from middleware import Middleware

app = API()

class SimpleCustomMiddleware(Middleware):
    def process_request(self, request):
        print("Request received", request.url)
    
    def process_response(self, request, response):
        print("Response received", response.url)


app.add_middleware(SimpleCustomMiddleware)
```