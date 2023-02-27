import requests


ENDPOINT = "https://todo.pixegami.io/"

# response = requests.get(ENDPOINT) #calling this returns a reponse object
# print(response)

# data = response.json()
# print(data)

# status_code = response.status_code
# print(status_code)

def test_can_call_endpoint():
    response = requests.get(ENDPOINT)
    assert response.status_code == 200

def test_can_create_task():
    payload = { 
    "content": "test content",
    "user_id": "test_user",
    # "task_id": "test_task_id", dont need task_id as the server provides one
    "is_done": False, 
    }

    create_task_response = requests.put(ENDPOINT + "/create-task", json=payload)
    assert create_task_response.status_code == 200

    data = create_task_response.json()
    print(data)

    task_id = data["task"]["task_id"]
    get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}")

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"] #both passed as intended (python -m pytest -v -s)
    # assert get_task_data["content"] == "some other value" # intentional fail just to check
    assert get_task_data["user_id"] == payload["user_id"]