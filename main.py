#!/usr/bin/env python
# -*- coding: utf-8 -*-

from aiogram.dispatcher import FSMContext
from aiogram.utils.markdown import hlink
from aiogram.types import \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from Stater import *
from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
import pandas as pd
import matching as p2

bot = Bot(token='2118596990:AAHQaoEahd5ty9ziRjfNiImVSg7y5nnJIpo', parse_mode='html')
dp = Dispatcher(bot, storage=MemoryStorage())

r = open('rules.txt','r',encoding='utf-8')
rules_text = ''.join(r.readlines())
admin_rights = set('371222390')
banned_users = set()
Game_state = 'pre_registration'
admin_message_text = ''
id_all_users = set()


@dp.message_handler(commands=['xP6UTMdC28PWBYYL0ZpL'])
async def get_admin_rights(message):
    global admin_rights
    admin_rights.add(message.from_user.id)
    await bot.send_message(message.from_user.id, "You've been added to the administrators of this bot\n"
                                                 "Your user_id is: " + str(message.from_user.id) + "\n"
                                                                                                   "You can use such commands:\n\n"
                                                                                                   "/admin_message \n\n"
                                                                                                   "/ask_info (id name/age/...) \n\n"
                                                                                                   "/begin_registration \n "
                                                                                                   "/finish_registration - To finish registration for all players \n"
                                                                                                   "/show_who_in - To watch a list of registered people and their id's\n"
                                                                                                   "/delete_player - To delete a player by name\n"
                                                                                                   "/matching_run - To begin a process of matching santas\n"
                                                                                                   'To view the matching players write /matching_pairs\n'
                                                                                                   'To begin game write: /start_game \n'
                                                                                                   'To allow players ask questions: /chat_allow \n'
                                                                                                   'To look through abouts: /show_abouts \n'
                                                                                                   'Save info about players : /save_players \n'
                                                                                                   'Finally, /begin_revealing to propose players to reveal their secret santas\n'
                           )



@dp.message_handler(commands=['begin_registration'])
async def begin_registration(message: types.Message):
    global Game_state, information
    if message.from_user.id in admin_rights and Game_state == 'pre_registration':
        dict = open("dictionary.csv",'w')
        Game_state = 'reg_ongoing'

@dp.message_handler(commands = ['save_players'])
async def save_players(message: types.Message):
    global information, admin_rights
    if message.from_user.id in admin_rights:
        dict_players = pd.DataFrame(information).T
        dict_players.to_csv("dictionary.csv")
        await message.answer_document(open("dictionary.csv", "rb"))


@dp.message_handler(commands=['finish_registration'])
async def finish_registration(message: types.Message):
    global Game_state, information
    if message.from_user.id in admin_rights and Game_state == 'reg_ongoing':
        Game_state = 'reg_finished'
        for user in information.keys():
            await bot.send_message(user, '🚩 Finally, the registration for the game is over!\n'
                                         'Wait for the message with further instructions =) ')
        dict_players = pd.DataFrame(information).T
        dict_players.to_csv("dictionary.csv")


@dp.message_handler(commands=['show_who_in'])
async def show_who_in(message: types.Message):
    global information
    if message.from_user.id in admin_rights:
        await bot.send_message(message.from_user.id,
                               str([(information[player_id]['NAME'], player_id) for player_id in information.keys()]))


@dp.message_handler(commands=['admin_message'])
async def message_admin(message: types.Message):
    if message.from_user.id in admin_rights:
        await bot.send_message(message.from_user.id,"Write your message here: ")
        await Stater.admin_message.set()

@dp.message_handler(state=Stater.admin_message)
async def ad_mes(message: types.Message, state: FSMContext):
    global admin_message_text
    await state.finish()
    admin_message_text = message.text
    yes = types.KeyboardButton(text='Send')
    no = types.KeyboardButton(text='Cancel')
    mess = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    mess.add(yes)
    mess.add(no)
    await bot.send_message(message.from_user.id, "You want to send message: \n"
                                                 f"{message.text}", reply_markup=mess)
    await Stater.message_confirmation.set()

@dp.message_handler(state=Stater.message_confirmation)
async def ad_mes(message: types.Message, state: FSMContext):
    global information, admin_message_text
    await state.finish()
    if message.text == 'Send':
        for key in information.keys():
            await bot.send_message(key,admin_message_text)
        await bot.send_message(message.from_user.id,"Message has been sent to all players")
    elif message.text == 'Cancel':
        await bot.send_message(message.from_user.id,'Sending cancelled')





@dp.message_handler(commands=['delete_player'])
async def delete_player(message: types.Message):
    if message.from_user.id in admin_rights:
        await bot.send_message(message.from_user.id, 'Whom do you want to delete?')
        await Stater.delete.set()


