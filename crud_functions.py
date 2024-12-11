# Дополнение к Module_14_4.py
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.9.13
#   Aiogram версии 2.25.1
#
# Содержит функции:
#   - initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса.
#     Эта таблица должна содержать следующие поля:
#           1. id - целое число, первичный ключ
#           2. title(название продукта) - текст (не пустой)
#           3. description(описание) - текст
#           4.price(цена) - целое число (не пустой)
#
#   - get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.
# *****************************************************************************************************************

import sqlite3

def initiate_db():
    connection = sqlite3.connect('DB_Product_module_14_4.db')
    cursor = connection.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Products(
    id INT PRIMARY KEY,
    title TEXT NOT NULL,
    description TEXT,
    price INT NOT NULL
    );
    ''')

    connection.commit()
    connection.close()

def check_db(id, title, description, price):
    connection = sqlite3.connect('DB_Product_module_14_4.db')
    cursor = connection.cursor()

    check_db = cursor.execute('SELECT * FROM Products WHERE title=?', (title,))

    if check_db.fetchone() is None:
        cursor.execute(f'''
    INSERT INTO Products (id, title, description, price) VALUES('{id}', '{title}', '{description}', '{price}')
''')
    connection.commit()
    connection.close()

def get_all_products():
    connection = sqlite3.connect('DB_Product_module_14_4.db')
    cursor = connection.cursor()

    cursor.execute('SELECT * FROM Products WHERE id > ?', (0,))
    return cursor.fetchall()

    connection.commit()
    connection.close()


if __name__ == '__main__':
    initiate_db()
    check_db(1,'Продукт 1', 'описание 1', 100)
    check_db(2,'Продукт 2', 'описание 2', 200)
    check_db(3,'Продукт 3', 'описание 3', 300)
    check_db(4, 'Продукт 4', 'описание 4', 400)


