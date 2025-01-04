import os

import aiohttp


BASE_URL = os.getenv("BASE_URL")
BOT_TOKEN = os.getenv("BOT_TOKEN")


# TODO: Прикрутить логгер


class ApiClient:

    def __init__(self):
        self.base_url = BASE_URL
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": BOT_TOKEN
        }
        self.add_url = ""

    async def send_get(self, params: dict =None):
        if not params:
            url = self.base_url + self.add_url
        else:
            url_query = "&".join([f"{param_name}={param_value}" for param_name, param_value in params.items()])
            url = self.base_url + self.add_url + "?" + url_query

        print(f"Sending GET to {url}")

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=self.headers) as response:
                status_code = response.status

                if status_code != 200:
                    error_text = await response.text()
                    print(f"Fail to send GET to {url}. Response: {error_text}")
                    return
                else:
                    data = await response.json()
                    return data

    async def send_post(self, data: dict):
        url = self.base_url + self.add_url
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=self.headers) as response:
                status_code = response.status
                if status_code != 201:
                    error_text = await response.text()
                    print(f"Fail to send POST to {url}. Response: {error_text}")
                    return
                else:
                    response_data = await response.json()
                    return response_data

class TrainingApi(ApiClient):

    def __init__(self):
        super().__init__()
        self.add_url = "exercise/trainings/"

    async def get_all_trainings(self):
        return await self.send_get()

    async def create_new_training(self, data):
        return await self.send_post(data)


class HistoryApi(ApiClient):

    def __init__(self):
        super().__init__()
        self.add_url = "exercise/stories/"

    async def add_new_history(self, data):
        return await self.send_post(data)


class UsersApi(ApiClient):

    def __init__(self):
        super().__init__()
        self.add_url = "users/telegram_users/"

    async def get_user_by_tg_id(self, tg_id):
        result = await self.send_get({"telegram_id": tg_id})
        if result:
            return result[0]


class UserGroupApi(ApiClient):

    def __init__(self):
        super().__init__()
        self.add_url = "users/telegram_user_groups/"

    async def get_groups_by_user_id(self, user_id):
        result = await self.send_get({"user": user_id})
        if result:
            return result
