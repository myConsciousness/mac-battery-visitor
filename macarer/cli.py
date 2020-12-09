"""
Copyright 2020 Kato Shinya.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. See the License for the specific language governing permissions and limitations under
the License.
"""

import sys
from os import getenv
from macarer.macarer import Macarer

__DEFAULT_UPPER_LIMIT = 0.71
__DEFAULT_LOWER_LIMIT = 0.31
__DEFAULT_LINE_NOTIFY_TOKEN = str(getenv('LINE_NOTIFY_TOKEN_FOR_MACARER'))

__KEY_UPPER_LIMIT = 'upper_limit'
__KEY_LOWER_LIMIT = 'lower_limit'
__KEY_LINE_NOTIFY_TOKEN = 'line_notify_token'


def execute():
    """
    Executes the process of Macarer.

    If you specify arguments, please input them in the following format.

    macarer upper_limit=float_number lower_limit=float_number line_notify_token=token_associated_with_line_room'

    Therefore following format:
        macarer upper_limit=0.71 lower_limit=0.41
        macarer line_notify_token=0123456789abcdefghijk
                    ...or something like above!

    Raises:
        RuntimeError: When invalid argument format is detected
    """

    args = sys.argv[1:]

    if args:
        battery_upper_limit = 0.0
        battery_lower_limit = 0.0
        line_notify_token = ''

        for arg in args:
            splited_arg = arg.split('=')

            if len(splited_arg) < 2:
                __print_error_messages()
                raise RuntimeError('Invalid format was detected.')

            if splited_arg[0] == __KEY_UPPER_LIMIT:
                battery_upper_limit = float(splited_arg[1])
            elif splited_arg[0] == __KEY_LOWER_LIMIT:
                battery_lower_limit = float(splited_arg[1])
            elif splited_arg[0] == __KEY_LINE_NOTIFY_TOKEN:
                line_notify_token = str(splited_arg[1])

        Macarer(
            battery_upper_limit if battery_upper_limit > 0.0 else __DEFAULT_UPPER_LIMIT, battery_lower_limit if battery_lower_limit > 0.0 else __DEFAULT_LOWER_LIMIT,
            line_notify_token if line_notify_token else __DEFAULT_LINE_NOTIFY_TOKEN
        ).examine()

    else:
        Macarer().examine()


def __print_error_messages():
    """
    Prints the error message with correct argument format.
    """

    print('The set of arguments is invalid:')
    print('    If you specify arguments, please enter them in the following format.')
    print('        macarer upper_limit=float_number lower_limit=float_number line_notify_token=token_associated_with_line_room')
    print('        therefore')
    print('            macarer upper_limit=0.71 lower_limit=0.41')
    print('            macarer line_notify_token=0123456789abcdefghijk')
