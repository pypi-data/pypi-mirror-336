import clickhouse_connect  # Импорт библиотеки для работы с ClickHouse
from typing import List, Dict, Any  # Импорт типов для аннотации


def escape_sql_string(html_string: str) -> str:
    """
    Экранирует специальные символы в строке для безопасной вставки в SQL-запросы.

    Args:
        html_string (str): Исходная строка с HTML-разметкой или текстом

    Returns:
        str: Экранированная строка, безопасная для использования в SQL
    """
    if html_string is None:  # Проверка на None для корректной обработки пустых значений
        return "NULL"  # Возвращаем строку "NULL" для вставки в SQL

    # Последовательное экранирование специальных символов
    escaped = html_string.replace("\\", "\\\\")  # Замена \ на \\ для корректной обработки слешей
    escaped = escaped.replace("'", "''")         # Замена ' на '' для защиты от SQL-инъекций
    escaped = escaped.replace('"', '\\"')        # Замена " на \" для корректной работы с кавычками
    escaped = escaped.replace("\0", "\\0")       # Экранирование нулевого символа
    escaped = escaped.replace("\n", "\\n")       # Замена новой строки на \n
    escaped = escaped.replace("\r", "\\r")       # Замена возврата каретки на \r
    escaped = escaped.replace("\t", "\\t")       # Замена табуляции на \t

    return escaped  # Возвращаем экранированную строку

