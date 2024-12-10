# Домашнее задание по теме "Доработка бота"
# *****************************************************************************************************************
# Исользуются
#   Python версии 3.9.13
#   Aiogram версии 2.25.1
#
# Задача "Витамины для всех!":
#
# Подготовка. Подготовьте Telegram-бота из последнего домашнего задания 13 модуля
# сохранив код с ним  в файл module_14_3.py.
#
# Дополните ранее написанный код для Telegram-бота:
#
# Создайте и дополните клавиатуры:
#   1. В главную (обычную) клавиатуру меню добавьте кнопку "Купить".
#   2. Создайте Inline меню из 4 кнопок с надписями "Product1", "Product2", "Product3", "Product4".
#      У всех кнопок назначьте callback_data="product_buying"
#
# Создайте хэндлеры и функции к ним:
#   1. Message хэндлер, который реагирует на текст "Купить" и оборачивает функцию get_buying_list(message).
#   2. Функция get_buying_list должна выводить надписи
#      'Название: Product<number> | Описание: описание <number> | Цена: <number * 100>' 4 раза.
#      После каждой надписи выводите картинки к продуктам. В конце выведите ранее созданное
#      Inline меню с надписью "Выберите продукт для покупки:".
#   3. Callback хэндлер, который реагирует на текст "product_buying" и оборачивает
#      функцию send_confirm_message(call).
#   4. Функция send_confirm_message, присылает сообщение "Вы успешно приобрели продукт!"
#
# Примечание: Название продуктов и картинок к ним можете выбрать самостоятельно. (Минимум 4)
# *****************************************************************************************************************

from aiogram import Bot, Dispatcher,executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


api = ''
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

# ------ Маркап клавиатура (с кнопками)----------------
kb = ReplyKeyboardMarkup(resize_keyboard=True)
button = KeyboardButton(text='Информация')
button2 = KeyboardButton(text='Рассчитать')
button3 = KeyboardButton(text='Купить')
kb.row(button)
kb.row(button2)
kb.add(button3)

#-------- Инлайн клавиатуры (с кнопками)----------------
kb2 = InlineKeyboardMarkup()
in_button1 = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
in_button2 = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')

kb2.add(in_button1)
kb2.add(in_button2)
kb3 = InlineKeyboardMarkup(resize_keyboard=True) # покупка продукта

in_button3 = InlineKeyboardButton(text='Продукт1', callback_data='product_buying')
in_button4 = InlineKeyboardButton(text='Продукт2', callback_data='product_buying')
in_button5 = InlineKeyboardButton(text='Продукт3', callback_data='product_buying')
in_button6 = InlineKeyboardButton(text='Продукт4', callback_data='product_buying')

kb3.add(in_button3)
kb3.row(in_button4)
kb3.row(in_button5)
kb3.row(in_button6)

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
    for i in range(4):
        number = i + 1
        await message.answer(f'Название: Product{number} | Описание: описание{number} | Цена: {number*100}')
        with open (f'{str(number) + ".png"}', 'rb') as img:
            await message.answer_photo(img)

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