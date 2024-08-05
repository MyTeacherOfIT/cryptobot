import datetime
import sqlite3


def insert_info(user_id: int, crypto: str):
    """
    :param user_id: ID телеграм аккаунта
    :param crypto: название криптовалюты

    Добавление информации в базу данных о поиске информации о криптовалюте
    """
    connection = sqlite3.connect('skillcrypto.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO cryptocurrencies (user_id, date, command, crypto) 
    VALUES (?, ?, ?, ?)
    ''', (user_id, datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), "info", crypto))
    connection.commit()
    connection.close()


def insert_top(user_id: int):
    """
    :param user_id: ID телеграм аккаунта

    Добавление информации в базу данных о поиске топ 10 криптовалют
    """
    connection = sqlite3.connect('skillcrypto.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO cryptocurrencies (user_id, date, command, crypto) 
    VALUES (?, ?, ?, ?)
    ''', (user_id, datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), "top10", "top10"))
    connection.commit()
    connection.close()


def insert_price(user_id: int, crypto: str):
    """
    :param user_id: ID телеграм аккаунта
    :param crypto: название криптовалюты

    Добавление информации в базу данных о поиске стоимости криптовалюте
    """
    connection = sqlite3.connect('skillcrypto.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO cryptocurrencies (user_id, date, command, crypto) 
    VALUES (?, ?, ?, ?)
    ''', (user_id, datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), "price", crypto))
    connection.commit()
    connection.close()


def insert_top_ex(user_id: int):
    """
    :param user_id: ID телеграм аккаунта

    Добавление информации в базу данных о поиске топ 10 криптобирж
    """
    connection = sqlite3.connect('skillcrypto.db')
    cursor = connection.cursor()
    cursor.execute('''
    INSERT INTO cryptocurrencies (user_id, date, command, crypto) 
    VALUES (?, ?, ?, ?)
    ''', (user_id, datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"), "top_ex", "top_ex"))
    connection.commit()
    connection.close()


def get_base(user_id: int):
    """
    :param user_id: ID телеграм аккаунта
    :return: список всех запросов User
    """
    connection = sqlite3.connect('skillcrypto.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM cryptocurrencies""")
    results = cursor.fetchall()
    connection.close()
    user_requests: list = []
    for result in results:
        if result[0] == user_id:
            user_requests.append(result)
    return user_requests


def get_base_2(user_id: int, date: str):
    """
    :param user_id: ID телеграм аккаунта
    :param date: дата запроса
    :return: запрос по дате
    """
    connection = sqlite3.connect('skillcrypto.db')
    cursor = connection.cursor()
    cursor.execute("""SELECT * FROM cryptocurrencies""")
    results = cursor.fetchall()
    connection.close()
    for result in results:
        if result[0] == user_id and result[1] == date:
            return result
