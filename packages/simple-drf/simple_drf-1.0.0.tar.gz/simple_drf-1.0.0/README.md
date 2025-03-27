# Simple Django Rest Framework

A Python package for quicker API development in Django.

## Table of Contents

- [Description](#description)
- [Installation](#installation)
- [Usage](#usage)
- [Contact](#contact)
- [License](#license)

## Description

Simple-DRF is a Python package that facilitates the process of creating a CRUD API in Django with the Django Rest Framework. I do not recommend using this package for complicated API development, only for setting up a simple API (e.g. CRUD).

## Installation

In order to install Simple-DRF, run the following command in your terminal:

```bash
pip install simple-drf
```

## Usage

Simple-DRF provides two ways to set up an API: functions & classes.

### API Functions

Using API functions is recommended when individual CRUD operations are needed.

You can import API functions from Simple-DRF as follows:

```python
from simple_drf.api_functions import *
```

Simple-DRF provides functions for each of the CRUD operations: `get_all()`, `post()`, `get_one()`, `put()`, & `delete()`.

In order to utilize these functions, define them inside of an class inheriting DRF's `APIView` class:

```python
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from simple_drf.api_functions import get_all()


class ListAPIView(APIView):
	def get(self, request):
		return get_all(Post, PostSerializer)
```

If you want to create a full CRUD API you can use all the API functions:

```python
from rest_framework.views import APIView
from .models import Post
from .serializers import PostSerializer
from simple_drf.api_functions import get_all(), post(), get_one(), put(), delete()


class ListAPIView(APIView):
	def get(self, request):
		return get_all(Post, PostSerializer)

	def post(self, request):
		return post(PostSerializer, request)


class DetailAPIView(APIView):
	def get(self, request, pk):
		return get_one(Post, PostSerializer, pk)

	def put(self, request, pk):
		return put(Post, PostSerializer, request, pk)

	def delete(self, request, pk):
		return delete(Post, pk)
```

Just like that we have created a full CRUD API.

### API Classes

Using API classes is recommended when all CRUD operations are needed.

You can import API classes from Simple-DRF as follows:

```python
from simple_drf.api_classes import ListAPIView, DetailAPIView, FullAPIView
```

Simple-DRF provides a class `ListAPIView` for operations that do not require a primary key parameter (e.g. get all, post) and a class `DetailAPIView` for operations that require a primary key parameter (e.g. get one, put, delete). Simple-DRF also provides a class `FullAPIView` that implements all CRUD operations in one class.

#### ListAPIView

The `ListAPIView` class is used for implementing CRUD operations that do not require a primary key parameter (e.g. get all, post).

You can implement `ListAPIView` in your code as follows:

```python
from .models import Post
from .serializers import PostSerializer
from simple_drf.api_classes import ListAPIView


class PostListAPIView(ListAPIView):
    model = Post
    model_serializer = PostSerializer
```

All you need to do is specify a `model` and `model_serializer` and `ListAPIView` will create operations get all and post for you.

You must then add your class to `urls.py`:

```python
from django.urls import path
from .views import PostListAPIView

urlpatterns = [
    path('', PostListAPIView.as_view(), name='post-list'),
]
```

#### DetailAPIView

The `DetailAPIView` class is used for implementing CRUD operations that require a primary key parameter (e.g. get one, put, delete).

You can implement `DetailAPIView` in your code as follows:

```python
from .models import Post
from .serializers import PostSerializer
from simple_drf.api_classes import DetailAPIView


class PostDetailAPIView(DetailAPIView):
    model = Post
    model_serializer = PostSerializer
```

All you need to do is specify a `model` and `model_serializer` and `DetailAPIView` will create operations get one, put, and delete for you.

You must then add your class to `urls.py`:

```python
from django.urls import path
from .views import PostDetailAPIView

urlpatterns = [
    path('<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
]
```

#### ListAPIView & DetailAPIView

You can implement all CRUD operations by combining ListAPIView and DetailAPIView:

```python
from .models import Post
from .serializers import PostSerializer
from simple_drf.api_classes import ListAPIView, DetailAPIView


class PostListAPIView(ListAPIView):
    model = Post
    model_serializer = PostSerializer


class PostDetailAPIView(DetailAPIView):
    model = Post
    model_serializer = PostSerializer
```

Then your `urls.py` will look like this:

```python
from django.urls import path
from .views import PostListAPIView, PostDetailAPIView

urlpatterns = [
    path('', PostListAPIView.as_view(), name='post-list'),
    path('<int:pk>/', PostDetailAPIView.as_view(), name='post-detail'),
]
```

#### FullAPIView

If you want to implement all CRUD operations in one class, then use `FullAPIView`.

```python
from .models import Post
from .serializers import PostSerializer
from simple_drf.api_classes import FullAPIView

class PostFullAPIView(FullAPIView):
    model = Post
    model_serializer = PostSerializer
```

Your `urls.py` file will then look like this:

```python
from django.urls import path
from .views import PostFullAPIView

urlpatterns = [
    path('', PostFullAPIView.as_view(), name='post-full-list'),
    path('<int:pk>/', PostFullAPIView.as_view(), name='post-full-detail'),
]
```

## Contact

This package is still in development. If you notice any bugs or have any ideas for new functionality, feel free to contact me via `samuelchichester05@gmail.com`.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
