

from methods import Message, AddressBook, Record, Name, Phone, PhoneType, PhoneTypeError


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
        except PhoneTypeError:
            return Message.phone_type_error_message
        else:
            return result
    return wrapper


# ----------Handlers----------
@ input_error   
def add_item(name: str, phone_number: str = 'empty', phone_type: str = 'mobile') -> str:
    if name not in user_book.data:
        
        _name = Name(name)
        _phone_type = PhoneType(phone_type)
        _phone_number = Phone(phone_number)
    
        record = Record(_name, _phone_number, _phone_type)
        user_book.add_record(record)
        return Message.add_message
    else:
        return Message.add_exists_message
 
@ input_error
def update_item(name: str, new_phone_number: str, phone_type: str = 'mobile') -> str:
    
    _name = Name(name)
    _phone_type = PhoneType(phone_type)
    _new_phone_number = Phone(new_phone_number)
    
    record = user_book.get_record(_name)
    record.update_phone(_phone_type, _new_phone_number)
    user_book.add_record(record)
    return Message.update_message

@ input_error
def delete_item(name: str) -> str:
    key = Name(name)
    if user_book.data:
        del user_book.data[key.value]
        return Message.delete_message
    else:
        return Message.empty_book_message

@ input_error
def show_item(name: str) -> str:
    key = Name(name)
    if user_book.data:
        record = user_book.get_record(key)
        return record.show_record()
    else:
        return Message.empty_book_message

@ input_error
def show_all() -> str:
    if user_book.data:
        return user_book.show_records()
    else:
        return Message.empty_book_message

@ input_error
def debug() -> str:
    return user_book.data

commands_handler = {
    'hello_command': Message.hello_message,
    'add_command': add_item,
    'update_command': update_item,
    'show_command': show_item,
    'delete_command': delete_item,
    'show_all_command': show_all,
    'debug_command': debug,
    'exit_commnad': Message.exit_message
    }
