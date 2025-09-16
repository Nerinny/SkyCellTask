import pytest
from helpers.messages import EUI_MODEL_NAME_REQUIRED, EUI_CHARACTERS

from helpers.requests_helper import create_device, get_device_by_model, remove_device, create_device_custom_payload

@pytest.mark.parametrize("eui, model_name", [
    ("0011223344556677", "Test Device Sensor"),
    ("aabbccddeeff1122", "Test Device Thermostat"),
    ("AaBbCcDdEeFf1122", "Test Device Lock"),
    ("0011223344556677", "Test Device Lock v2.0.1")
])
def test_create_valid_device(eui, model_name):
    response = create_device(eui = eui, model_name= model_name)
    assert response.status_code == 201

    get_response = get_device_by_model(model_name=model_name)
    assert get_response.status_code == 200
    data = get_response.json()
    assert data[0]["eui"] == eui
    assert data[0]["modelName"] == model_name

    delete_response = remove_device(eui=eui)
    assert delete_response.status_code == 204


@pytest.mark.parametrize("eui, message", [
    (None, EUI_MODEL_NAME_REQUIRED),
    ("", EUI_MODEL_NAME_REQUIRED),
    ("0011", EUI_CHARACTERS),
    ("00112233445566778", EUI_CHARACTERS),
    ("00112233ABC556677", EUI_CHARACTERS),
    ("0011 223344556677", EUI_CHARACTERS),
    (1122334455667788, EUI_CHARACTERS)
])
def test_create_device_invalid_eui(eui, message):
    response = create_device(eui=eui, model_name="Test Device")
    assert response.status_code == 400

    response_json = response.json()
    assert response_json["error"] == message


@pytest.mark.parametrize("model_name", [
    None,
    "",
    " ",
    pytest.param("Test" * 10000, id="Very long value"),
    "<script>alert('Test')</script>"
])
def test_create_device_invalid_model(model_name):
    response = create_device(model_name=model_name)
    assert response.status_code == 400

def test_create_device_duplicate():
    eui = "1122334455667788"
    model_name = "Duplicate Test Device"

    response = create_device(eui=eui, model_name=model_name)
    assert response.status_code == 201


    response_duplicate = create_device(eui=eui, model_name=model_name)
    assert response_duplicate.status_code ==400

    remove_device(eui=eui)

@pytest.mark.parametrize("payload", [
    {},
    {"eui": "0011223344556677"},
    {"modelName": "Test Device Only Name"},
])
def test_create_device_missing_fields(payload):
    response = create_device_custom_payload(payload=payload)
    assert response.status_code == 400


@pytest.fixture(scope="session", autouse=True)
def cleanup_test_devices():
    yield

    response_test_devices = get_device_by_model(model_name="Test")

    if response_test_devices.status_code == 200:
        devices = response_test_devices.json()
        for device in devices:
            eui = device.get("eui")
            model = device.get("modelName")
            if "Test" in model:
                remove_device(eui=eui)