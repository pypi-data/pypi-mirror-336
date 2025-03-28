# inventory-grpc-client-python-kessel

This package is generated grpc python client from inventory-api proto files.

## Installation

This library is not yet available on pypi, but once it is, you can install it with the following command:
```shell
$ python -m pip install inventory-grpc-clients-python-kessel-project
```

## Publishing to [PyPI](https://pypi.org/project/inventory-grpc-clients-python-kessel-project/)

### 1. Clone this repo
Run following commands in the root directory.

### 2. Generate a new Python gRPC client

```
 ./generate_python_grpc_client.sh
```
### 3. Push the new version of the package to PyPI

```
 ./generate_python_grpc_client.sh <new_version>
```
example:
```
 ./generate_python_grpc_client.sh 0.8.10
```

NOTE: When `./generate_python_grpc_client.sh` is executed without an argument, the current version is displayed.

### 4. Create PR with new version of python grpc client
The version is included in the commit.
