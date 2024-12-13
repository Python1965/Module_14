# Домашнее задание по теме "Написание примитивной ORM"
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.9.13
#   Aiogram версии 2.25.1+ 
#
# Задача "Регистрация покупателей":
# Подготовка:
# Для решения этой задачи вам понадобится код из предыдущей задачи. Дополните его, следуя пунктам задачи ниже.
#
# Дополните файл crud_functions.py, написав и дополнив в нём следующие функции:
#   1. initiate_db дополните созданием таблицы Users, если она ещё не создана при помощи SQL запроса.
#       Эта таблица должна содержать следующие поля:
#           2. id - целое число, первичный ключ
#           3. username - текст (не пустой)
#           4. email - текст (не пустой)
#           5. age - целое число (не пустой)
#           5. balance - целое число (не пустой)
#
#   2. add_user(username, email, age), которая принимает: имя пользователя, почту и возраст.
#              Данная функция должна добавлять в таблицу Users вашей БД запись с переданными данными.
#              Баланс у новых пользователей всегда равен 1000. Для добавления записей в таблице используйте
#              SQL запрос.
#
#   3. is_included(username) принимает имя пользователя и возвращает True, если такой пользователь
#              есть в таблице Users, в противном случае False. Для получения записей используйте SQL запрос.
#
# Изменения в Telegram-бот:
#   1. Кнопки главного меню дополните кнопкой "Регистрация".
#   2. Напишите новый класс состояний RegistrationState со следующими объектами класса State:
#      username, email, age, balance(по умолчанию 1000).
#   3. Создайте цепочку изменений состояний RegistrationState.
#
# Фукнции цепочки состояний RegistrationState:
#   1. sing_up(message):
#       - Оберните её в message_handler, который реагирует на текстовое сообщение 'Регистрация'.
#       - Эта функция должна выводить в Telegram-бот сообщение "Введите имя пользователя
#         (только латинский алфавит):".
#       - После ожидать ввода имени в атрибут RegistrationState.username при помощи метода set.
#
#   2. set_username(message, state):
#       - Оберните её в message_handler, который реагирует на состояние RegistrationState.username.
#       - Если пользователя message.text ещё нет в таблице, то должны обновляться данные в состоянии
#         username на message.text. Далее выводится сообщение "Введите свой email:" и принимается
#         новое состояние RegistrationState.email.
#       - Если пользователь с таким message.text есть в таблице, то выводить "Пользователь существует,
#         введите другое имя" и запрашивать новое состояние для RegistrationState.username.
#
#   3 set_email(message, state):
#       - Оберните её в message_handler, который реагирует на состояние RegistrationState.email.
#       - Эта функция должна обновляться данные в состоянии RegistrationState.email на message.text.
#       - Далее выводить сообщение "Введите свой возраст:":
#       - После ожидать ввода возраста в атрибут RegistrationState.age.
#
#   4. set_age(message, state):
#       - Оберните её в message_handler, который реагирует на состояние RegistrationState.age.
#       - Эта функция должна обновляться данные в состоянии RegistrationState.age на message.text.
#       - Далее брать все данные (username, email и age) из состояния и записывать в таблицу Users
#         при помощи ранее написанной crud-функции add_user.
#       - В конце завершать приём состояний при помощи метода finish().
#
# Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода
# в чате Telegram-бота.
# *****************************************************************************************************************

from aiogram import Bot, Dispatcher,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions_14_5 import *


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# ------ Маркап клавиатура (главное меню)----------------
kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Рассчитать'),
            KeyboardButton(text='Регистрация')
        ],
            [KeyboardButton(text='Купить')]
    ],resize_keyboard=True
)


#-------- Инлайн клавиатуры (для колорий)----------------
kb2 = InlineKeyboardMarkup(resize_keyboard=True) # расчёт калорий человека
in_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

kb2.add(in_button1)
kb2.add(in_button2)

