import datetime
import os
import requests


API_URL = os.environ.get("SOLIDTIME_API_URL", "https://app.solidtime.io/api/v1")
ORG_ID = os.environ.get("SOLIDTIME_ORG_ID", None)
API_TOKEN = os.environ.get("SOLIDTIME_API_TOKEN", None)
USER_EMAIL = os.environ.get("SOLIDTIME_USER_EMAIL", None)

class SolidTimeClient:
    def __init__(self):
        if not ORG_ID:
            raise ValueError("ORG_ID is not set")
        if not API_TOKEN:
            raise ValueError("API_TOKEN is not set")
        if not USER_EMAIL:
            raise ValueError("USER_EMAIL is not set")
        self.url = API_URL
        self.user_id = self.__user_id()
        self.member_id = self.__member_id()

    def __headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_TOKEN}"
        }

    def __user_id(self):
        url = f"{self.url}/users/me"
        response = requests.get(url, headers=self.__headers())
        json_respone = response.json()
        user_id = json_respone["data"].get("id")
        return user_id

    def __member_id(self):
        members = self.list_members()
        for member in members["data"]:
            if member["email"] == USER_EMAIL:
                return member["id"]
        raise ValueError("No member found")

    def list_members(self):
        url = f"{self.url}/organizations/{ORG_ID}/members"
        response = requests.get(url, headers=self.__headers())
        json_response = response.json()
        return json_response

    def get_current_timer(self):
        url = f"{self.url}/users/me/time-entries/active"
        response = requests.get(url, headers=self.__headers())
        json_response = response.json()
        data = json_response.get("data")
        if data:
            return json_response
        return False # No timer is running

    def start_timer(self, description, billable):
        url = f"{self.url}/organizations/{ORG_ID}/time-entries"
        payload = {
            "task_id": None,
            "member_id": self.member_id,
            "project_id": None,
            "start": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "billable": billable,
            "description": description,
            "tags": []
        }
        response = requests.post(url, headers=self.__headers(), json=payload)
        return response.json()

    def stop_timer(self, current_timer):
        if not current_timer:
            raise ValueError("No timer is running")
        start = current_timer["data"]["start"]
        timer_id = current_timer["data"]["id"]
        url = f"{self.url}/organizations/{ORG_ID}/time-entries/{timer_id}"
        payload = {
            "start": start,
            "end": datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "user_id": self.user_id
        }
        response = requests.put(url, headers=self.__headers(), json=payload)
        return response.json()
