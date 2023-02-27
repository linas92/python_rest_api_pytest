import requests
import uuid


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
    # payload = { --- refactoring code
    # "content": "test content",--- refactoring code
    # "user_id": "test_user",--- refactoring code
    # # "task_id": "test_task_id", dont need task_id as the server provides one--- refactoring code
    # "is_done": False, --- refactoring code
    # }--- refactoring code
    payload = new_task_payload()#--- refactored code

    # create_task_response = requests.put(ENDPOINT + "/create-task", json=payload) --- refactoring code
    create_task_response = create_task(payload) #--- refactored code
    assert create_task_response.status_code == 200

    data = create_task_response.json()

    task_id = data["task"]["task_id"]
    # get_task_response = requests.get(ENDPOINT + f"/get-task/{task_id}") --- refactoring code
    get_task_response = get_task(task_id) #--- refactored code

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"] #both passed as intended (python -m pytest -v -s)
    # assert get_task_data["content"] == "some other value" # intentional fail just to check
    assert get_task_data["user_id"] == payload["user_id"]

def test_can_update_task():
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "updated content",
        "is_done": True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]

def test_can_list_tasks():
    n = 3
    payload = new_task_payload()
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200
    
    user_id = payload["user_id"]
    list_task_response = list_tasks(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()

    tasks = data["tasks"]
    assert len(tasks) == n


def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)

def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)

def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")

def list_tasks(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")

def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"

    return { 
    "content": content,
    "user_id": user_id,
    # "task_id": "test_task_id", dont need task_id as the server provides one
    "is_done": False, 
    }
