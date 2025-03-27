# core-tests
_______________________________________________________________________________

This project contains basic elements for testing purposes and the ability 
to run (via console commands) tests and code coverage (unittest-based). This way, we can 
stick to the `DRY -- Don't Repeat Yourself` principle and avoid code duplication
in each python project where tests coverage and tests execution are
expected...

## How to Use

### Install the package
```shell
pip install core-tests
```

### Create entry-point
```python
# manager.py

from click.core import CommandCollection
from core_tests.tests.runner import cli_tests

if __name__ == "__main__":
    cli = CommandCollection(sources=[cli_tests()])
    cli()
```

### Shell commands
```shell
python manager.py run-tests --test-type unit
python manager.py run-tests --test-type integration
python manager.py run-tests --test-type "another folder that contains test cases under ./tests"
python manager.py run-tests --test-type functional --pattern "*.py"
python manager.py run-coverage
```

## Execution Environment

### Install libraries
```shell
pip install --upgrade pip 
pip install virtualenv
```

### Create the Python Virtual Environment
```shell
virtualenv --python={{python-version}} .venv
virtualenv --python=python3.11 .venv
```

### Activate the Virtual Environment
```shell
source .venv/bin/activate
```

### Install required libraries
```shell
pip install .
```

### Check tests and coverage...
```shell
python manager.py run-tests
python manager.py run-coverage
```