def flatten_dict(d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
    """
    Преобразует вложенный словарь в плоский с составными ключами.

    Args:
        d (Dict[str, Any]): Исходный словарь
        parent_key (str): Префикс для ключей (используется при рекурсии)
        sep (str): Разделитель для составных ключей

    Returns:
        Dict[str, Any]: Плоский словарь
    """
    items = []  # Список для хранения пар ключ-значение
    for key, value in d.items():  # Итерация по ключам и значениям словаря
        # Формирование нового ключа с учетом родительского ключа
        new_key = f"{parent_key}{sep}{key}" if parent_key else key
        if isinstance(value, dict):  # Если значение - словарь
            # Рекурсивно обрабатываем вложенный словарь
            items.extend(self.flatten_dict(value, new_key, sep=sep).items())
        else:  # Если значение - не словарь
            items.append((new_key, value))  # Добавляем пару в список
    return dict(items)  # Преобразуем список пар в словарь

class ClickHouseJSONHandler:
    """Класс для работы с JSON-данными и их вставкой в ClickHouse."""

    def __init__(self, host: str, database: str):
        """
        Инициализация клиента ClickHouse.

        Args:
            host (str): Адрес хоста ClickHouse
            database (str): Название базы данных
        """
        # Создание подключения к ClickHouse с указанными параметрами
        self.client = clickhouse_connect.get_client(host=host, database=database)

    def flatten_dict__(self, d: Dict[str, Any], parent_key: str = '', sep: str = '_') -> Dict[str, Any]:
        """
        Преобразует вложенный словарь в плоский с составными ключами.

        Args:
            d (Dict[str, Any]): Исходный словарь
            parent_key (str): Префикс для ключей (используется при рекурсии)
            sep (str): Разделитель для составных ключей

        Returns:
            Dict[str, Any]: Плоский словарь
        """
        items = []  # Список для хранения пар ключ-значение
        for key, value in d.items():  # Итерация по ключам и значениям словаря
            # Формирование нового ключа с учетом родительского ключа
            new_key = f"{parent_key}{sep}{key}" if parent_key else key
            if isinstance(value, dict):  # Если значение - словарь
                # Рекурсивно обрабатываем вложенный словарь
                items.extend(self.flatten_dict(value, new_key, sep=sep).items())
            else:  # Если значение - не словарь
                items.append((new_key, value))  # Добавляем пару в список
        return dict(items)  # Преобразуем список пар в словарь

    def infer_table_structure(self, json_data: List[Dict[str, Any]]) -> Dict[str, str]:
        """
        Определяет структуру таблицы на основе первого элемента JSON-данных.

        Args:
            json_data (List[Dict[str, Any]]): Список словарей с данными

        Returns:
            Dict[str, str]: Словарь с именами колонок и их типами данных
        """
        sample_entry = json_data[0]  # Берем первый элемент как образец
        flat_entry = flatten_dict(sample_entry)  # Преобразуем в плоский вид
        structure = {}  # Словарь для хранения структуры таблицы

        for key, value in flat_entry.items():  # Итерация по ключам и значениям
            if isinstance(value, int):  # Если значение - целое число
                structure[key] = "UInt32"  # Устанавливаем тип UInt32
            elif isinstance(value, float):  # Если значение - число с плавающей точкой
                structure[key] = "Float64"  # Устанавливаем тип Float64
            elif isinstance(value, str):  # Если значение - строка
                structure[key] = "String"  # Устанавливаем тип String
            elif isinstance(value, list):  # Если значение - список
                if not value:  # Если список пустой
                    structure[key] = "Array(String)"  # Устанавливаем тип массива строк
                elif all(isinstance(i, dict) for i in value):  # Если список содержит словари
                    nested_keys = value[0].keys()  # Берем ключи первого элемента
                    # Формируем тип Array(Tuple) с ключами как String
                    structure[key] = f"Array(Tuple({', '.join(f'{k} String' for k in nested_keys)}))"
                else:  # Для остальных списков
                    structure[key] = "Array(String)"  # Устанавливаем тип массива строк
            elif value is None:  # Если значение - None
                structure[key] = "Nullable(String)"  # Устанавливаем тип с поддержкой NULL
            else:  # Для всех остальных типов
                structure[key] = "String"  # По умолчанию используем String
        return structure

    def create_table(self, table_name: str, structure: Dict[str, str]):
        """
        Создает таблицу в ClickHouse на основе заданной структуры.

        Args:
            table_name (str): Название таблицы
            structure (Dict[str, str]): Структура таблицы (колонки и типы)
        """
        # Формируем строку с определением колонок
        columns = ",\n        ".join(f"{col} {dtype}" for col, dtype in structure.items())
        # SQL-запрос для создания таблицы с движком MergeTree
        query = f'''
        CREATE TABLE IF NOT EXISTS {table_name} (
            {columns}
        ) ENGINE = MergeTree
        ORDER BY tuple()  -- Простой порядок сортировки
        '''
        self.client.command(query)  # Выполняем запрос

    def insert_json_data(self, table_name: str, json_data: List[Dict[str, Any]]):
        """
        Вставляет JSON-данные в таблицу ClickHouse.

        Args:
            table_name (str): Название таблицы
            json_data (List[Dict[str, Any]]): Список словарей с данными
        """
        formatted_data = []  # Список для хранения отформатированных записей
        columns = set()  # Множество для хранения всех уникальных колонок

        # Подготовка данных для вставки
        for entry in json_data:  # Итерация по записям JSON
            flat_entry = flatten_dict(entry)  # Преобразуем в плоский вид
            formatted_entry = {}  # Словарь для одной отформатированной записи

            for key, value in flat_entry.items():  # Итерация по ключам и значениям
                columns.add(key)  # Добавляем ключ в множество колонок
                if isinstance(value, list):  # Если значение - список
                    if not value:  # Если список пустой
                        formatted_entry[key] = []  # Сохраняем как пустой список
                    elif all(isinstance(i, dict) for i in value):  # Если список словарей
                        # Преобразуем словари в кортежи, заменяя None на "NULL"
                        formatted_entry[key] = [tuple(item[k] if item[k] is not None else "NULL" for k in item.keys())
                                               for item in value]
                    else:  # Для остальных списков
                        # Заменяем None на "NULL" в элементах списка
                        formatted_entry[key] = [v if v is not None else "NULL" for v in value]
                else:  # Для всех остальных типов значений
                    formatted_entry[key] = value  # Сохраняем как есть
            formatted_data.append(formatted_entry)  # Добавляем запись в список

        columns = sorted(columns)  # Сортируем колонки для единообразия
        values = []  # Список для строк значений в SQL-запросе

        # Формирование строк значений для SQL
        for entry in formatted_data:  # Итерация по отформатированным записям
            row_values = []  # Список значений для одной строки
            for col in columns:  # Итерация по всем колонкам
                value = entry.get(col, None)  # Получаем значение или None
                if isinstance(value, str):  # Если значение - строка
                    escaped_value = escape_sql_string(value)  # Экранируем строку
                    row_values.append(f"'{escaped_value}'")  # Добавляем в кавычках
                elif value is None:  # Если значение - None
                    row_values.append("NULL")  # Добавляем как NULL
                elif isinstance(value, list):  # Если значение - список
                    # Преобразуем список в строку, обрабатывая вложенные кортежи
                    row_values.append(str([tuple("NULL" if v is None else v for v in item)
                                         if isinstance(item, tuple) else item
                                         for item in value]))
                else:  # Для всех остальных типов
                    row_values.append(str(value))  # Преобразуем в строку
            # Формируем строку значений в скобках
            values.append(f"({', '.join(row_values)})")

        # Формируем итоговый SQL-запрос для вставки
        query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES {', '.join(values)}"
        self.client.command(query)  # Выполняем запрос в ClickHouse


def main():
    """Основная функция для демонстрации работы с ClickHouse."""
    # Создаем экземпляр обработчика с указанием хоста и базы данных
    handler = ClickHouseJSONHandler(host='192.168.192.42', database='mart')
    table_name = 't_arr'  # Название таблицы

    # Пример JSON-данных
    json_data = [
        {"event": {"event_type": "update_issue_work_type", "old_type": {"code": "06",
                                                                        "name": "\u041d\u0435 \u043a\u043b\u0430\u0441\u0441\u0438\u0444\u0438\u0446\u0438\u0440\u043e\u0432\u0430\u043d\u043e"},
                   "new_type": {"code": "service",
                                "name": "\u041e\u0431\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u043d\u0438\u0435"},
                   "author": {"first_name": "Xeniya", "last_name": "Larionova", "patronymic": "",
                              "id": 13, "type": "employee"}}, "issue": {
            "title": "RE: \u043e\u0442\u043f\u0443\u0441\u043a \u0420\u0438\u0441\u0431\u0435\u043c\u0431\u0435\u0442\u043e\u0432",
            "planned_execution_in_hours": None, "id": 19734, "parent_id": None, "child_ids": [],
            "description": "<div class=\"WordSection1\"><p class=\"MsoNormal\"><span lang=\"KZ\">\u0414\u043e\u0431\u0440\u044b\u0439 \u0434\u0435\u043d\u044c, \u043f\u0440\u043e\u0448\u0443 \u0432\u0435\u0440\u043d\u0443\u0442\u044c \u0432\u0441\u0435 \u0437\u0430\u0434\u0430\u0447\u0438 \u043f\u043e \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u044e \u043e\u0442\u043f\u0443\u0441\u043a\u0430 \u043f\u043e \u042e\u0436\u043d\u044b\u043c \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043c \u041d\u0443\u0440\u0431\u043e\u043b\u0443 \u0410\u0443\u0431\u0430\u043a\u0438\u0440\u043e\u0432\u0438\u0447\u0443, \u043a\u043e\u0442\u043e\u0440\u044b\u0439 \u0431\u044b\u043b\u0438 \u0432\u0440\u0435\u043c\u0435\u043d\u043d\u043e \u0438\u0441\u043a\u043b\u044e\u0447\u0435\u043d\u044b \u043d\u0430 \u0432\u0440\u0435\u043c\u044f \u0435\u0433\u043e \u043e\u0442\u043f\u0443\u0441\u043a\u0430</span></p><p class=\"MsoNormal\"><span lang=\"KZ\">\u0421 \u0443\u0432\u0430\u0436\u0435\u043d\u0438\u0435\u043c,\u0421\u0430\u043b\u0442\u0430\u043d\u0430\u0442!</span></p><div><div style=\"border:none;border-top:solid #E1E1E1 1.0pt;padding:3.0pt 0cm 0cm 0cm\"><p class=\"MsoNormal\"><b><span lang=\"EN-US\" style='font-family:\"Calibri\",sans-serif;'>From:</span></b><span lang=\"EN-US\" style='font-family:\"Calibri\",sans-serif;'> Saltanat Ospanova<br><b>Sent:</b> Wednesday, March 5, 2025 10:16 AM<br><b>To:</b> helpdesk &lt;helpdesk@eurasia.kz&gt;; Lyubov Timchenko &lt;lyubov.timchenko@eurasia.kz&gt;; Sklad Kyzylorda &lt;sklad.kyzylorda@eurasia.kz&gt;<br><b>Cc:</b> Baurzhan Raimkulov &lt;baurzhan.raimkulov@eurasia.kz&gt;<br><b>Subject:</b> </span><span style='font-family:\"Calibri\",sans-serif;'>\u043e\u0442\u043f\u0443\u0441\u043a</span><span style='font-family:\"Calibri\",sans-serif;'></span><span style='font-family:\"Calibri\",sans-serif;'>\u0420\u0438\u0441\u0431\u0435\u043c\u0431\u0435\u0442\u043e\u0432</span><span lang=\"EN-US\" style='font-family:\"Calibri\",sans-serif;'></span></p></div></div><p class=\"MsoNormal\"><span lang=\"KZ\">\u0414\u043e\u0431\u0440\u044b\u0439 \u0434\u0435\u043d\u044c, \u043a\u043e\u043b\u043b\u0435\u0433\u0438!<br>\u0412 \u0441\u0432\u044f\u0437\u0438 \u0441 \u0442\u0435\u043c, \u0447\u0442\u043e \u0434\u0438\u0440\u0435\u043a\u0442\u043e\u0440 \u043f\u043e \u044e\u0436\u043d\u043e\u043c\u0443 \u0440\u0435\u0433\u0438\u043e\u043d\u0443 \u0411\u0430\u0439\u0437\u0438\u0440\u043e\u0432 \u041d.\u0410. \u043d\u0430\u0445\u043e\u0434\u0438\u0442\u0441\u044f \u0432 \u043e\u0442\u043f\u0443\u0441\u043a\u0435, \u043f\u0440\u043e\u0448\u0443 \u0438\u0441\u043a\u043b\u044e\u0447\u0438\u0442\u044c \u0435\u0433\u043e \u0432 \u0437\u0430\u0434\u0430\u0447\u0435 \u00ab\u043e\u0442\u043f\u0443\u0441\u043a\u00bb \u0432 \u0447\u0430\u0441\u0442\u0438 \u0441\u043e\u0433\u043b\u0430\u0441\u043e\u0432\u0430\u043d\u0438\u044f \u0434\u043e 07 \u043c\u0430\u0440\u0442\u0430 \u0432\u043a\u043b\u044e\u0447\u0438\u0442\u0435\u043b\u044c\u043d\u043e \u043f\u043e \u042e\u0436\u043d\u044b\u043c \u0440\u0435\u0433\u0438\u043e\u043d\u0430\u043c</span></p><p class=\"MsoNormal\"><span lang=\"KZ\">\u041b\u044e\u0431\u043e\u0432\u044c, \u043f\u0440\u043e\u0448\u0443 \u043f\u0440\u0438\u043d\u044f\u0442\u044c \u043f\u0440\u0438\u043a\u0430\u0437 \u043f\u043e \u043e\u0442\u043f\u0443\u0441\u043a\u0443 \u0432\u043e \u0432\u043b\u043e\u0436\u0435\u043d\u0438\u0438, \u0434\u043b\u044f \u0438\u0441\u043a\u043b\u044e\u0447\u0435\u043d\u0438\u044f \u043f\u0440\u043e\u0441\u0440\u043e\u0447\u0435\u043a \u043f\u043e \u0432\u044b\u043f\u043b\u0430\u0442\u0435</span></p><p class=\"MsoNormal\"><span lang=\"KZ\">\u0411\u043b\u0430\u0433\u043e\u0434\u0430\u0440\u044e!</span></p><p class=\"MsoNormal\"><span lang=\"KZ\">\u0416\u0430\u043d\u0431\u043e\u043b\u0430\u0442, \u0431\u04b1\u0439\u0440\u044b\u049b\u043f\u0435\u043d \u0442\u0430\u043d\u044b\u0441\u044b\u043f, \u049b\u043e\u043b \u049b\u043e\u0439\u044b\u043f \u0410\u0441\u0442\u0430\u043d\u0430\u0493\u0430 \u043c\u0435\u043d\u0456\u04a3 \u0430\u0442\u044b\u043c\u0430 \u0436\u0456\u0431\u0435\u0440\u0443\u0456\u04a3\u0456\u0437\u0434\u0456 \u0441\u04b1\u0440\u0430\u0439\u043c\u044b\u043d</span></p><p class=\"MsoNormal\"><span lang=\"KZ\">\u0420\u0430\u0445\u043c\u0435\u0442!</span></p><p class=\"MsoNormal\"><span lang=\"KZ\" style='font-size:12.0pt;font-family:\"Calibri\",sans-serif;'>\u0421 \u0443\u0432\u0430\u0436\u0435\u043d\u0438\u0435\u043c,</span></p><p class=\"MsoNormal\"><span><img width=\"460\" height=\"269\" style=\"width:4.7916in;height:2.8in\" id=\"\u0420\u0438\u0441\u0443\u043d\u043e\u043a_x0020_2\" src=\"/issues/19734/attachments/35367045\"></span><span lang=\"KZ\" style=\"font-size:12.0pt;\"></span></p></div>",
            "type": {"code": "service",
                     "name": "\u041e\u0431\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u043d\u0438\u0435",
                     "inner": False}, "priority": {"code": "low", "name": "\u041d\u0438\u0437\u043a\u0438\u0439"},
            "status": {"code": "opened", "name": "\u0412 \u043e\u0447\u0435\u0440\u0435\u0434\u0438"}, "rate": None,
            "old_status": None, "client": {"company": {"name": "\u0422\u041e\u041e Eurasia Group Kazakhstan", "id": 3},
                                           "contact": {"first_name": "Saltanat", "last_name": "Ospanova",
                                                       "patronymic": None, "id": 3082}}, "agreement": None,
            "maintenance_entity": None, "equipments": [],
            "author": {"first_name": "Saltanat", "last_name": "Ospanova", "patronymic": None, "id": 3082,
                       "type": "contact"}, "assignee": {
                "group": {"name": "SAP \u043f\u0435\u0440\u0432\u0430\u044f \u043b\u0438\u043d\u0438\u044f", "id": 1},
                "employee": {"first_name": "Xeniya", "last_name": "Larionova", "patronymic": "", "id": 13}},
            "coexecutors": [], "observers": {"employees": [], "contacts": [
                {"first_name": "Nurbol", "last_name": "Baizirov", "patronymic": None, "id": 3193}], "groups": []},
            "created_at": "2025-03-11T10:21:26.480+05:00", "deadline_at": "2025-03-12T09:21:27.000+05:00",
            "planned_reaction_at": "2025-03-11T12:21:00.000+05:00", "start_execution_until": None, "completed_at": None,
            "reacted_at": None, "parameters": [{"code": "A",
                                                "name": "\u0425\u0430\u0440\u0430\u043a\u0442\u0435\u0440 \u0437\u0430\u0434\u0430\u0447\u0438",
                                                "type": "ftselect", "value": None},
                                               {"code": "tag3", "name": "\u0422\u044d\u0433\u0438",
                                                "type": "ftmultiselect",
                                                "value": None}], "attachments": [
                {"id": 35367045, "is_public": True, "attachment_file_name": "image001.png", "description": None,
                 "attachment_file_size": 28242, "created_at": "2025-03-11T10:21:26.827+05:00"}]}}
    ]

    # Определяем структуру таблицы на основе JSON
    structure = handler.infer_table_structure(json_data)
    # Создаем таблицу в ClickHouse
    handler.create_table(table_name, structure)
    # Вставляем данные в таблицу
    handler.insert_json_data(table_name, json_data)
    print("Данные успешно вставлены в ClickHouse")  # Сообщение об успехе


if __name__ == "__main__":
    main()  # Запуск основной функции при выполнении скрипта