#-------- Инлайн клавиатурa (для покупок)----------------
kb3 = InlineKeyboardMarkup(
    inline_keyboard=[
        [
InlineKeyboardButton(text='Продукт1', callback_data='product_buying'),
InlineKeyboardButton(text='Продукт2', callback_data='product_buying'),
InlineKeyboardButton(text='Продукт3', callback_data='product_buying'),
InlineKeyboardButton(text='Продукт4', callback_data='product_buying')
        ]
],resize_keyboard=True
)


class RegistrationState(StatesGroup):
    username = State()
    email = State()
    age = State()
    balance = 1000

class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот помогающий твоему здоровью.', reply_markup=kb)

@dp.message_handler(text='Информация')
async def inform(message):
    await message.answer('На текущий момент я пока только могу рассчитать необходимое количество килокалорий (ккал) '
                         'в сутки для каждого конкретного человека. \n По формулуe Миффлина-Сан Жеора, разработанной '
                         'группой американских врачей-диетологов под руководством докторов Миффлина и Сан Жеора. \n'
                         'А ещё пробую создать меню покупок продуктов для здоровья')

@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb2)

@dp.callback_query_handler(text='formulas')
async def get_formulas(call):
    await call.message.answer('для мужчин: 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5;'
                              '\nдля женщин: 10 x вес (кг) + 6,25 x рост (см) – 5 x возраст (г) – 161')
    await call.answer()

@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Данные необходимо вводить целыми числами')
    await call.message.answer('Введите свой возраст:')
    await call.answer()
    await UserState.age.set()

@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(age=message.text)
    await message.answer('Введите свой рост:')
    await UserState.growth.set()

@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(growth=message.text)
    await message.answer('Введите свой вес:')
    await UserState.weight.set()

@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(weight=message.text)
    data = await state.get_data()
    mans = (10*int(data['weight'])+6.25*int(data['growth'])-5*int(data['age'])+5)
    wumans = (10 * int(data['weight']) + 6.25 * int(data['growth']) - 5 * int(data['age']) - 161)
    await message.answer(f'При таких параметрах норма калорий: \nдля мужчин {mans} ккал в сутки \nдля женщин {wumans} ккал в сутки')
    await UserState.weight.set()
    await state.finish()

@dp.message_handler(text='Купить')
async def get_buying_list(message):
    for i in get_all_products():
        number = i[0]
        title = i[1]
        description = i[2]
        price = i[3]
        with open (f'{str(number) + ".png"}', 'rb') as img:
            await message.answer_photo(img, caption=f'Название: {title} | Описание: {description} | Цена: {price}')

    await message.answer(text='Выберите продукт для покупки: ', reply_markup=kb3)

@dp.callback_query_handler(text='product_buying')
async def send_confirm_message(call):
    await call.message.answer(text='Вы успешно приобрели продукт!')
    await call.answer()


# ---------------- Регистрация пользователя -------------------
@dp.message_handler(text="Регистрация")
async def sing_up(message):
    await message.answer("Введите имя пользователя (только латинский алфавит):")
    await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.username)
async def set_username(message, state):
    await state.update_data(username=message.text)
    data = await state.get_data()

    name = is_included(data['username'])
    if name is True:
        await state.update_data(username=message.text)
        await message.answer("Введите свой email:")
        await RegistrationState.email.set()
    else:
        await message.answer("Пользователь существует, введите другое имя")
        await RegistrationState.username.set()

@dp.message_handler(state=RegistrationState.email)
async def set_email(message, state):
    await state.update_data(email=message.text)
    await message.answer("Введите свой возраст:")
    await RegistrationState.age.set()

@dp.message_handler(state=RegistrationState.age)
async def set_age(message, state):
    await state.update_data(age=message.text)
    data = await state.get_data()
    # print(data)
    add_user(data['username'], data['email'], data['age'])
    await message.answer("Регистрация прошла успешно!")
    await state.finish()

@dp.message_handler()
async def all_message(message):
   await message.answer('Введите команду /start, чтобы начать общение.')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)