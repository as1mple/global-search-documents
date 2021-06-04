import datetime
import requests
from typing import List
from pprint import pprint

import numpy as np
from pydantic import BaseModel, ValidationError


class Items(BaseModel):
    title: str
    date: int
    size: int
    url: str


class Response(BaseModel):
    count: int
    items: List[Items]


class Vk(BaseModel):
    response: Response


def get_setting() -> list:
    with open("setting.txt", "r") as fl:
        setting = fl.readlines()
    version = setting[0].replace("version=", "".replace("\n", ""))
    token = setting[1].replace("token=", "").replace("\n", "")
    proxy = setting[2].replace("proxy=", "")
    return [version, token, proxy]


def get_doc(search: str, count: str) -> dict:
    version, token, proxy = get_setting()
    search_own = "0"
    return_targs = "1"
    result = {}
    iteration = 0
    URL = "https://api.vk.com/method/docs.search?"
    while True:
        try:
            response = requests.get(URL,
                                    timeout=3,
                                    params={
                                        "access_token": token,
                                        "q": search,
                                        "search_own": search_own,
                                        "count": count,
                                        "return_tags": return_targs,
                                        "v": version},
                                    proxies={"https": f"https://{proxy}"},
                                    verify=False
                                    )
            print("Successful")
            break
        except Exception as e:
            iteration += 1
            print("error", e[:10])
            if iteration == 5:
                return {'result': "404"}

    data = response.json()

    try:
        vk = Vk(**data)
        [result.update({vk.response.items[i].url: [vk.response.items[i].title, vk.response.items[i].size / 1_000_000,
                                                   datetime.datetime.fromtimestamp(vk.response.items[i].date).strftime(
                                                       '%Y-%m-%d %H:%M:%S')]})
         for i in np.arange(len(vk.response.items) - 1, -1, -1)]
    except ValidationError as e:
        pprint(e.json())
    print("-" * 128)
    return result
