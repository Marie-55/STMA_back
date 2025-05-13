import requests
from src.utils import routes

session= [
    {
        "date": "2025-03-30",
        "start_time": "14:00:00",
        "task_id": 1
    },
    {
        "duration": 90,
        "date": "2025-03-31",
        "start_time": "10:30:00",
        "task_id": 2
    },
    {
        "duration": 60,
        "date": "2025-04-01",
        "start_time": "08:00:00",
        "task_id": 3
    }
]


def test_create_session(t):
    response = requests.post(f"{routes.SESSION_BASE_URL}/write/add", json=t)
    print(f"Response: {response.status_code}, {response.text}")
    return response

def test_get_task():
    response = requests.get(f"{routes.SESSION_BASE_URL}/read/all")
    print(f"Response: {response.status_code}, {response.text}")
    return response

def test_update_task(id,status):
    response = requests.patch(json=f"{routes.SESSION_BASE_URL}/update/status/{id}/{status}",url=f"{routes.SESSION_BASE_URL}/update/status/{id}/{status}")
    print(f"Response: {response.status_code}, {response.text}")
    return response

def test_delete_task(id):
    response = requests.delete(json=f"{routes.SESSION_BASE_URL}/delete/{id}",url=f"{routes.SESSION_BASE_URL}/delete/{id}",)
    print(f"Response: {response.status_code}, {response.text}")
    return response

if __name__ == "__main__":
    print(routes.SESSION_BASE_URL)
    response= test_create_session(session[1])
    #response= test_get_task()
    #response= test_update_task(1,"In progress")
    #response= test_delete_task(3)
    print(response)
