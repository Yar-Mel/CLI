

import re


from collections import UserDict
from datetime import datetime


from settings import ALLOWED_PHONE_TYPES, DEFAULT_PHONE_TYPE


#Messages
class Message:
    # Commands
    start_message = '\
        \nSupported functions:\n\n\
        1. Add [Name] (Phone) (Phone type) (Birthday)\n\
        2. Change [Name] [Phone] (Phone type)\n\
        3. Birthday [Name] [Birthday date]\n\
        4. Phone [Name]\n\
        5. Show all\n\
        6. Exit\n\
        \nSay hello to start\n'
    
    hello_message = '\nHow can I help you?'
    exit_message = '\nGood bye!'
    add_message = '\nRecord has been added'
    add_exists_message =  '\nUser alredy exists'
    update_message = '\nRecord has been updated'
    empty_book_message = '\nPhone book is empty'
    delete_message = '\nRecord has been deleted'
    empty_input_message = 'Empty input. Please, try again'
    unknown_command_message = "\nI don't know this command("
    not_exists_message = "\nUser do not exists. First create record"
    
    # Errors
    index_error_message = '\nIndexError. Something wrong, try again\n'
    key_error_message = "\nKeyError. I don't know this name(\n"
    type_error_message = '\nTypeError. Something wrong, try again\n'
    value_error_message = '\nValueError. Something wrong, try again\n'
    phone_type_error_message = '\nPhone type must be is one of "work", "mobile" or "home"\n'
    phone_format_error_message = '\nPhone must be numeric with 9 char\n'
    name_format_error_message = '\nName must less than 16 char\n'
    birthday_format_error_message = '\nBirthday must be in [dd-mm-yyyy] format and not in the future!\n'
    
    
    def past_birthday(date: str | datetime):
        return f'Birthday was on {date}"\n'

# Custom errors
class NameFormatError(Exception):
    pass
class PhoneTypeError(Exception):
    pass
class PhoneFormatError(Exception):
    pass
class BirthdayFormatError(Exception):
    pass


# Methods
class Field:
    def __init__(self, value) -> None:
        self.__value = None
        self.value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        self.__value = new_value


class Name(Field):     
    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value: str):
        if len(value) > 16:
            raise NameFormatError
        else:
            Field.value.fset(self, value)

    def __repr__(self) -> str:
        return f"Name(value={self.value})"


class PhoneType(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    @Field.value.setter
    def value(self, value: str):
        if value == None:
            Field.value.fset(self, DEFAULT_PHONE_TYPE)
        elif value not in ALLOWED_PHONE_TYPES:
            raise PhoneTypeError
        else:
            Field.value.fset(self, value)

    def __repr__(self) -> str:
        return f"PhoneType(value={self.value})"


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
    
    @Field.value.setter
    def value(self, value: str):
        if value == None:
            pass
        else:
            if self.phone_validate(value):
                Field.value.fset(self, value)
            else:
                raise PhoneFormatError

    def phone_validate(self, phone):
        if len(phone) == 9 and phone.isnumeric():
            return True
        return False

    def __repr__(self) -> str:
        return f"Phone(value={self.value})"


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
    
    @Field.value.setter
    def value(self, value: str):
        if value == None:
            pass
        else:
            birthday_date = self.birthday_normalize(value)
            if birthday_date:
                Field.value.fset(self, birthday_date)
            else:
                raise BirthdayFormatError
    
    def birthday_normalize(self, value: str) -> datetime:
        result = None
        birthday_match = re.search(fr'^\d\d-\d\d-\d\d\d\d$', value)
        if birthday_match[0]:
            birthday_date = (datetime.strptime(birthday_match[0], '%d-%m-%Y'))
            if birthday_date < datetime.now():
                result = birthday_date
        return result
    
    def __repr__(self) -> str:
        if self.value:
            return f"Birthday(value={self.value.date()})"
        return f"Birthday(value={self.value})"


class Record(Field):
    
    def __init__(
        self,
        name: Name,
        phone: Phone | None = None,
        phone_type: PhoneType | None = None,
        birthday: Birthday | None = None
        ) -> None:
        
        self.name = name
        self.phone_type = phone_type
        self.birthday = birthday
        self.phones = []
        if name:
            self.add_phone(phone_type, phone)       

    def add_phone(self, phone_type: PhoneType | str, new_phone: Phone | str):
            self.phones.append({phone_type: new_phone})

    def update_phone(self, new_phone_type: PhoneType | str, new_phone: Phone | str) -> None:
            for phone in self.phones:
                for phone_type in phone.keys():
                    if new_phone_type.value == phone_type.value:
                        phone[phone_type] = new_phone
                        return
            self.phones.append({phone_type: new_phone})
            
    def days_to_birthday(self, birthday: Birthday | datetime):
        result = None
        current_date = datetime.now()
        if isinstance(birthday, datetime):
            _date = datetime(year=current_date.year, month=birthday.month, day=birthday.day+1)
            if _date < current_date:
                next_birthday = datetime(year=current_date.year+1, month=birthday.month, day=birthday.day)
                result =  next_birthday - current_date
            else:
                result = _date - current_date
            return result.days
    
    def show_record(self) -> str:
        result = f'\n{self.name.value}\n\n'
        for phone in self.phones:
            for k, v in phone.items():
                    if v.value:
                        result += f'{k.value}: {v.value}\n'
        if self.birthday.value:
            days_to_birthday = self.days_to_birthday(self.birthday.value)
            if (days_to_birthday) == 0:
                result += f'days to birthday: Birthday is today!\n'
            else:
                result += f'days to birthday: {days_to_birthday}\n'
        return result
    
    def __repr__(self) -> str:
        return f"Record: {self.name}, phones: {self.phones}, birthday: {self.birthday}" 


class AddressBook(UserDict, Field):

    def __init__(self, record: Record | None = None) -> None:
        UserDict.__init__(self)
        self.record = record

    def add_record(self, record: Record) -> None:
            self.data[record.name.value] = record
    
    def get_record(self, record_name: Name) -> Record:
        return self.data[record_name.value]
    
    def iterator(self, N: int):
        lisf_of_keys = [key for key in self.data.keys()]
        count = 0
        result = '\n'
        for indx, key in enumerate(lisf_of_keys):
            result += f'{indx}. {self.data[key]}\n'
            count += 1
            if count == N:
                yield result.rstrip()
                result = ''
                count = 0
    
    def show_records(self) -> str:
        result = ''
        for record in self.data.values():
            result += f'{record.show_record()}'
        return result


class Parser(Field):

    def input_parser(input: str) -> tuple:
        user_input = input.strip().split(' ')
        user_command = user_input[0].lower()
        data = user_input[1:]
        return user_command, data
    
    def command_check(user_command: str, commands: dict) -> str:
        for i in commands.keys():
            for j in commands[i]:
                if user_command == j:
                    return i

    def data_analisis(user_data: str) -> str:
        pass
