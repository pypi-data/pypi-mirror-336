# EnvModel

A Python library for simplifying the use of environment variables in your projects.

## Overview
EnvModel provides a simple and intuitive way to define, manage, and access environment variables in your Python 
projects. It supports a variety of field types, including strings, integers, floats, booleans, JSON, and string lists.

## Installation

To install EnvModel, run the following command:

```bash
pip install envmodel
```

## Usage

Here's a minimal example of how to use EnvModel:

```python
from envmodel import EnvModel, StringField

class MyConfig(EnvModel):
    api_key = StringField(name="API_KEY", required=True)
    database_url = StringField(name="DATABASE_URL", default="sqlite:///example.db")

config = MyConfig()
print(config.api_key)  # prints the value of API_KEY environment variable
print(config.database_url)  # prints the value of DATABASE_URL environment variable or the default value
```

## Field Types

EnvModel supports the following field types:

* `StringField`: A string field that can hold any string value.
* `IntegerField`: An integer field that can hold any integer value.
* `FloatField`: A float field that can hold any float value.
* `BooleanField`: A boolean field that can hold a boolean value.
* `JsonField`: A JSON field that can hold any JSON value.
* `StringListField`: A string list field that can hold a list of string values.

See the [Field Types documentation](https://envmodel.readthedocs.io/en/latest/fields.html) for more details.

## Contributing

We welcome contributions to EnvModel! Please check out the [Contributing documentation](https://envmodel.readthedocs.io/en/latest/CONTRIBUTING.html) for more information.

## License

EnvModel is released under the [Apache License 2.0](LICENSE).

## Changelog

See the [CHANGELOG](CHANGELOG.md) for a list of changes.
