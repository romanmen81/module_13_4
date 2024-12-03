from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Определяем класс состояний
class UserState(StatesGroup):
    age = State()     # Состояние для ввода возраста
    growth = State()  # Состояние для ввода роста
    weight = State()  # Состояние для ввода веса

# Инициализация бота и диспетчера
bot = Bot(token='Ваш TOKEN')
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Функция для получения возраста
@dp.message_handler(commands=['Calories'])
async def set_age(message: types.Message):
    logging.info("Команда /Calories получена.")
    await message.answer('Введите свой возраст:')
    await UserState.age.set()  # Установка состояния age

# Функция для получения роста
@dp.message_handler(state=UserState.age)
async def set_growth(message: types.Message, state: FSMContext):
    await state.update_data(age=message.text)  # Сохранение возраста
    await message.answer('Введите свой рост:')
    await UserState.growth.set()  # Установка состояния growth

# Функция для получения веса
@dp.message_handler(state=UserState.growth)
async def set_weight(message: types.Message, state: FSMContext):
    await state.update_data(growth=message.text)  # Сохранение роста
    await message.answer('Введите свой вес:')
    await UserState.weight.set()  # Установка состояния weight

# Функция для вычисления нормы калорий
@dp.message_handler(state=UserState.weight)
async def send_calories(message: types.Message, state: FSMContext):
    await state.update_data(weight=message.text)  # Сохранение веса
    data = await state.get_data()  # Получение всех данных
    age = int(data['age'])  # Извлечение возраста
    growth = int(data['growth'])  # Извлечение роста
    weight = int(data['weight'])  # Извлечение веса

    # Формула Миффлина - Сан Жеора для мужчин (можно использовать для женщин в зависимости от предпочтений)
    calories = 10 * weight + 6.25 * growth - 5 * age + 5  # Формула для мужчин

    await message.answer(f'Ваша норма калорий: {calories} калорий в день.')  # Ответ пользователю
    await state.finish()  # Завершение состояния

# Запуск бота
async def on_startup(dp):
    logging.info('Бот запущен!')

if __name__ == '__main__':
    executor.start_polling(dp, on_startup=on_startup)
