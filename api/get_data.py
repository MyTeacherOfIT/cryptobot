import requests
import json


def get_info(token: str):
    """
    :param token: ID криптовалюты
    :return: описание и логотип криптовалюты
    """
    from config_data.config import API_KEY
    url = f"https://api.coingecko.com/api/v3/coins/{token}?developer_data=true&x_cg_demo_api_key={API_KEY}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data: dict = json.loads(response.text)
    bbt = ""
    forum = ""
    for url in data["links"]["official_forum_url"]:
        if url != "":
            forum = url
            break
    else:
        forum = "-"
    for i in data["links"]["blockchain_site"]:
        if i != "":
            bbt = bbt + i + "\n"
            break
    else:
        bbt = "-"
    text = f"""
{data['name']}({data['symbol']})
                
Топ криптовалют: {str(data["market_cap_rank"])}
        
Время блокировки в минутах: {str(data["block_time_in_minutes"])}
        
{bbt}
        
Сайт: {data["links"]["homepage"][0]}
        
Форум: {forum}

"""
    if data["links"]["twitter_screen_name"] != "":
        text += f"""Twitter: @{data["links"]["twitter_screen_name"]}\n\n"""
    if data["links"]["facebook_username"] != "":
        text += f"""Facebook: @{data["links"]["facebook_username"]}"""
    return text, data['image']['large']


def get_top10():
    """
    :return: список информации и список логотипов топ 10 криптовалют по капитализации в валюте
    """
    from config_data.config import API_KEY
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&x_cg_demo_api_key={API_KEY}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    text: list = []
    lst_im: list = []
    for i in range(10):
        text.append(f"""
Топ {str(i + 1)}.

{data[i]["name"]} ({data[i]["symbol"]})

Рыночная капитализация в валюте: {data[i]['market_cap']}$

Стоимость: {data[i]['current_price']}$
""")
        lst_im.append(data[i]["image"])
    return text, lst_im


def get_price(token: str):
    """
    :param token: ID криптовалюты
    :return: стоимость и капитализация криптовалюты
    """
    from config_data.config import API_KEY
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={token}&vs_currencies=usd&include_market_cap=true&x_cg_demo_api_key={API_KEY}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data: dict = json.loads(response.text)
    text = f"""
Стоимость {token}: {data[token]['usd']}$

Капитализация {token}: {data[token]['usd_market_cap']}$
    """

    return text


def get_tokens():
    """
    :return: словарь символ криптовалюты - id криптовалюты
    """
    from config_data.config import API_KEY
    url = f"https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&x_cg_demo_api_key={API_KEY}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data: dict = json.loads(response.text)
    user_data: dict = {}
    for i in range(100):
        user_data[data[i]["symbol"]] = data[i]["id"]
    return user_data


def get_top_exchanges():
    """
    :return: список информации и список логотипов топ 10 криптобирж
    """
    from config_data.config import API_KEY
    url = f"https://api.coingecko.com/api/v3/exchanges?per_page=100&x_cg_demo_api_key={API_KEY}"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    data = json.loads(response.text)
    text: list = []
    lst_im: list = []
    for i in range(10):
        text.append(f"""
Топ {str(i + 1)}.

{data[i]["name"]}

Страна: {data[i]['country']}$

Дата основания: {data[i]['year_established']}г.
    
Ссылка на биржу: {data[i]["url"]}
""")
        lst_im.append(data[i]["image"])
    return text, lst_im
