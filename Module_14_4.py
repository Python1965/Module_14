# Домашнее задание по теме "План написания админ панели"
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.9.13
#   Aiogram версии 2.25.1
#
# Задача "Продуктовая база":
#
# Подготовка. Для решения этой задачи вам понадобится код из предыдущей задачи.
# Дополните его, следуя пунктам задачи ниже.
#
# Создайте файл crud_functions.py и напишите там следующие функции:
#
#   - initiate_db, которая создаёт таблицу Products, если она ещё не создана при помощи SQL запроса.
#     Эта таблица должна содержать следующие поля:
#           1. id - целое число, первичный ключ
#           2. title(название продукта) - текст (не пустой)
#           3. description(описание) - текст
#           4.price(цена) - целое число (не пустой)
#
#   - get_all_products, которая возвращает все записи из таблицы Products, полученные при помощи SQL запроса.
#
# Изменения в Telegram-бот:
#   1. В самом начале запускайте ранее написанную функцию get_all_products.
#   2. Измените функцию get_buying_list в модуле с Telegram-ботом, используя вместо обычной нумерации продуктов
#      функцию get_all_products. Полученные записи используйте в выводимой надписи:
#      "Название: <title> | Описание: <description> | Цена: <price>"
#
# Перед запуском бота пополните вашу таблицу Products 4 или более записями для последующего вывода
# в чате Telegram-бота.
# *****************************************************************************************************************

from aiogram import Bot, Dispatcher,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

from crud_functions import get_all_products


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())


# ------ Маркап клавиатура (главное меню)----------------
kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Информация'),
            KeyboardButton(text='Рассчитать')
        ],
            [KeyboardButton(text='Купить')]
    ],resize_keyboard=True
)


#-------- Инлайн клавиатуры (для колорий)----------------
kb2 = InlineKeyboardMarkup()
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
                         'Погнали!? - жми кнопку Рассчитать')

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

@dp.message_handler()
async def all_message(message):
   await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)