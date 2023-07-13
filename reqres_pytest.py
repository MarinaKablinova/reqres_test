import requests
from jsonschema import validate
import schemas
from datetime import datetime

def send_request(type, uri, data = {}, headers = {}):
    url = "https://reqres.in/api/"+uri
    response = requests.request(type, url, headers=headers, data=data)
    return response

def test_full_users_list():
    url = "users?page=1&per_page=12"
    response = send_request("GET", url)
    response_dict = response.json()

    assert len(response_dict['data']) == 12, "List should contain all the values"
    assert response.status_code == 200, "Error code should be 200"

def test_part_of_the_users_list():
    url = "users?page=2&per_page=2"
    response = send_request("GET", url)
    response_dict = response.json()

    assert response.status_code == 200, "Error code should be 200"
    assert response_dict['data'][0]['id'] == 3 and response_dict['data'][1]['id'] == 4, "Response should return users with id's 3 and 4"
    assert len(response_dict['data']) == 2, "List should contain all the values"

def test_user_data():
    url = "users/2"
    response = send_request("GET", url)
    response_dict = response.json()

    assert response.status_code == 200, "Error code should be 200"
    assert response_dict['data']['id'] == 2, "Response should return user with id = 2"

    #Check JSON schema
    try:
        validate(response_dict['data'], schemas.schema_user)
    except:
        print("Incorrect output for User, check JSON schema")

def test_user_data_with_invalid_id():
    url = "users/0"
    response = send_request("GET", url)
    response_dict = response.json()

    assert len(response_dict) == 0, "Request should return empty JSON file"
    assert response.status_code == 404, "Error code for non-existent User should be 404"

    url = "users/13"
    response = send_request("GET", url)
    response_dict = response.json()

    assert len(response_dict) == 0, "Request should return empty JSON file"
    assert response.status_code == 404, "Error code for non-existent User should be 404"

def test_resources_list():
    url = "{resource}?page=1&per_page=12"
    response = send_request("GET", url)
    response_dict = response.json()

    assert len(response_dict['data']) == 12, "List should contain all the values"
    assert response.status_code == 200, "Error code should be 200"

def get_part_of_the_resources_list():
    url = "{resource}?page=2&per_page=2"
    response = send_request("GET", url)
    response_dict = response.json()

    assert response.status_code == 200, "Error code should be 200"
    assert response_dict['data'][0]['id'] == 3 and response_dict['data'][1]['id'] == 4, "Response should return users with id's 3 and 4"
    assert len(response_dict['data']) == 2, "List should contain all the values"

def test_get_one_resource_data():
    url = "{resource}/4"
    response = send_request("GET", url)
    response_dict = response.json()

    assert response.status_code == 200, "Error code should be 200"
    assert response_dict['data']['id'] == 4, "Response should return user with id = 2"

    #Check JSON schema
    try:
        validate(response_dict['data'], schemas.schema_resource)
    except:
        print("Incorrect output for Resource, check JSON schema")

def test_resouce_data_with_invalid_id():
    url = "{resource}/0"
    response = send_request("GET", url)
    response_dict = response.json()

    assert len(response_dict) == 0, "Request should return empty JSON file"
    assert response.status_code == 404, "Error code for non-existent Resource should be 404"

    url = "{resource}/13"
    response = send_request("GET", url)
    response_dict = response.json()

    assert len(response_dict) == 0, "Request should return empty JSON file"
    assert response.status_code == 404, "Error code for non-existent Resource should be 404"

def test_request_delay():
    start = datetime.utcnow()
    url = "users?delay=10"
    response = send_request("GET", url)
    response_dict = response.json()
    finish = datetime.utcnow()
    res = finish-start
    assert res.seconds == 10, "Delay should be 10 sec"
    assert response.status_code == 200, "Request successfull"

headers = {}

#POST TESTS
def test_register_new_user():
    url = "register"
    payload = {
            "email": "eve.holt@reqres.in",
            "password": "pistol"
            }
    response = send_request("POST", url, payload)
    response_dict = response.json()

    assert ('id' in response_dict.keys() and 'token' in response_dict.keys()) == True, "Output should contain id and token values"
    assert response.status_code == 200, "Invalid Error code"

def test_register_new_user_part_data():
    url = "register"
    payload = {
            "email": "eve.holt@reqres.in"
           }
    response = send_request("POST", url, payload)
    response_dict = response.json()

    assert response_dict["error"] == "Missing password", "Invalid error message"
    assert response.status_code == 400, "Invalid Error code"

