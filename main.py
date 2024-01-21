from aiogram import Bot, Dispatcher, executor, types
from database import Database
from aiogram.dispatcher.filters.state import StatesGroup, State
import time
import aioschedule
import asyncio

db = Database("DataBase/databasee")

API_TOKEN = '6848839856:AAHmIXbflA5egxD1KfeFOTqLzT52CnLAWbQ'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


class ProfileStatesGroup(StatesGroup):
    name = State()
    age = State()


@dp.message_handler(commands=['start'])
async def send_birthday(message: types.Message):
    await message.reply("Привет!\nСоздать свой профиль - напишите /name [ВАШЕ ИМЯ]")
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
    else:
        print('такой есть уже')


@dp.message_handler(commands=['name'])
async def cmd_create(message: types.Message) -> None:
    text = message.text[6:]
    db.add_name(text, message.from_user.id)
    await message.reply("Ваше имя добавлено. Напишите /age [ДЕНЬ.МЕСЯЦ.ГОД](13.05.99), чтобы добавить дату рождения")


@dp.message_handler(commands=['age'])
async def cmd_create(message: types.Message) -> None:
    text = message.text[5:]
    db.add_birthday(text, message.from_user.id)

    await message.reply('Ваш анкета успешно создана')


@dp.message_handler(commands=['test'])
async def test(message: types.Message) -> None:
    t = time.localtime()
    current_time = time.strftime("%D", t)
    current_time = current_time.split('/')
    current_time = '.'.join([current_time[1], current_time[0], current_time[2]])
    # print(current_time)
    for i in db.get_users():
        if current_time[:-2] == i[1][:-2]:
            await bot.send_message('-4169425553', text=f'S DR, @{message.from_user.username}')


async def on_startup(x):
    asyncio.create_task(scheduler())


async def scheduler():
    print('zawel')
    aioschedule.every().minute.do(test)
    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


@dp.message_handler(commands="mailing")
async def mailing(mes):
    user_id = mes.from_user.id
    if user_id == 612485708:  # Тут id того, кому можно выполнять команду рассылки
        await test()


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
