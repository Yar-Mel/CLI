from collections import UserDict


class Message:
    # Commands
    start_message = '\nSupported functions:\n\n1. Add [Name] (Phone) (Phone type)\n2. Change [Name] [Phone] (Phone type)\n3. Phone [Name]\n4. Show all\n5. Exit\n\nSay hello to start\n'
    hello_message = '\nHow can I help you?'
    exit_message = '\nGood bye!'
    add_message = '\nRecord has been added'
    add_exists_message =  '\nUser alredy exists'
    update_message = '\nRecord has been updated'
    empty_book_message = '\nPhone book is empty'
    delete_message = '\nRecord has been deleted'
    empty_input_message = 'Empty input. Please, try again'
    unknown_command_message = "\nI don't know this command("
    
    # Errors
    index_error_message = '\nIndexError. Something wrong, try again\n'
    key_error_message = "\nKeyError. I don't know this name(\n"
    type_error_message = '\nTypeError. Something wrong, try again\n'
    phone_type_error_message = '\nPhone type must be is one of "Work", "Mobile" or "Home"\n'


class Field:
    def __init__(self, value) -> None:
        self.value = value


class Name(Field):
    def __init__(self, value) -> None:
        super().__init__(value)

    def __repr__(self) -> str:
        return f"Name(value={self.value})"


class PhoneTypeError(Exception):
    pass


class PhoneType(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
        if value not in ['mobile', 'work', 'home']:
           raise PhoneTypeError


    def __repr__(self) -> str:
        return f"PhoneType(value={self.value})"


class Phone(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
    
    def __repr__(self) -> str:
        return f"Phone(value={self.value})"


class Birthday(Field):
    def __init__(self, value) -> None:
        super().__init__(value)
    
    def __repr__(self) -> str:
        return f"Birthday(value={self.value})"


class Record(Field):
    
    def __init__(
        self,
        name: Name,
        phone: Phone | str | None = None,
        phone_type: PhoneType | str = 'Mobile'
        ) -> None:
        
        self.name = name
        self.phone_type = phone_type
        self.phones = []
        if phone is not None:
            self.add_phone(phone_type, phone)
    
    def __repr__(self) -> str:
        return f"Record: {self.name}, phones: {self.phones}"        
    
    def add_phone(self, phone_type: PhoneType | str, new_phone: Phone | str):
            self.phones.append({phone_type: new_phone})
    
    def update_phone(self, phone_type: PhoneType | str, new_phone: Phone | str) -> None:
            for phone in self.phones:
                for i in phone.keys():
                    if phone_type.value == i.value:
                        phone[i] = new_phone
                        return
            self.phones.append({phone_type: new_phone})
    
    def show_record(self) -> str:
        result = f'\n{self.name.value}\n\n'
        for phone in self.phones:
            for k, v in phone.items():
                    result += f'{k.value}: {v.value}\n'
        return result


class AddressBook(UserDict, Field):

    def __init__(self, record: Record | None = None) -> None:
        UserDict.__init__(self)
        self.record = record

    def add_record(self, record: Record) -> None:
            self.data[record.name.value] = record
    
    def get_record(self, record_name: Name) -> Record:
        return self.data[record_name.value]
    
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
