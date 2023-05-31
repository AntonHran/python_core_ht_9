import re
import sys
from typing import *
from typing import Type
import json


def input_error(func):
    def inner_func(*parameters):
        try:
            qu = len([param for param in parameters if param])
            if qu == len(parameters):
                res = func(*parameters)
                return res
            else:
                raise KeyError
        except (KeyError, ValueError, IndexError, TypeError) as error:
            print(f'Error: {error}. Please check the accordance of the entered data to the requirements.\n'
                  f'And also a correctness of the entered name or/and phone number. And their existence.')

    return inner_func


def greeting() -> None:
    print('How can I help you?')


@input_error
def add(name: str, number: str):
    number = normalize(number)
    if name and number:
        phone_numbers.update({name: number})
        print('Contact was added.')


@input_error
def delete(name: str):
    del phone_numbers[name]
    print('Contact was deleted.')


@input_error
def change(name: str, new_number: str):
    new_number = normalize(new_number)
    if name and new_number:
        phone_numbers.pop(name)
        phone_numbers.update({name: new_number})
        print('Phone number was changed.')


@input_error
def change_name(name: str):
    number: str = phone_numbers[name]
    new_name = name.replace(name, '').strip()
    if new_name:
        phone_numbers.pop(name)
        phone_numbers.update({new_name: number})
        print('Name was changed.')
    else:
        raise TypeError


@input_error
def show_phone_number(name: str) -> None:
    print(f'{name}: {phone_numbers[name]}')


def show_all():
    print('\nContacts:')
    [print('|{:<20}|{:^20}|'.format(name, number)) for name, number in phone_numbers.items()]


def help_():
    print('''\nCommands:
    To add a new contact enter: add <name> <number>
    To delete some contact enter: delete <name>
    To change a number of some contact enter: change number <name as it was recorded> <new phone number>
    To change a name of some contact enter: change name <name as it was recorded> <new name>
    To show a phone number of some contact enter: phone <name as it was recorded>
    To show all notices enter: show all
    To exit and shut down the CUI assistant enter: good bye or close or exit
    To read all commands once again enter: help
    All phone numbers should be added according to a phone pattern: +380(XX)-XXX-XX-XX or 0XX-XXX-XXXX
    Names and phone numbers are written without brackets <...>''')


def farewell():
    print('Good bye!')
    with open('phone_numbers.json', 'w') as file:
        json.dump(phone_numbers, file, indent=4)
    sys.exit()


@input_error
def normalize(phone: str) -> None | str:
    LOWER: int = 9
    HIGHER: int = 12
    pattern: str = r'\+380\(\d{2}\)\d{3}-\d{2}-\d{2}'
    if not re.match(pattern, phone):
        phone = [re.sub('[+\-() ]', '', symbol) for symbol in phone]
        if HIGHER > len(phone) > LOWER and ''.join(phone).isdigit():
            dif = len(phone) - LOWER
            phone = phone[dif:]
        else:
            raise TypeError
        phone = f'+380({phone[0]}{phone[1]}){phone[2]}{phone[3]}{phone[4]}-{phone[5]}{phone[6]}-{phone[7]}{phone[8]}'
    return phone


@input_error
def parser(command: str) -> Tuple | Type[KeyError] | List:
    text: list = command.split(' ')
    keys: List[tuple] = [(key, COMMANDS[key][1]) for key in COMMANDS if re.search(text[0].lower(), ''.join(key)
                                                                                if type(key) is str else ' '.join(key))]
    if len(keys) > 1:
        keys = [(key, COMMANDS[key][1]) for key in COMMANDS if re.fullmatch(' '.join(text[:2]).lower(), ''.join(key))]
    if keys:
        key_command, argument_num = keys[0][0], keys[0][1]
        if argument_num == 0:
            return [key_command]
        elif argument_num == 1:
            if type(key_command) is str:
                args = command.replace(key_command, '').strip()
                return key_command, args
            else:
                args = [command.replace(com, '') for com in key_command]
                return key_command, ' '.join(args).strip()
        else:
            if type(key_command) is str:
                args = command.replace(key_command, '').strip()
                *name, phone = args.split(' ')
                return key_command, ' '.join(name), phone
            else:
                args = [command.replace(com, '') for com in key_command]
                return key_command, ' '.join(args[:-1]).strip(), args[-1]


@input_error
def handle_input(key_word: str) -> Tuple:
    return COMMANDS[key_word]


COMMANDS = {('hello', 'hi'): (greeting, 0),
            'add': (add, 2),
            'change number': (change, 2),
            'change name': (change_name, 1),
            'phone': (show_phone_number, 1),
            'delete': (delete, 1),
            'show all': (show_all, 0),
            ('good bye', 'close', 'exit'): (farewell, 0),
            'help': (help_, 0), }


def main():
    print('Welcome to the CUI personal assistant.\n'
          'I can help you with adding, changing, showing and storing all contacts.')
    global phone_numbers
    with open('phone_numbers.json', 'r') as jf:
        phone_numbers = json.load(jf)
    help_()
    while True:
        text = input('\nEnter your command: ')
        command = parser(text)
        try:
            if len(command) == 1:
                handler = handle_input(command[0])
                handler[0]()
            elif len(command) == 2:
                handler = handle_input(command[0])
                handler[0](command[1])
            else:
                handler = handle_input(command[0])
                handler[0](command[1], command[2])
        except (TypeError, KeyError):
            print('I do not understand what you want to do. Please look at the commands.')


if __name__ == '__main__':
    main()
