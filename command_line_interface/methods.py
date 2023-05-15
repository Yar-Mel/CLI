

import re


from collections import UserDict
from datetime import datetime


from settings import ALLOWED_PHONE_TYPES, DEFAULT_PHONE_TYPE, DEFAULT_EMPTY_FIELD


#Messages
class Message:
    # Commands
    start_message = '\
        \nSupported functions:\n\n\
        1. Add [Name] (Phone) (Phone type) (Birthday)\n\
        2. Change [Name] [Phone] (Phone type)\n\
        3. Birthday [Name] [Birthday date]\n\
        4. Show [Name]\n\
        5. All\n\
        6. Debug\n\
        7. Exit\n\
        \nSay hello to start!\n'
    
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
    birthday_is_today_message = 'Birthday is today!'
    
    # Errors
    index_error_message = '\nIndexError. Something wrong, try again\n'
    key_error_message = "\nKeyError. I don't know this name(\n"
    type_error_message = '\nTypeError. Something wrong, try again\n'
    value_error_message = '\nValueError. Something wrong, try again\n'
    phone_type_error_message = '\nPhone type must be is one of "work", "mobile" or "home"\n'
    phone_format_error_message = '\nPhone must be numeric with 9 char\n'
    name_format_error_message = '\nName must less than 16 char\n'
    birthday_format_error_message = 'Birthday must be in [dd-mm-yyyy] format and not in the future!'
    days_to_birthday_message = 'Days to birthday'


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
    def value(self, value: str) -> None:
        if self.name_validate(value):
            Field.value.fset(self, value)
        else:
            raise TypeError
            
    def name_validate(self, value: str) -> bool:
        if value is not None and len(value) <= 16:
            return True
        raise NameFormatError
        


    def __repr__(self) -> str:
        return f"Name(value={self.value})"


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
    
    @Field.value.setter
    def value(self, value: str) -> None:  
        for phone_type, phone_number in value.items():
            
            if phone_type is None and phone_number is None:
                Field.value.fset(self, {DEFAULT_PHONE_TYPE: DEFAULT_EMPTY_FIELD})
                
            elif phone_type is None and phone_number is not None:
                if self.phone_number_validate(phone_number):
                    Field.value.fset(self, {DEFAULT_PHONE_TYPE: self.phone_normalize(phone_number)})
                    
            elif phone_type is not None and phone_number is None:
                if self.phone_type_validate(phone_type):
                    Field.value.fset(self, {phone_type: DEFAULT_EMPTY_FIELD})
                    
            elif phone_type is not None and phone_number is not None:
                if self.phone_type_validate(phone_type) and self.phone_number_validate(phone_number):
                    Field.value.fset(self, {phone_type: self.phone_normalize(phone_number)})
            else:                                       
                raise TypeError

    def phone_type_validate(self, phone_type: str) -> bool:
        if phone_type in ALLOWED_PHONE_TYPES:
             return True
        raise PhoneTypeError

    def phone_number_validate(self, phone_number: str) -> bool:
        if len(phone_number) == 9 and phone_number.isnumeric():
            return True
        raise PhoneFormatError

    def phone_normalize(self, phone_number: str) -> str:
        return f'+380-{phone_number[0:2]}-{phone_number[2:5]}-{phone_number[5:7]}-{phone_number[7:9]}'
    
    def __repr__(self) -> str:
        for phone_type, phone_number in self.value.items():
            return f"Phone(value(type={phone_type}, number={phone_number})"


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
    
    @Field.value.setter
    def value(self, value: str) -> None:
        if value == None:
            Field.value.fset(self, DEFAULT_EMPTY_FIELD)
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
        if isinstance(self.value, datetime):
            return f"Birthday(value={self.value.date()})"
        return f"Birthday(value={self.value})"


class Record(Field):
    
    def __init__(
        self,
        name: Name,
        phone: Phone | None = None,
        birthday: Birthday | None = None
        ) -> None:
        
        self.name = name
        self.birthday = birthday
        self.phones = []
        if name:
            self.add_phone(phone)       

    def add_phone(self, new_phone: Phone | str) -> None:
            self.phones.append(new_phone)

    def update_phone(self, new_phone: Phone | str) -> None:
        for phone in self.phones:
            for phone_type, new_phone_type in zip(phone.value, new_phone.value):
                if phone_type == new_phone_type:
                    phone.value[phone_type] = new_phone.value[new_phone_type]
                    return
        self.phones.append(new_phone)
            
    def days_to_birthday(self, birthday: Birthday | datetime) -> int:
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
        result = '\n{:^40}\n{:^40}\n'.format(self.name.value, '-'*40)
        for phone in self.phones:
            for phone_type, phone_number in phone.value.items():
                if phone_number:
                    result += '|{:^18}|{:^19}|\n{:^40}\n'.format(phone_type, phone_number, ('-'*40))
                    
        if isinstance(self.birthday.value, datetime):
            days_to_birthday = self.days_to_birthday(self.birthday.value)
            if days_to_birthday == 0:
                result += '|{:^38}|\n{:^40}\n'.format(Message.birthday_is_today_message, '-'*40)
            else:
                result += '|{:^18}|{:^19}|\n{:^40}\n'.format(Message.days_to_birthday_message, days_to_birthday, '-'*40)
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
    
    def iterator(self, N: int) -> str:
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

