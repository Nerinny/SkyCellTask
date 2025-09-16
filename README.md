# API tests for creating device endpoint
API tests done with Python, Pytest and Requests. Includes Dockerfile and GH actions pipeline with HTML report.

## Running solution locally
- Clone repository locally
- Run Docker daemon or desktop
- Build docker image:
```docker build . --file Dockerfile --tag api-test:latest```
- Run docker 
```docker run --rm -e API_URL='<API_base_url_here>' api-test:latest```

## Structure of the solution
- **.github/workflows/docker-image.yml** - GH workflow configuration
- **helpers/request_helper.py** - helper methods for requests
- **helpers/messages.py** - API response messages strings
- **tests/test_create_device_endpoint.py** - tests for creating device endpoint
- **Dockerfile** - commands to create docker container
- **pytest.ini** - configuration of pytest
- **requirements.txt** - required libraries

## Found issues
- Endpoint for getting device by ID doesn't return proper results
- User can add devices with the same IDs and model names multiple times
- Because of the issue above delete is not controlling which duplicate of device will be removed
- Invalid model names are accepted and data is inserted - long name, empty name, JS code, int
- When user adds device with model name in UI - model name is trimmed to first space
- Filter in UI doesn't work

## Workarounds
- Since getting device by ID doesn't return proper result - getting device by model name is used instead
- Some tests are failing because of found issues - additional cleanup after all tests is used that removes all test devices

## Improvements
#### Given limited time there are some improvements that could be implemented:
- One assert per test case
- Soft assertions if more asserts are used for more full result of what is failing
- Custom assert messages
- Faker for test data
- Method docstrings
- Setup with test data and checks if setup devices persist after inserting new devices
- Setup with no test data and check if tests run properly on empty environment