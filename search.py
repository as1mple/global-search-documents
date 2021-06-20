import urllib3
import datetime
import requests
from typing import List
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

import numpy as np
from loguru import logger
from pydantic import BaseModel, ValidationError

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


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
    search_own, return_targs = 0, 1
    URL = "https://api.vk.com/method/docs.search?"
    result = dict()

    session = requests.Session()
    retry = Retry(connect=3)
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('https://', adapter)
    try:
        response = session.get(URL,
                               timeout=5,
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
    except Exception as e:
        logger.error(e)
        return {'result': "404"}

    data = response.json()

    try:
        vk = Vk(**data)
        [result.update({vk.response.items[i].url: [vk.response.items[i].title, vk.response.items[i].size / 1_000_000,
                                                   datetime.datetime.fromtimestamp(vk.response.items[i].date).strftime(
                                                       '%Y-%m-%d %H:%M:%S')]})
         for i in np.arange(len(vk.response.items) - 1, -1, -1)]
        logger.info("=> D O N E <=")
        return result

    except ValidationError as e:
        logger.error(e.json())