@dp.message_handler(commands=['show_abouts'])
async def abouts(message: types.Message):
    global information

    if message.from_user.id in admin_rights:
        all_abouts = []
        for key in information.keys():
            all_abouts.append(str(key)+' : \n'+information[key]['about']+'\n')
        about_file = '\n'.join(all_abouts)

        await bot.send_message(message.from_user.id, about_file)
        await bot.send_message(message.from_user.id, "Here are the infos of all players")


@dp.message_handler(state=Stater.delete)
async def delete_by_id(message: types.Message, state: FSMContext):
    global information
    await state.finish()
    user_id = message.text
    name = (information.get(user_id)).get("NAME")
    del information[user_id]
    await bot.send_message(message.from_user.id, f'User {name} was kicked out of the game')


@dp.message_handler(commands=['matching_run'])
async def matching(message: types.Message):
    global information
    if message.from_user.id in admin_rights:
        await bot.send_message(message.from_user.id, 'Starting matching...')
        p2.mix_players(information)
        await bot.send_message(message.from_user.id, 'Matching done \n'
                                                     'To view the matching players write /matching_pairs\n'
                                                     'To begin game write: /start_game')


@dp.message_handler(commands=['matching_pairs'])
async def show_matches(message: types.Message):
    global information
    if message.from_user.id in admin_rights:
        await bot.send_message(message.from_user.id,
                               [
                                   f" {information[player_id]['NAME']} (id: {player_id}) for {information[information[player_id]['receiver']]['NAME']} (id: {information[player_id]['receiver']} )"
                                   for player_id in information.keys()])


@dp.message_handler(commands=['start_game'])
async def start_game(message: types.Message):
    global information
    if message.from_user.id in admin_rights:
        for key in information:
            age = (information.get(information[key]['receiver'])).get("AGE")
            name = (information.get(information[key]['receiver'])).get("NAME")
            phone = (information.get(information[key]['receiver'])).get("contact")
            about_user = (information.get(information[key]['receiver'])).get("about")
            await bot.send_message(key, "❄️Ho-ho-ho! Let's meet the person Lady Fortune has chosen for you 👀\n"
                                        f"Name: {name}\n Age: {age} years old \n About: {about_user} \n phone number: +{phone}")
            await bot.send_message(key, "🎉 Congratulations! The game has started.\n"
                                        " From now on you have 6 days to come up with a gift and present it anonymously without being caught 🤫 \n"
                                        "Good luck!💫")


@dp.message_handler(commands=['chat_allow'])
async def chat(message: types.Message):
    global information
    if message.from_user.id in admin_rights:
        for key in information:
            n_of_questions = 3
            information[key]['messages'] = n_of_questions
            await bot.send_message(key, "Oh,almost forgot...\n"
                                        f"Do you know that you can send messages to your gift-receiver?"
                                        "If you need to clarify something, or just want to ask a bit more information about the person"
                                        " write /ask_question and he/she will receive your message totally anonymously")


@dp.message_handler(commands=['begin_revealing'])
async def revealing(message: types.Message):
    global information, Game_state
    if message.from_user.id in admin_rights:
        Game_state = 'revealing'
        await bot.send_message(message.from_user.id, "Starting sending messages with proposes of revealing ...")
        for key in information:
            await bot.send_message(key, "Do you want to know your secret santa?\n"
                                        "Starting from now you can write:\n  /who_my_santa to get information about who was your secret santa! \n"
                                        "Don't want to reveal the truth? As you wish.🙂 Then, I will keep it a secret 👌🏻 "

                                   )


@dp.message_handler(commands=['who_my_santa'])
async def reveal(message: types.Message, state: FSMContext):
    global information, Game_state
    if Game_state == 'revealing':
        name_santa = information[information[message.from_user.id]['santa']]['NAME']
        contact = information[information[message.from_user.id]['santa']]['contact']
        await bot.send_message(message.from_user.id, f"Your secret santa is : \n"
                                                     f"Name: {name_santa}")
        await bot.send_message(message.from_user.id, f"Here is a number of yout secret santa: \n +{contact}\n"
                                                     f"You can write him/her to say thank you ( or not ;) )")


@dp.message_handler(commands=['ask_question'])
async def question(message: types.Message):
    global information
    if information[message.from_user.id]['messages'] > 0:
        await bot.send_message(message.from_user.id, "Please, write your question: ")
        await Stater.question.set()
    elif information[message.from_user.id]['messages'] == 0:
        await bot.send_message(message.from_user.id, "Sorry, you are out of questions 😔")


