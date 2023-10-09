import requests
import json
import os
from jsonschema.validators import validate
from conftest import resources_path


def test_login_successful():
    email = "eve.holt@reqres.in"
    password = "123456"
    response = requests.post(
        url='https://reqres.in/api/login',
        data={"email": email, "password": password}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert len(response_json['token'][0]) != 0


def test_login_not_successful():
    email = ""
    password = ""
    response = requests.post(
        url='https://reqres.in/api/login',
        data={"email": email, "password": password}
    )
    assert response.status_code == 400
    response_json = response.json()
    assert response_json['error'] == 'Missing email or username'


def test_all_users():
    with open(os.path.join(resources_path, 'get_users_schema.json')) as file:
        schema = json.loads(file.read())
    response = requests.get("https://reqres.in/api/users")
    response_json = response.json()
    validate(instance=response_json, schema=schema)


def test_single_users():
    with open(os.path.join(resources_path, 'get_single_user_schema.json')) as file:
        schema = json.loads(file.read())
    response = requests.get("https://reqres.in/api/users/2")
    response_json = response.json()
    validate(instance=response_json, schema=schema)


def test_get_all_users_list():
    resp = requests.get("https://reqres.in/api/users")
    assert resp.status_code == 200


def test_users_per_page():
    per_page = 7
    response = requests.get(
        url="https://reqres.in/api/users",
        params={"per_page": per_page}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['per_page'] == per_page


def test_open_single_user():
    user_id = 7
    response = requests.get(
        url=f"https://reqres.in/api/users/{user_id}",
        params={"id": user_id}
    )
    assert response.status_code == 200
    response_json = response.json()
    assert response_json['data']['id'] == user_id


def test_open_not_exist_single_user():
    user_id = 666
    response = requests.get(
        url=f"https://reqres.in/api/users/{user_id}",
        params={"id": user_id}
    )
    assert response.status_code == 404


def test_create_user():
    name = "Aleksandr"
    job = "Psevdo_QA"
    response = requests.post(
        url='https://reqres.in/api/users',
        data={"name": name, "job": job}
    )
    assert response.status_code == 201
    response_json = response.json()
    assert response_json['name'] == name
    assert response_json['job'] == job


def test_user_register_successful():
    email = "eve.holt@reqres.in"
    password = "123456"
    response = requests.post(
        url='https://reqres.in/api/register',
        data={"email": email, "password": password}
    )
    assert response.status_code == 200


def test_user_register_not_successful():
    password = "123456"
    response = requests.post(
        url='https://reqres.in/api/register',
        data={"password": password}
    )
    assert response.status_code == 400
    response_json = response.json()
    assert response_json['error'] == 'Missing email or username'
