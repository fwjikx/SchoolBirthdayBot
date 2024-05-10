from aiogram import Bot, Dispatcher, executor, types
from database import Database
from aiogram.dispatcher.filters.state import StatesGroup, State
import time
import aioschedule
import asyncio

db = Database("DataBase/databasee")

API_TOKEN = '7016382315:AAHed1BgEc23aiwm6PXewHViZtZ__j5o_aE'
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


class ProfileStatesGroup(StatesGroup):
    name = State()
    age = State()


@dp.message_handler(commands=['start'])
async def send_birthday(message: types.Message):
    await message.reply("Привет!\nСоздать свой профиль - напишите /name ВАШЕ ИМЯ")
    try:
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        else:
            print('такой есть уже')
    except Exception as e:
        print(e, 'send_birthday')


@dp.message_handler(commands=['name'])
async def cmd_create(message: types.Message) -> None:
    try:
        text = message.text[6:]
        print(text)
        db.add_name(text, message.from_user.id)
        await message.reply(
            "Ваше имя добавлено. Напишите /age ДЕНЬ.МЕСЯЦ.ГОД - 13.05.99, чтобы добавить дату рождения")
    except Exception as e:
        print(e, 'cmd_create')


@dp.message_handler(commands=['age'])
async def cmd_create(message: types.Message) -> None:
    print('fsa')
    try:
        flag = False
        text = message.text[5:]
        if len(text) != 8:
            flag = True
        elif int(text[3:5]) not in list(range(1, 13)):
            flag = True
        elif int(text[0:2]) not in list(range(1, 32)):
            flag = True
        if flag:
            await message.reply('Неккоректно введена дата')
        else:
            db.add_birthday(text, message.from_user.id)
            print(text, message.from_user.id)

            await message.reply('Ваш анкета успешно создана')
    except Exception as e:
        print(e, 'cmd_create')


@dp.message_handler()
async def test():
    try:
        print('ZAWEL V TEST')
        t = time.localtime()
        current_time = time.strftime("%D", t)
        current_time = current_time.split('/')
        current_time = '.'.join([current_time[1], current_time[0], current_time[2]])
        # print(current_time)
        for i in db.get_users():
            print(i)
            if current_time[:-2] == i[1][:-2]:
                await bot.send_message('-4173593040', text=f'S DR {i[-1]}')
    except Exception as e:
        print(e, 'test')


@dp.message_handler(commands="mailing")
async def mailing(mes):
    try:
        user_id = mes.from_user.id
        if user_id == 612485708:  # Тут id того, кому можно выполнять команду рассылки
            await test()
    except Exception as e:
        print(e, 'mailing')


async def scheduler():
    try:
        print('zawel!')
        aioschedule.every().day.at('13:40').do(test)  # Тут говорим, что рассылка будет раз в день, отсчет начинается с момента запуска кода
        while True:
            await aioschedule.run_pending()
            await asyncio.sleep(1)
    except Exception as e:
        print(e, 'scheduler')


async def on_startup(x):
    asyncio.create_task(scheduler())


@dp.message_handler(commands="start")
async def start(mes):
    user_id = mes.from_user.id
    await mes.answer("Привет! Тут ты будешь получать рассылку.")
    # new_user(user_id)


@dp.message_handler(commands="mailing")
async def mailing(mes):
    try:
        user_id = mes.from_user.id
        if user_id == 612485708:  # Тут id того, кому можно выполнять команду рассылки
            await test()
    except Exception as e:
        print(e, 'mailing')


if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
