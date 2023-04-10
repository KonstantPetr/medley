import sqlite3

from extensions import convert_to_binary_data, show_object


# Функция: поиск объекта
def search_object(query):

    # инициализируем базу данных
    connect = sqlite3.connect('storage/data/db_build_buddy.db')
    cursor = connect.cursor()

    # здесь поиск по базе
    if query[1] == 'num':
        # алгоритм поиска по кадастровому номеру в БД
        sql_query = """select cadastral_number, addres, status_problem, status_execution, priority, deadline 
                       from objects where cadastral_number = ?"""
        cursor.execute(sql_query, (query[0],))
        records = cursor.fetchall()
        cursor.close()
        try:
            records = list(records[0])
        except IndexError:
            records = 'bad_request'
        return records

    elif query[1] == 'addr':
        # алгоритм поиска по адресу в БД
        sql_query = """select cadastral_number, addres, status_problem, status_execution, priority, deadline 
                       from objects where addres = ?"""
        cursor.execute(sql_query, (query[0],))
        records = cursor.fetchall()
        cursor.close()
        try:
            records = list(records[0])
        except IndexError:
            records = 'bad_request'
        return records


# Функция: добавить основные данные в таблицу
def insert_primary_data_to_the_table(query):

    try:
        sqlite_connection = sqlite3.connect('storage/data/db_build_buddy.db')
        cursor = sqlite_connection.cursor()

        sqlite_insert_query = """INSERT OR IGNORE INTO objects
                                 (cadastral_number, addres, status_problem, status_execution, tracking,
                                  priority, deadline) VALUES (?, ?, ?, ?, ?, ?, ?)"""

        data_tuple = tuple(query)  # Преобразование данных в формат кортежа
        cursor.execute(sqlite_insert_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()
        return 'Вы успешно добавили объект'

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        return 'с базой данных что-то не так'
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# Функция: добавить файл к объекту
def insert_file_to_the_table(query):  # query[0] - файл, query[1] - кадастровый номер

    try:
        sqlite_connection = sqlite3.connect('storage/data/db_build_buddy.db')
        cursor = sqlite_connection.cursor()

        sqlite_update_query = """UPDATE objects
                                 SET document = ?
                                 WHERE cadastral_number = ?"""

        query[0] = convert_to_binary_data(query[0])
        data_tuple = tuple(query)
        cursor.execute(sqlite_update_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()
        return 'Файл успешно добавлен'

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        return 'с базой данных что-то не так'
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# Функция: добавить фото к объекту
def insert_photo_to_the_table(query):  # query[0] - файл, query[1] - кадастровый номер

    try:
        sqlite_connection = sqlite3.connect('storage/data/db_build_buddy.db')
        cursor = sqlite_connection.cursor()

        sqlite_update_query = """UPDATE objects
                                 SET photo = ?
                                 WHERE cadastral_number = ?"""

        query[0] = convert_to_binary_data(query[0])
        data_tuple = tuple(query)
        cursor.execute(sqlite_update_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()
        return 'Фото успешно добавлено'

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        return 'с базой данных что-то не так'
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# Функция: изменить подписку на объект
def change_subscribe_of_object(cad_num):

    try:
        sqlite_connection = sqlite3.connect('storage/data/db_build_buddy.db')
        cursor = sqlite_connection.cursor()

        sql_query = """SELECT tracking 
                       FROM objects 
                       WHERE cadastral_number = ?"""
        cursor.execute(sql_query, (cad_num,))
        tracking = int(cursor.fetchall()[0][0])

        sqlite_update_query = """UPDATE objects
                                 SET tracking = ?
                                 WHERE cadastral_number = ?"""

        tracking = {0: 1, 1: 0}[tracking]
        data_tuple = (tracking, cad_num)
        cursor.execute(sqlite_update_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()
        code_1 = {0: 'Да', 1: 'Нет'}
        code_2 = {1: 'Да', 0: 'Нет'}
        return f'Вы изменили статус отслеживания с {code_1[tracking]} на {code_2[tracking]}'

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        return 'с базой данных что-то не так'
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# Функция: изменить статус объекта
def change_status_problem_of_object(cad_num):

    try:
        sqlite_connection = sqlite3.connect('storage/data/db_build_buddy.db')
        cursor = sqlite_connection.cursor()

        sql_query = """SELECT status_problem 
                       FROM objects 
                       WHERE cadastral_number = ?"""
        cursor.execute(sql_query, (cad_num,))
        status_problem = int(cursor.fetchall()[0][0])

        sqlite_update_query = """UPDATE objects
                                 SET status_problem = ?
                                 WHERE cadastral_number = ?"""

        status_problem = {0: 1, 1: 0}[status_problem]
        data_tuple = (status_problem, cad_num)
        cursor.execute(sqlite_update_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()
        code_1 = {0: 'Да', 1: 'Нет'}
        code_2 = {1: 'Да', 0: 'Нет'}
        return f'Вы изменили статус проблемности с {code_1[status_problem]} на {code_2[status_problem]}'

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        return 'с базой данных что-то не так'
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# Функция: изменить приоритет объекта
def change_priority_of_object(cad_num):

    try:
        sqlite_connection = sqlite3.connect('storage/data/db_build_buddy.db')
        cursor = sqlite_connection.cursor()

        sql_query = """SELECT priority 
                       FROM objects 
                       WHERE cadastral_number = ?"""
        cursor.execute(sql_query, (cad_num,))
        priority = int(cursor.fetchall()[0][0])

        sqlite_update_query = """UPDATE objects
                                 SET priority = ?
                                 WHERE cadastral_number = ?"""

        priority = {0: 1, 1: 0}[priority]
        data_tuple = (priority, cad_num)
        cursor.execute(sqlite_update_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()
        code_1 = {0: 'Да', 1: 'Нет'}
        code_2 = {1: 'Да', 0: 'Нет'}
        return f'Вы изменили статус приоритета с {code_1[priority]} на {code_2[priority]}'

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        return 'с базой данных что-то не так'
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# Функция: изменить адрес объекта
def change_address_of_object(query):
    try:
        sqlite_connection = sqlite3.connect('storage/data/db_build_buddy.db')
        cursor = sqlite_connection.cursor()

        sqlite_update_query = """UPDATE objects
                                 SET addres = ?
                                 WHERE cadastral_number = ?"""

        data_tuple = (query[0], query[1])
        cursor.execute(sqlite_update_query, data_tuple)
        sqlite_connection.commit()
        cursor.close()
        return 'Вы успешно откорректировали адрес'

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite:", error)
        return 'с базой данных что-то не так'
    finally:
        if sqlite_connection:
            sqlite_connection.close()


# фильтры и сортировки
def filter_by_priority(priority):
    pass


def filter_by_added(date):
    pass


def sort_by_solution(solution):
    pass


def sort_by_deadline(deadline):
    pass


def sort_by_number(cad_num):
    pass


def sort_by_address(address):
    pass


if __name__ == '__main__':

    # Создание и соединение с базой данных
    con = sqlite3.connect('storage/data/db_build_buddy.db')
    cur = con.cursor()
    con.commit()

    # Создание таблиц базы данных
    cur.execute(""" CREATE TABLE IF NOT EXISTS objects(
            id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE,
            cadastral_number TEXT NOT NULL UNIQUE,
            addres TEXT NOT NULL UNIQUE,
            status_problem INTEGER NOT NULL,
            document BLOB,
            photo BLOB,
            status_execution INTEGER,
            tracking INTEGER,
            priority INTEGER,
            deadline TEXT
            );
    """)
    con.commit()

    print(search_object(['47141203001818', 'num']))
    print(search_object(['Проезд Смольный, д. 1, лит. Б.', 'addr']))

    query_1 = [
                47141203001818,  # arg_cadastral_number
                'Проезд Смольный, д. 1, лит. Г.',  # arg_addres
                1,  # arg_status_problem
                1,  # arg_status_execution
                1,  # arg_tracking
                1,  # arg_priority
                '24.05.2023'  # arg_deadline
               ]
    insert_primary_data_to_the_table(query_1)
    insert_file_to_the_table(['storage/data/document_2.docx', 47141203001818])
    insert_photo_to_the_table(['storage/data/photos/file_0.jpg', 47141203001818])

    print(show_object(search_object(['47141203001818', 'num'])))