def test_register_new_user_invalid_data():
    url = "register"
    payload = {
        "username": "testUser",
        "email": "testEmail@mail.com",
        "password": "qwe45werty"
    }
    response = send_request("POST", url, payload)
    response_dict = response.json()

    assert response_dict["error"] == "Note: Only defined users succeed registration", "Invalid error message"
    assert response.status_code == 400, "Invalid Error code"

def test_register_new_user_empty_data():
    url = "register"
    payload = {
        "username": "",
        "email": "",
        "password": ""
    }
    response = send_request("POST", url, payload)
    response_dict = response.json()

    assert response.status_code == 400, "Invalid Error code"

def test_user_login():
    url = "login"
    payload = {
        "email":"eve.holt@reqres.in",
        "password":"cityslicka"
    }
    response = send_request("POST", url, payload)
    response_dict = response.json()

    assert ('token' in response_dict.keys()) == True, "Invalid data"
    assert response.status_code == 200, "Invalid Error code"

def test_not_existing_user_login():
    url = "login"
    payload = {
        "username": "testUser",
        "email": "testEmail@mail.com",
        "password": "pass123"
    }
    response = send_request("POST", url, payload)
    response_dict = response.json()

    assert response_dict["error"] == "user not found"
    assert response.status_code == 400, "Invalid Error code"

def test_user_login_part_fields():
    url = "login"
    payload = {
        "password":"cityslicka"
    }
    response = send_request("POST", url, payload)
    response_dict = response.json()

    assert response_dict["error"] == "Missing email or username"
    assert response.status_code == 400, "Invalid Error code"

def test_update_user_data_PATCH():
    url = "users/2"
    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }

    response = send_request("PATCH", url, payload)
    response_dict = response.json()

    try:
        validate(response_dict, schemas.schema_update_user)
    except:
        print("Incorrect output, check JSON schema")
    assert response.status_code == 200, "Invalid Error code"

def test_update_user_data_empty_body_PATCH():
    url = "users/2"
    payload = {}
    response = send_request("PATCH", url, payload)
    response_dict = response.json()

    try:
        validate(response_dict, schemas.schema_update_user_part)
    except:
        print("Incorrect output, check JSON schema")

    assert response.status_code == 200, "Invalid Error code"

def test_update_user_data_invalid_id_PATCH():
    url = "users/123"
    payload = {
        "name": "invalid_Id",
        "job": "invalid_Id"
    }
    response = send_request("PATCH", url, payload)
    response_dict = response.json()

    try:
        validate(response_dict, schemas.schema_update_user)
    except:
        print("Incorrect output, check JSON schema")

    assert response.status_code == 200, "Invalid Error code"

def test_update_user_data_PUT():
    url = "users/2"
    payload = {
        "name": "morpheus",
        "job": "zion resident"
    }
    response = send_request("PUT", url, payload)
    response_dict = response.json()

    try:
        validate(response_dict, schemas.schema_update_user)
    except:
        print("Incorrect output, check JSON schema")

    assert response.status_code == 200, "Invalid Error code"

def test_update_user_data_empty_body_PUT():
    url = "users/2"
    payload = {}
    response = send_request("PUT", url, payload)
    response_dict = response.json()

    try:
        validate(response_dict, schemas.schema_update_user_part)
    except:
        print("Incorrect output, check JSON schema")
    assert response.status_code == 200, "Invalid Error code"

def test_update_user_data_invalid_id_PUT():
    url = "users/123"
    payload = {
        "name": "invalid_Id",
        "job": "invalid_Id"
    }
    response = send_request("PUT", url, payload)
    response_dict = response.json()

    try:
        validate(response_dict, schemas.schema_update_user)
    except:
        print("Incorrect output, check JSON schema")

    assert response.status_code == 200, "Invalid Error code"

def test_new_user_creation():
    url = "users"
    payload = {
        "name": "morpheus",
        "job": "leader"
    }
    response = send_request("POST", url, payload)
    response_dict = response.json()

    try:
        validate(response_dict, schemas.schema_new_user)
    except:
        print("Incorrect output, check JSON schema")

    assert response.status_code == 201, "Invalid Error code"

#DELETE
def test_user_delete():
    url = "users/2"
    response = send_request("DELETE", url)
    assert response.status_code == 204, "Invalid Error code"