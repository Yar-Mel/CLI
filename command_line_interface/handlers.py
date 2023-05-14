

from methods import Message, AddressBook
from methods import Record, Name, Phone, PhoneType, Birthday
from methods import PhoneTypeError, PhoneFormatError, NameFormatError, BirthdayFormatError

user_book = AddressBook()


# ----------Error handler----------
def input_error(func) -> str:
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except IndexError:
            return Message.index_error_message
        except KeyError:
            return Message.key_error_message
        except TypeError:
            return Message.type_error_message
        except ValueError:
            return Message.value_error_message
        except PhoneTypeError:
            return Message.phone_type_error_message
        except PhoneFormatError:
            return Message.phone_format_error_message
        except  NameFormatError:
            return Message.name_format_error_message
        except  BirthdayFormatError:
            return Message.birthday_format_error_message        
        else:
            return result
    return wrapper


# ----------Handlers----------
@ input_error
def add_record(name: str, phone_number: str | None = None, phone_type: str | None = None, birthday: str | None = None) -> str:
    if name not in user_book.data:
        
        _name = Name(name)
        _phone_type = PhoneType(phone_type)
        _phone_number = Phone(phone_number)
        _birthday = Birthday(birthday)
    
        record = Record(_name, _phone_number, _phone_type, _birthday)
        user_book.add_record(record)
        return Message.add_message
    else:
        return Message.add_exists_message

@ input_error
def update_phone(name: str, new_phone_number: str, phone_type: str | None = None) -> str:
    
    _name = Name(name)
    _phone_type = PhoneType(phone_type)
    _new_phone_number = Phone(new_phone_number)
    
    record = user_book.get_record(_name)
    record.update_phone(_phone_type, _new_phone_number)
    user_book.add_record(record)
    return Message.update_message

@ input_error   
def update_birthday(name: str, birthday: str) -> str:
    if name in user_book.data:
        _name = Name(name)
        _birthday = Birthday(birthday)
        
        record = user_book.get_record(_name)
        record.birthday = _birthday
        user_book.add_record(record)
        return Message.update_message
    else:
        return Message.not_exists_message
    
@ input_error
def delete_record(name: str) -> str:
    
    _name = Name(name)
    
    if user_book.data:
        del user_book.data[_name.value]
        return Message.delete_message
    else:
        return Message.empty_book_message

@ input_error
def show_record(name: str) -> str:
    
    _name = Name(name)
    
    if user_book.data:
        record = user_book.get_record(_name)
        return record.show_record()
    else:
        return Message.empty_book_message

@ input_error
def show_all_records() -> str:
    if user_book.data:
        return user_book.show_records()
    else:
        return Message.empty_book_message

@ input_error
def debug() -> str:
    info = user_book.iterator(1)
    result = ''
    for i in info:
        result += f'{i}\n'
    return result

commands_handler = {
    'hello_command': Message.hello_message,
    'add_command': add_record,
    'add_bd_command': update_birthday,
    'update_command': update_phone,
    'show_command': show_record,
    'delete_command': delete_record,
    'show_all_command': show_all_records,
    'debug_command': debug,
    'exit_commnad': Message.exit_message
    }


# name_1 = Name('Test_1')
# name_2 = Name('Test_2')
# name_3 = Name('Test_3')
# name_4 = Name('Test_4')
# name_5 = Name('Test_5')

# phone = Phone(None)
# phone_type = PhoneType('work')
# birthday_1 = Birthday(None)
# birthday_2 = Birthday('13-05-2000')
# birthday_3 = Birthday('14-05-2000')
# birthday_4 = Birthday('15-05-2000')
# birthday_5 = Birthday('16-05-2000')

# record_1 = Record(name_1, phone, phone_type, birthday_1)
# record_2 = Record(name_2, phone, phone_type, birthday_2)
# record_3 = Record(name_3, phone, phone_type, birthday_3)
# record_4 = Record(name_4, phone, phone_type, birthday_4)
# record_5 = Record(name_5, phone, phone_type, birthday_5)


# user_book.add_record(record_1)
# user_book.add_record(record_2)
# user_book.add_record(record_3)
# user_book.add_record(record_4)
# user_book.add_record(record_5)