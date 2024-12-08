# Домашнее задание по теме "Создание БД, добавление, выбор и удаление элементов."
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.11
#
# Задача "Первые пользователи":
#
# Создайте файл базы данных not_telegram.db и подключитесь к ней, используя встроенную библиотеку sqlite3.
# Создайте объект курсора и выполните следующие действия при помощи SQL запросов:
# Создайте таблицу Users, если она ещё не создана. В этой таблице должны присутствовать следующие поля:
#
#   1. id - целое число, первичный ключ
#   2. username - текст (не пустой)
#   3. email - текст (не пустой)
#   4. age - целое число
#   5. balance - целое число (не пустой)
#
# Заполните её 10 записями:
# User1, example1@gmail.com, 10, 1000
# User2, example2@gmail.com, 20, 1000
# User3, example3@gmail.com, 30, 1000
# ...
# User10, example10@gmail.com, 100, 1000
# Обновите balance у каждой 2ой записи начиная с 1ой на 500:
# User1, example1@gmail.com, 10, 500
# User2, example2@gmail.com, 20, 1000
# User3, example3@gmail.com, 30, 500
# ...
# User10, example10@gmail.com, 100, 1000
# Удалите каждую 3ую запись в таблице начиная с 1ой:
# User2, example2@gmail.com, 20, 1000
# User3, example3@gmail.com, 30, 500
# User5, example5@gmail.com, 50, 500
# ...
# User9, example9@gmail.com, 90, 500
#
# Сделайте выборку всех записей при помощи fetchall(), где возраст не равен 60 и выведите их в консоль в следующем формате (без id):
# Имя: <username> | Почта: <email> | Возраст: <age> | Баланс: <balance>
# *****************************************************************************************************************

import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS Users(
id INTEGER PRIMARY KEY,
username TEXT NOT NULL,
email TEXT NOT NULL,
age INTEGER,
balance INTEGER NOT NULL
)
''')

# ----------------- Добавление информации в базу данных ------------
for n in range(1,11):
    cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', (f'User{n}', f'example{n}@gmail.com', f'{n*10}', '1000'))

# ----------------- Изменение данных в базе данных -----------------
for i in range(1, 11, 2):
    cursor.execute('UPDATE Users SET balance = ? WHERE username = ?', (500 , f'User{i}'))

# ----------------- Удаление данных из БД -------------------------
for i in range(1, 11, 3):
    cursor.execute('DELETE FROM Users WHERE username = ?', (f'User{i}', ))

# ----------------- Выборка данных из БД ------------------------
cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != ?', (60,))
users = cursor.fetchall()
for user in users:
    print(f'Имя:{user[0]} | Почта:{user[1]} | Возраст:{user[2]} | Баланс:{user[3]}')


# cursor.execute('SELECT * FROM Users')
# users = cursor.fetchall()
# for user in users:
#     print(f'username:{user[1]} | email:{user[2]} | age:{user[3]} | balance:{user[4]}')

connection.commit()
connection.close()