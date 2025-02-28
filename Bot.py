from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message
import random
import pickle

def Save():
    with open('info.pickle', 'wb') as file:
         pickle.dump(users, file)


BOT_TOKEN = " PASTE TOKEN "

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

users = {}

with open('info.pickle', 'rb') as file:
    users = pickle.load(file)



def random_num() -> int:
    return random.randint(1, 100)


@dp.message(Command(commands='start'))
async def send_message_start(message: Message):
    await message.answer('Привет!\nДавай сыграем в игру "Угадай число"?\n\n'
    'Чтобы получить правила игры и список доступных '
        'команд - отправьте команду /help')

    if message.from_user.id not in users:
            users[message.from_user.id] = {
                'in_game': False,
                'secret_number': None,
                'attemps': 5,
                'total_games': 0,
                'wins': 0,
                'settings': False,
                'ATTEMPS': 1
            }
            Save()

@dp.message(Command(commands='help'))
async def send_message_help(message: Message):
    await message.answer('Правила игры:\n\nЯ загадываю число от 1 до 100, '
        f'а вам нужно его угадать\nУ тебя есть 5 '
        'попыток по умолчанию, но это можно изменить.\n\nДоступные команды:\n/start - если возникли проблемы\n\n/help - правила '
        'игры и список команд\n\n/cancel - выйти из игры\n\n'
        '/stat - посмотреть статистику\n\n/play - начать игру \n\n/attemps - изменить количество попыток\n\nДавай сыграем?')


@dp.message(Command(commands='stat'))
async def send_message_stat(message: Message):
    await message.answer(
        f'Всего игр сыграно: {users[message.from_user.id]["total_games"]}\n'
        f'Игр победных {users[message.from_user.id]["wins"]}'
    )


@dp.message(Command(commands='attemps'))
async def send_setting_message(message: Message):
        users[message.from_user.id]['settings'] = True
        await message.answer('Введите количество попыток от 2 до 10')

@dp.message(lambda x: x.text and x.text.isdigit() and users[x.from_user.id]['settings'])
async def swap_attemps(message: Message):
    if 2<=int(message.text)<=10:
        users[message.from_user.id]["attemps"] = int(message.text)
        users[message.from_user.id]['settings'] = False
        await message.answer(f'Количество попыток успешно изменено!\n'
                            f'Количество попыток равно {users[message.from_user.id]["attemps"]}\n\n'
                            'Сыграем?:)'
                            )
        Save()
    
    else:
        await message.answer('Пожалуйста введите от 2 до 10(БЕЗ ТОЧЕК!)')
    


@dp.message(Command(commands='cancel'))
async def send_message_cancel(message:Message):
    if users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = False
        await message.answer(
            'Вы вышли из игры. Если захотите сыграть '
            'снова - напишите об этом'
        )
    else:
        await message.answer(
            'Мы не в игре, ты чё  '
            'Может, сыграем разок?:)'
        )

@dp.message(F.text.lower().in_(['да','да.', 'ок.', 'ок', 'давай','гоу', 'хочу играть', 'сыграем', '/play']))
async def send_message_positive(message:Message):
    if not users[message.from_user.id]['in_game']:
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = random_num()
        users[message.from_user.id]['ATTEMPS'] = 1
        await message.answer(
            'Ну поехали!\n\nЯ загадал число от 1 до 100, '
            'попробуй угадать! Не угадаешь, то ты бот, а не я :)) \n\n'
            f'Ваше количество попыток {users[message.from_user.id]["attemps"]}\n\n'
            'Попытка номер 1. Удачи!'
            )
    else:
        await message.answer(
            'Пока мы играем в игру я могу '
            'реагировать только на числа от 1 до 100 '
            'и команды /cancel и /stat')
    Save()

@dp.message(F.text.lower().in_(['нет', 'не', 'не хочу', 'не буду']))
async def send_message_negative(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer(
            'Ну и бот, иди занимайся человеческими делами\n'
            'А если ты не Саня и всё таки хочешь сыграть то скажи об'
            'этом "Например так: хочу играть"'
        )
    else:
        await message.answer(
            'Мы же сейчас с вами играем. Присылайте, '
            'пожалуйста, числа от 1 до 100'
        )

@dp.message(lambda x: x.text and
            x.text.isdigit() and
            1 <= int(x.text) <= 100)
async def play_process(message: Message):
    
    if users[message.from_user.id]['in_game']:
        if int(message.text)==users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            users[message.from_user.id]['wins'] += 1
            await message.answer(
                'Поздравляю ты победил!!!\n'
                'Ещё каточку?'
            )
        elif users[message.from_user.id]["ATTEMPS"] == users[message.from_user.id]["attemps"]:
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
            await message.answer(
                'К сожалению, у вас больше не осталось '
                'попыток. Вы проиграли вы бот -_-\n\nМое число '
                f'было {users[message.from_user.id]["secret_number"]}\n\nДавайте '
                'сыграем еще?'
            )
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            users[message.from_user.id]['ATTEMPS'] += 1
            await message.answer('Мое число меньше\n'
            f'Попыткa номер {users[message.from_user.id]["ATTEMPS"]}')
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            users[message.from_user.id]["ATTEMPS"] += 1
            await message.answer('Мое число больше\n'
            f'Попыткa номер {users[message.from_user.id]["ATTEMPS"]}')       
    else:
        await message.answer('Мы еще не играем. Хотите сыграть?')

@dp.message()
async def send_other_massage(message:Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Ну и кто тут не человек?\n'
        'Мы в игре если забыл((\n'
        'Присылай число от 1 до 100 пожалуйста')
    else:
        await message.answer(
            'Такому я ещё не научился, давай '
            'просто сыграем в игру?'
        )

if __name__ =='__main__':
    dp.run_polling(bot)