# Домашнее задание по теме "Выбор элементов и функции в SQL запросах"
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.11
#
# Задача "Средний баланс пользователя":
#
# Для решения этой задачи вам понадобится решение предыдущей.
# Для решения необходимо дополнить существующий код:
#
#   1. Удалите из базы данных not_telegram.db запись с id = 6.
#   2. Подсчитать общее количество записей.
#   3. Посчитать сумму всех балансов.
#   4. Вывести в консоль средний баланс всех пользователей.
# *****************************************************************************************************************

import sqlite3

connection = sqlite3.connect('not_telegram.db')
cursor = connection.cursor()

# cursor.execute('''
# CREATE TABLE IF NOT EXISTS Users(
# id INTEGER PRIMARY KEY,
# username TEXT NOT NULL,
# email TEXT NOT NULL,
# age INTEGER,
# balance INTEGER NOT NULL
# )
# ''')
#
# # ----------------- Добавление информации в базу данных ------------
# for n in range(1,11):
#     cursor.execute('INSERT INTO Users (username, email, age, balance) VALUES (?, ?, ?, ?)', (f'User{n}', f'example{n}@gmail.com', f'{n*10}', '1000'))
#
# # ----------------- Изменение данных в базе данных -----------------
# for i in range(1, 11, 2):
#     cursor.execute('UPDATE Users SET balance = ? WHERE username = ?', (500 , f'User{i}'))
#
# # ----------------- Удаление данных из БД -------------------------
# for i in range(1, 11, 3):
#     cursor.execute('DELETE FROM Users WHERE username = ?', (f'User{i}', ))
#
# # ----------------- Выборка данных из БД ------------------------
# cursor.execute('SELECT username, email, age, balance FROM Users WHERE age != ?', (60,))
# users = cursor.fetchall()
# for user in users:
#     print(f'Имя:{user[0]} | Почта:{user[1]} | Возраст:{user[2]} | Баланс:{user[3]}')

# ---------------- Удаление строки по условиюиз БД --------------
cursor.execute('DELETE FROM Users WHERE id = ?', (6,))

# # ---------------- Подсчёт количества записей в БД -----------------
cursor.execute('SELECT COUNT(*) FROM Users')
total = cursor.fetchone()[0]
# print(total)

# ---------------- Подсчёт суммы балансов в БД -----------------
cursor.execute('SELECT SUM(balance) FROM Users')
total2 = cursor.fetchone()[0]
# print(total2)

# ---------------- Средний баланс пользователей в БД -----------------
cursor.execute('SELECT AVG(balance) FROM Users')
total3 = cursor.fetchone()[0]
# print(total3) # средняя сумма через встроенную функцию
print(total2/total) # средняя сумма через вычисление по предыдущим итогам

# cursor.execute('SELECT * FROM Users')
# users = cursor.fetchall()
# for user in users:
#     print(f'username:{user[1]} | email:{user[2]} | age:{user[3]} | balance:{user[4]}')


connection.commit()
connection.close()