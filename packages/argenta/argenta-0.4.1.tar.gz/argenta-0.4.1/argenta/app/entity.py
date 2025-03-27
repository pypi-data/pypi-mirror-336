from typing import Callable
from inspect import getfullargspec
import re

from argenta.command import Command
from argenta.router import Router
from argenta.router.defaults import system_router
from argenta.command.exceptions import (UnprocessedInputFlagException,
                                  RepeatedInputFlagsException,
                                  EmptyInputCommandException)
from .exceptions import (InvalidRouterInstanceException,
                         InvalidDescriptionMessagePatternException,
                         NoRegisteredRoutersException,
                         NoRegisteredHandlersException,
                         RepeatedCommandInDifferentRoutersException,
                         IncorrectNumberOfHandlerArgsException)


class App:
    def __init__(self,
                 prompt: str = 'Enter a command',
                 initial_message: str = '\nHello, I am Argenta\n',
                 farewell_message: str = '\nGoodBye\n',
                 invalid_input_flags_message: str = 'Invalid input flags',
                 exit_command: str = 'Q',
                 exit_command_description: str = 'Exit command',
                 system_points_title: str = 'System points:',
                 ignore_exit_command_register: bool = True,
                 ignore_command_register: bool = False,
                 line_separate: str = '',
                 command_group_description_separate: str = '',
                 repeat_command_groups: bool = True,
                 messages_on_startup: list[str] = None,
                 print_func: Callable[[str], None] = print) -> None:
        self.prompt = prompt
        self.print_func = print_func
        self.exit_command = exit_command
        self.exit_command_description = exit_command_description
        self.system_points_title = system_points_title
        self.ignore_exit_command_register = ignore_exit_command_register
        self.farewell_message = farewell_message
        self.initial_message = initial_message
        self.invalid_input_flags_message = invalid_input_flags_message
        self.line_separate = line_separate
        self.command_group_description_separate = command_group_description_separate
        self.ignore_command_register = ignore_command_register
        self.repeat_command_groups = repeat_command_groups
        self.messages_on_startup = messages_on_startup if messages_on_startup else []

        self._routers: list[Router] = []
        self._description_message_pattern: str = '[{command}] *=*=* {description}'
        self._registered_router_entities: list[dict[str, str | list[dict[str, Callable[[], None] | Command]] | Router]] = []
        self._invalid_input_flags_handler: Callable[[str], None] = lambda raw_command: print_func(f'Incorrect flag syntax: "{raw_command}"')
        self._repeated_input_flags_handler: Callable[[str], None] = lambda raw_command: print_func(f'Repeated input flags: "{raw_command}"')
        self._empty_input_command_handler: Callable[[], None] = lambda: print_func(f'Empty input command')
        self._unknown_command_handler: Callable[[Command], None] = lambda command: print_func(f"Unknown command: {command.get_trigger()}")
        self._exit_command_handler: Callable[[], None] = lambda: print_func(self.farewell_message)


    def start_polling(self) -> None:
        self._setup_system_router()
        self._validate_number_of_routers()
        self._validate_included_routers()
        self._validate_all_router_commands()

        self.print_func(self.initial_message)

        for message in self.messages_on_startup:
            self.print_func(message)

        if not self.repeat_command_groups:
            self._print_command_group_description()
            self.print_func(self.prompt)

        while True:
            if self.repeat_command_groups:
                self._print_command_group_description()
                self.print_func(self.prompt)

            raw_command: str = input()

            try:
                input_command: Command = Command.parse_input_command(raw_command=raw_command)
            except UnprocessedInputFlagException:
                self.print_func(self.line_separate)
                self._invalid_input_flags_handler(raw_command)
                self.print_func(self.line_separate)

                if not self.repeat_command_groups:
                    self.print_func(self.prompt)
                continue

            except RepeatedInputFlagsException:
                self.print_func(self.line_separate)
                self._repeated_input_flags_handler(raw_command)
                self.print_func(self.line_separate)

                if not self.repeat_command_groups:
                    self.print_func(self.prompt)
                continue

            except EmptyInputCommandException:
                self.print_func(self.line_separate)
                self._empty_input_command_handler()
                self.print_func(self.line_separate)

                if not self.repeat_command_groups:
                    self.print_func(self.prompt)
                continue

            is_exit = self._is_exit_command(input_command)
            if is_exit:
                return

            self.print_func(self.line_separate)
            is_unknown_command: bool = self._check_is_command_unknown(input_command)

            if is_unknown_command:
                self.print_func(self.line_separate)
                self.print_func(self.command_group_description_separate)
                if not self.repeat_command_groups:
                    self.print_func(self.prompt)
                continue

            for router in self._routers:
                router.input_command_handler(input_command)

            self.print_func(self.line_separate)
            self.print_func(self.command_group_description_separate)
            if not self.repeat_command_groups:
                self.print_func(self.prompt)


    def set_initial_message(self, message: str) -> None:
        self.initial_message: str = message


    def set_farewell_message(self, message: str) -> None:
        self.farewell_message: str = message


    def set_description_message_pattern(self, pattern: str) -> None:
        first_check = re.match(r'.*{command}.*', pattern)
        second_check = re.match(r'.*{description}.*', pattern)

        if bool(first_check) and bool(second_check):
            self._description_message_pattern: str = pattern
        else:
            raise InvalidDescriptionMessagePatternException(pattern)


    def set_invalid_input_flags_handler(self, handler: Callable[[str], None]) -> None:
        args = getfullargspec(handler).args
        if len(args) != 1:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._invalid_input_flags_handler = handler


    def set_repeated_input_flags_handler(self, handler: Callable[[str], None]) -> None:
        args = getfullargspec(handler).args
        if len(args) != 1:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._repeated_input_flags_handler = handler


    def set_unknown_command_handler(self, handler: Callable[[str], None]) -> None:
        args = getfullargspec(handler).args
        if len(args) != 1:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._unknown_command_handler = handler


    def set_empty_command_handler(self, handler: Callable[[str], None]) -> None:
        args = getfullargspec(handler).args
        if len(args) != 1:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._empty_input_command_handler = handler


    def set_exit_command_handler(self, handler: Callable[[], None]) -> None:
        args = getfullargspec(handler).args
        if len(args) != 0:
            raise IncorrectNumberOfHandlerArgsException()
        else:
            self._exit_command_handler = handler


    def add_message_on_startup(self, message: str) -> None:
        self.messages_on_startup.append(message)


    def include_router(self, router: Router) -> None:
        if not isinstance(router, Router):
            raise InvalidRouterInstanceException()

        router.set_ignore_command_register(self.ignore_command_register)
        self._routers.append(router)

        command_entities: list[dict[str, Callable[[], None] | Command]] = router.get_command_entities()
        self._registered_router_entities.append({'name': router.get_name(),
                                                 'title': router.get_title(),
                                                 'entity': router,
                                                 'commands': command_entities})


    def _validate_number_of_routers(self) -> None:
        if not self._routers:
            raise NoRegisteredRoutersException()


    def _validate_included_routers(self) -> None:
        for router in self._routers:
            if not router.get_command_entities():
                raise NoRegisteredHandlersException(router.get_name())


    def _validate_all_router_commands(self) -> None:
        for idx in range(len(self._registered_router_entities)):
            current_router: Router = self._registered_router_entities[idx]['entity']
            routers_without_current_router = self._registered_router_entities.copy()
            routers_without_current_router.pop(idx)

            current_router_all_commands: list[str] = current_router.get_all_commands()

            for router_entity in routers_without_current_router:
                if len(set(current_router_all_commands).intersection(set(router_entity['entity'].get_all_commands()))) > 0:
                    raise RepeatedCommandInDifferentRoutersException()
                if self.ignore_command_register:
                    if len(set([x.lower() for x in current_router_all_commands]).intersection(set([x.lower() for x in router_entity['entity'].get_all_commands()]))) > 0:
                        raise RepeatedCommandInDifferentRoutersException()


    def _setup_system_router(self):
        system_router.set_title(self.system_points_title)
        @system_router.command(Command(self.exit_command, self.exit_command_description))
        def exit_command():
            self._exit_command_handler()

        if system_router not in [router['entity'] for router in self._registered_router_entities]:
            self.include_router(system_router)


    def _is_exit_command(self, command: Command):
        if command.get_trigger().lower() == self.exit_command.lower():
            if self.ignore_exit_command_register:
                system_router.input_command_handler(command)
                return True
            else:
                if command.get_trigger() == self.exit_command:
                    system_router.input_command_handler(command)
                    return True
        return False


    def _check_is_command_unknown(self, command: Command):
        registered_router_entities: list[dict[str, str | list[dict[str, Callable[[], None] | Command]] | Router]] = self._registered_router_entities
        for router_entity in registered_router_entities:
            for command_entity in router_entity['commands']:
                if command_entity['command'].get_trigger().lower() == command.get_trigger().lower():
                    if self.ignore_command_register:
                        return False
                    else:
                        if command_entity['command'].get_trigger() == command.get_trigger():
                            return False
        self._unknown_command_handler(command)
        return True


    def _print_command_group_description(self):
        for router_entity in self._registered_router_entities:
            self.print_func(router_entity['title'])
            for command_entity in router_entity['commands']:
                self.print_func(self._description_message_pattern.format(
                        command=command_entity['command'].get_trigger(),
                        description=command_entity['command'].get_description()
                    )
                )
            self.print_func(self.command_group_description_separate)
