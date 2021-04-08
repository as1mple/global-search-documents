import datetime

import requests


def get_setting() -> list:
    with open("setting.txt", "r") as fl:
        setting = fl.readlines()
    version = setting[0].replace("version=", "".replace("\n", ""))
    token = setting[1].replace("token=", "").replace("\n", "")
    proxy = setting[2].replace("proxy=", "")
    return [version, token, proxy]


def get_doc(search, count) -> dict:
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
            print("error")
            if iteration == 5:
                return {'result': "404"}

    data = response.json()
    res = data.get('response', "No")

    print(f"COUNT = {res.get('count', 'No')}")
    items = res.get("items", "NO")
    items.reverse()
    try:
        for i in range(int(count)):
            title = items[i].get('title', '')
            date = items[i].get('date', '')
            time = datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')
            size = items[i].get('size', '') / 1_000_000
            url = items[i].get('url', '')
            result.update({url: [title, size, time]})

    except IndexError as e:
        print(e)
    print("-" * 128)
    return result