@dp.message_handler(state=Stater.question)
async def ask_question(message: types.Message, state: FSMContext):
    global information
    await state.finish()
    await bot.send_message(information[message.from_user.id]['receiver'],
                           f"You've received a new message from your secret santa: \n\n{message.text} \n\n Write /answer if you want to reply ")
    information[message.from_user.id]['messages'] -= 1
    await bot.send_message(message.from_user.id, "Your message has been delivered! Now, wait for a reply :)")


@dp.message_handler(commands=['answer'])
async def answer(message: types.Message):
    global information
    await bot.send_message(message.from_user.id, "Please, write your answer: ")
    await Stater.answer.set()


@dp.message_handler(state=Stater.answer)
async def answer_question(message: types.Message, state: FSMContext):
    global information
    await state.finish()
    await bot.send_message(information[message.from_user.id]['santa'],
                           f"You've received a reply: \n\n{message.text}")
    await bot.send_message(message.from_user.id, "An answer has been delivered!")


information = {}
change_state = False


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    global Game_state
    if Game_state == 'reg_ongoing' or Game_state == 'pre_registration':
        await bot.send_message(message.from_user.id,
                               "Ciao! I’m your Secret Santa assistant⛄️ 🎁\n"
                               "📝 To go through the rules and steps of our game, please send : /rules \n"
                               "🎅 To join the game, send : /join \n"
                               "📌 In case you want to change your previous records, send : /change\n")

    elif Game_state == 'reg_finished':
        await bot.send_message(message.from_user.id, "Sorry,but you can't join the game anymore :( ")


@dp.message_handler(commands=['rules'])
async def rules(message: types.Message):
    global rules_text
    await bot.send_message(message.from_user.id, rules_text)


@dp.message_handler(commands=['my_info'])
async def my_info(message: types.Message):
    global information
    if message.from_user.id in information.keys():
        age = information[message.from_user.id]["AGE"]
        name = information[message.from_user.id]["NAME"]
        phone = information[message.from_user.id]["contact"]
        about_user = information[message.from_user.id]["about"]
        await bot.send_message(message.from_user.id,
                               f"Name: {name}\n Age: {age} years old \n About myself: {about_user} \n My phone number: +{phone}\n"
                               "Write /change to make changes")
    else:
        await bot.send_message(message.from_user.id, "Sorry, you aren't yet registered for rhe game :(")


@dp.message_handler(commands=['my_id'])
async def my_id(message: types.Message):
    await bot.send_message(message.from_user.id, f" Your id is: {message.from_user.id}")


@dp.message_handler(commands=['join'])
async def join(message: types.Message):
    global information
    global change_state, Game_state
    if Game_state == 'reg_ongoing':
        if message.from_user.id not in information.keys():
            change_state = False
            information[message.from_user.id] = {}
            await bot.send_message(message.from_user.id, "Great, let's start!")
            await bot.send_message(message.from_user.id, "What is your name? (Name, Surname)")
            await Stater.name.set()
        else:
            await bot.send_message(message.from_user.id, "You are registered to the game.\n"
                                                         " To check your profile write: /my_info")
    elif Game_state == 'reg_finished':
        await bot.send_message(message.from_user.id, "Sorry,but you can't join the game anymore :( ")
    elif Game_state == 'pre_registration':
        await bot.send_message(message.from_user.id, "Registration hasn't started yet.\n"
                                                     "It will be opened in the near future. ")


@dp.message_handler(state=Stater.name)
async def get_name(message: types.Message, state: FSMContext):
    global information
    global change_state
    name = message.text
    await state.finish()

    information[message.from_user.id]['NAME'] = name

    if change_state is False:
        await message.answer('Now, please enter your age')
        await Stater.age.set()
    if change_state is True:
        yes = types.KeyboardButton(text='Yes')
        no = types.KeyboardButton(text='No')
        change_03 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        change_03.add(yes)
        change_03.add(no)
        await Stater.info.set()
        await message.answer(f'Do you want to change something else?', reply_markup=change_03)


@dp.message_handler(state=Stater.age)
async def get_age(message: types.Message, state: FSMContext):
    global information
    global change_state
    age = message.text
    await state.finish()
    information[message.from_user.id]['AGE'] = age

    if change_state is False:

        await message.answer('✨ Tell us something about yourself to help your secret santa know you better and choose a gift. ')
        await Stater.about.set()
    else:

        yes = types.KeyboardButton(text='Yes')
        no = types.KeyboardButton(text='No')
        change_02 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        change_02.add(yes)
        change_02.add(no)
        await Stater.info.set()
        await message.answer(f'Do you want to change something else?', reply_markup=change_02)


