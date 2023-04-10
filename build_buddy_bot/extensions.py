import json
import re


# класс для организации временной памяти в боте
class TempData:

    def __init__(self, _object=None, _path: str = 'storage/data/temp.json'):
        self._object = _object
        self._path = _path

    # кладём временные данные в файл
    def add_data_to_temp(self):
        with open(self._path, 'w', encoding='utf-8') as temp_file:
            json.dump(self._object, temp_file, ensure_ascii=False, indent=4)

    # берём временные данные из файла
    def get_data_from_temp(self):
        try:
            with open(self._path, 'r', encoding='utf-8') as temp_file:
                self._object = json.load(temp_file)
        except IOError:
            return 'Проблема с файловой системой'
        except json.decoder.JSONDecodeError:
            return 'Объект не выбран'
        return self._object

    # чистим временный файл
    def clear_data_in_temp(self):
        try:
            with open(self._path, 'r+') as temp_file:
                temp_file.truncate()
        except IOError:
            return 'Проблема с файловой системой'
        except json.decoder.JSONDecodeError:
            return 'Объект не выбран'


# получение изображения
def get_image(img_path):
    dir_path = 'storage/menu_img/'
    return open(f'{dir_path}{img_path}', 'rb')


# определение, вести поиск по кадастровому номеру или по адресу или плохой запрос
def ident_search_type(text):

    test_num = re.match(r'(\d{2}):(\d{2}):(\d{4,}):(\d{2,}\W)', text)
    test_addr = re.match(r'(.+),(\s?)д(.{2,5}),(.+)', text)

    if test_num:
        return 'num'
    elif test_addr:
        return 'addr'
    else:
        return 'bad'


# преобразование кадастрового номера в приемлемый вид для базы данных
def make_cad_num_for_db(num_str):
    num_int = int(''.join([num_str[i] for i in range(len(num_str)) if num_str[i] != ':']))
    return num_int


# проверка на да/нет
def check_yn(answer):
    return 1 if answer in ['да', 'нет'] else 0


# проверка на дату
def check_date(text):
    test_date = re.match(r'(\d{2})\.(\d{2})\.(\d{4})', text)
    return 1 if test_date else 0


# Функция: конвертация изображений и файлов в бинарные данные
def convert_to_binary_data(filename):
    # Преобразование данных в двоичный формат
    with open(filename, 'rb') as file:
        blob_data = file.read()
    return blob_data


# приведение объекта, полученного из БД в удобоваримый вид для отображения
def show_object(object_list):
    keys = [
            'Кадастровый номер: ', 'Адрес: ', 'Проблемный: ',
            'Решение выполнено: ', 'В приоритете: ', 'Дедлайн по объекту: '
            ]
    object_data = ''
    for i, object_attr in enumerate(object_list):
        if type(object_attr) == int:
            object_attr = {0: 'Нет', 1: 'Да'}[object_attr]
        object_data += f'{keys[i]}{object_attr}\n'
    return object_data


if __name__ == '__main__':

    pass
