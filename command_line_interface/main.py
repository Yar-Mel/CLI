
from settings import COMANDS

from methods import Message, Parser

from handlers import commands_handler


# ----------Request-Respond----------
def main() -> None:

    print(Message.start_message)

    while True:
        user_input = input('>>> ')
        user_command, data = Parser.input_parser(user_input)
        if user_command:
            valid_command = Parser.command_check(user_command, COMANDS)
            if valid_command:
                if valid_command == 'hello_command':
                    handler = commands_handler[valid_command]
                    result = handler
                    print(result)
                elif valid_command == 'exit_command':
                    handler = commands_handler[valid_command]
                    result = handler
                    print(result)
                    return
                else:
                    handler = commands_handler[valid_command]
                    result = handler(*data)
                    print(result)
            else:
                print(Message.unknown_command_message)
        else:
            print(Message.empty_input_message)


# ----------Entry point----------
if __name__ == '__main__':
    main()
