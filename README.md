# Macarer: Carer for the battery of your important MacBook

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

**_Table of Contents_**

- [What is it?](#what-is-it)
- [Benefits](#benefits)
- [How To Use](#how-to-use)
  - [**_1: Create the TOKEN of LINE Notify API_**](#_1-create-the-token-of-line-notify-api_)
  - [**_2: Set Environment Variable (optional)_**](#_2-set-environment-variable-optional_)
  - [**_3: Install or Clone Macarer_**](#_3-install-or-clone-macarer_)
  - [**_4: Import and Run Macarer_**](#_4-import-and-run-macarer_)
  - [**_5: Run with the CLI_**](#_5-run-with-the-cli_)
- [License](#license)
- [More Information](#more-information)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## What is it?

**_Make your MacBook's battery condition last longer!_**

`Macarer` is a script created with the purpose of optimizing the battery state of MacBook.

Monitor MacBook's battery status and battery life to prevent overcharged and undercharged conditions.</br>
If `Macarer` detects an overcharge and undercharge condition, it uses the `LINE Notify API` to send a notification to the LINE room associated with the specified token.

## Benefits

- Theoretically make the battery condition of the MacBook last longer

- Easy and intuitive configuration and operation

- Receive notifications on [LINE](https://line.me/en-US/)

- Schedule monitoring using **_cron_**

## How To Use

### **_1: Create the TOKEN of LINE Notify API_**

Read [public documentation](https://notify-bot.line.me/en/) and create the token of LINE Notify API.

> **_Note:_**</br>
> The tokens you create in this step are required.</br>
> This token will be used to send notifications to Notify room on LINE.

### **_2: Set Environment Variable (optional)_**

Set the token created in the above step to environment variable.

```sh
export LINE_NOTIFY_TOKEN_FOR_MACARER=0123456789abcdefghijk
```

> **_Note:_**</br>
> This step is not necessary if you want to pass in the token you created as an argument.

### **_3: Install or Clone Macarer_**

**_Install_**

```cmd
pip install macarer
```

**_Clone_**

```cmd
git clone https://github.com/myConsciousness/mac-battery-visitor.git
```

### **_4: Import and Run Macarer_**

**_Default:_**

The default case runs in the following states.

| Option              | Value                                                 |
| ------------------- | ----------------------------------------------------- |
| battery_upper_limit | 0.71                                                  |
| battery_lower_limit | 0.31                                                  |
| line_notify_token   | The environment value (LINE_NOTIFY_TOKEN_FOR_MACARER) |

```python
from macarer.macarer import Macarer

Macarer().examine()
```

**_With specific options:_**

```python
from macarer.macarer import Macarer

Macarer(battery_upper_limit=0.65, battery_lower_limit=0.21, line_notify_token='0123456789abcdefghijk').examine()
```

### **_5: Run with the CLI_**

**_Default:_**

The default case runs in the following states.

| Option              | Value                                                 |
| ------------------- | ----------------------------------------------------- |
| battery_upper_limit | 0.71                                                  |
| battery_lower_limit | 0.31                                                  |
| line_notify_token   | The environment value (LINE_NOTIFY_TOKEN_FOR_MACARER) |

```sh
macarer
```

**_With specific options:_**

```sh
macarer upper_limit=0.65, lower_limit=0.21, line_notify_token=0123456789abcdefghijk
```

> **_Note:_**</br>
> With specific options, the above format is required.

## License

```license
Copyright 2020 Kato Shinya.

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
in compliance with the License. You may obtain a copy of the License at

     http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License
is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
or implied. See the License for the specific language governing permissions and limitations under
the License.
```

## More Information

`Macarer` was designed and implemented by Kato Shinya, who works as a freelance developer.

Regardless of the means or content of communication, I would love to hear from you if you have any questions or concerns. I do not check my email box very often so a response may be delayed, anyway thank you for your interest!

- [Creator Profile](https://github.com/myConsciousness)
- [Creator Website](https://myconsciousness.github.io/)
- [License](https://github.com/myConsciousness/mac-battery-visitor/blob/master/LICENSE)
- [PyPi](https://pypi.org/project/macarer/)
- [Release Note](https://pypi.org/project/macarer/#history)
- [File a Bug](https://github.com/myConsciousness/mac-battery-visitor/issues)