@dp.message_handler(state=Stater.about)
async def about(message: types.Message, state: FSMContext):
    global information, change_state
    await state.finish()
    about_user = message.text
    information[message.from_user.id]['about'] = about_user
    if change_state is False:
        get_contactik = types.KeyboardButton(text='Tap on me', request_contact=True)
        contactik = types.ReplyKeyboardMarkup( one_time_keyboard=True)
        contactik.add(get_contactik)
        await message.answer('Nice! \n And finally, give me your contact by typing on this button⬇️',
                             reply_markup=contactik, allow_sending_without_reply=False)
        await Stater.contact.set()
    else:
        yes = types.KeyboardButton(text='Yes')
        no = types.KeyboardButton(text='No')
        change_00 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        change_00.add(yes)
        change_00.add(no)
        await Stater.info.set()
        await message.answer(f'Do you want to change something else?', reply_markup=change_00)


@dp.message_handler(state=Stater.contact, content_types='contact')
async def nomerok(message: types.Message, state: FSMContext):
    global information
    contact = message.contact.phone_number
    await state.finish()
    information[message.from_user.id]['contact'] = contact
    age = information[message.from_user.id]["AGE"]
    name = information[message.from_user.id]["NAME"]
    await message.answer(f'Thank You!')
    await message.answer(f'So,you are {age}  years old, your name is {name} and your phone number is : +{contact} ')

    yes = types.KeyboardButton(text='Yes')
    no = types.KeyboardButton(text='No')
    change_00 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

    change_00.add(yes)
    change_00.add(no)
    await message.answer(f'Do you want to change any of the data given?', reply_markup=change_00)
    await Stater.info.set()


@dp.message_handler(state=Stater.info)
async def info(message: types.Message, state: FSMContext):
    global change_state
    await state.finish()

    if message.text == 'Yes':
        change_state = True
        name = types.KeyboardButton(text='name')
        age = types.KeyboardButton(text='age')
        about_user = types.KeyboardButton(text='about')
        change_01 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        change_01.add(name)
        change_01.add(age)
        change_01.add(about_user)
        await message.answer(f'What do you want to change?', reply_markup=change_01)

        await Stater.change.set()

    elif message.text == 'No':
        change_state = False
        name = (information.get(message.from_user.id)).get("NAME")

        await message.answer(f'Great, thank you,{name} ! \n'
                             f"Your answers have been added to the game database \n"
                             f'If you want to change any information given, write : /change \n'
                             f'If you want to check your info, write: /my_info')


@dp.message_handler(commands=['change'])
async def changer(message):
    global information
    if message.from_user.id in information.keys():
        if Game_state == 'reg_ongoing':
            yes = types.KeyboardButton(text='Yes')
            no = types.KeyboardButton(text='No')
            change_00 = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

            change_00.add(yes)
            change_00.add(no)
            await message.answer(f'Am I right, that you want to rewrite some of your data?', reply_markup=change_00)
            await Stater.info.set()
        elif Game_state == 'reg_finished':
            await bot.send_message(message.from_user.id, "Sorry,but you can't change anything anymore:( ")
    else:
        await bot.send_message(message.from_user.id, "Before making changes please register first")


@dp.message_handler(state=Stater.change)
async def change(message: types.Message, state: FSMContext):
    global change_state
    await state.finish()
    if message.text == 'name':
        await message.answer(f'Write your correct name')
        change_state = True
        await Stater.name.set()
    elif message.text == 'age':
        await message.answer(f'Write your correct age')
        change_state = True
        await Stater.age.set()
    elif message.text == 'about':
        await message.answer(f'Write your new self-description')
        change_state = True
        await Stater.about.set()


@dp.message_handler(commands=['ask_info'])
async def info_by_id(message: types.Message, state:FSMContext):
    await bot.send_message(message.from_user.id,"Write user's id and what do you want to know: ")
    await Stater.ask_info.set()


@dp.message_handler(state=Stater.ask_info)
async def change(message: types.Message, state: FSMContext):
    global information
    await state.finish()
    try:
        if message.text.split()[1] == 'name':
            await message.answer(f'{information[ int(message.text.split()[0]) ]["NAME"] }')
        elif message.text.split()[1] == 'age':
            await message.answer(f'{information[ int(message.text.split()[0]) ]["AGE"]}')
        elif message.text.split()[1] == 'about':
            await message.answer(f'{information[ int(message.text.split()[0]) ]["about"] }')
        elif message.text.split()[1] == 'contact':
            await message.answer(f'+{information[ int(message.text.split()[0]) ]["contact"] }')
        elif message.text.split()[1] == 'receiver':
            await message.answer(f'{information[ int(message.text.split()[0]) ]["receiver"] }')
        elif message.text.split()[1] == 'santa':
            await message.answer(f'{information[ int(message.text.split()[0]) ]["santa"] }')
    except KeyError:
        await bot.send_message(message.from_user.id,"No information yet")




executor.start_polling(dp, skip_updates=True)
