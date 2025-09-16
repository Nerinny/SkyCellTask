import requests
from requests import Response
import os

BASE_URL = os.getenv("API_URL")

def get_device_by_id(eui: str = "0011223344556677", base_url: str = BASE_URL) -> Response:
    url = f"{base_url}/api/devices/{eui}"
    headers = {
        "Accept": "application/json",
    }

    response = requests.get(headers=headers, url=url)
    return response

def get_device_by_model(model_name : str= "Test Model Name", base_url: str = BASE_URL) -> Response:
    url = f"{base_url}/api/devices/"
    headers = {
        "Accept": "application/json",
    }

    payload = { 'modelFilter': model_name}


    response = requests.get(headers=headers, params=payload, url=url)
    return response

def create_device(eui: str = "0011223344556677", model_name: str | None = "Test Model Name", base_url: str = BASE_URL) -> Response:
    url = f"{base_url}/api/devices"

    headers= {
        "Accept": "application/json",
    }

    payload = {
        "eui": eui,
        "modelName" : model_name
    }

    response = requests.post(url, json=payload, headers=headers)
    return response

def create_device_custom_payload(payload: dict, base_url: str = BASE_URL) -> Response:
    url = f"{base_url}/api/devices"

    headers= {
        "Accept": "application/json",
    }

    response = requests.post(url, json=payload, headers=headers)
    return response

def remove_device(eui: str = "0011223344556677", base_url: str = BASE_URL) -> Response:
    url = f"{base_url}/api/devices/{eui}"
    headers= {
        "Accept": "*/*",
    }

    response = requests.delete(url, headers=headers)
    return response
