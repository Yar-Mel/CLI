
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
            command = Parser.command_check(user_command, COMANDS)
            if command:
                if command != 'exit_commnad':
                    handler = commands_handler[command]
                    result = handler(*data)
                    print(result)
                else:
                    handler = commands_handler[command]
                    result = handler()
                    print(result)
                    return
            else:
                print(Message.unknown_command_message(user_command))
        else:
            print(Message.empty_input_message)


# ----------Entry point----------
if __name__ == '__main__':
    main()
