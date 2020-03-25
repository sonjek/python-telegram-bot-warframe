warframe_notification_tbot
======================

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![GitHub tag](https://img.shields.io/github/tag/sonjek/warframe_notification_tbot.svg)](https://github.com/sonjek/warframe_notification_tbot/tags/) [![License](https://img.shields.io/badge/License-BSD%203--Clause-blue.svg)](https://opensource.org/licenses/BSD-3-Clause)


A Telegram bot for event notification with a rare award (Orokin Reactor, Orokin Catalyst, Forma and etc).
It can send a notification to a configured Telegram channel or manually through an inline query to another user.

*NOTE*: This bot uses https://api.warframestat.us

You can try: [@warframe_monit_bot](https://t.me/warframe_monit_bot)


## Commands

### Supported public commands
```
/start             Main menu
/invasions         Invasions list
/alerts            Alerts list
/voidtrader        Baro Ki'Teer item list
/twitchstatus      Check Warframe Twitch channel activity
```

### Supported admin commands
```
/admin             Admin menu. Allows to enable or disable Telegram channel notifications.
```


## Build and run

Initial setup
-----------------
```bash
$ git clone https://github.com/sonjek/warframe_notification_tbot.git
$ cd warframe_notification_tbot
$ cp data/config.sample.json data/config.json
$ nano data/config.json
_________________________________________________________________________
{
    "admin_name": "ADMIN_NAME",
    "admin_id": "ADMIN_ID",
    "channel_id": "CHANNEL_ID",
    "bot_token": "TOKEN",
    "twitch_token": "TOKEN",
...
_________________________________________________________________________
```



Run method 1
-------------

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip3 install -r tbot/requirements.txt
$ venv/bin/python -i -m tbot.bot
```



Run method 2
-------------

#### Presetting
- Docker (Linux users can use [install instruction](https://docs.docker.com/install/linux/docker-ce/ubuntu/))
- Docker Compose (Linux users can use [install instruction](https://docs.docker.com/compose/install/#install-compose))

#### Build and run
```bash
$ docker-compose up --build -d
```



Run method 3
-------------

#### Presetting
- Docker (Linux users can use [install instruction](https://docs.docker.com/install/linux/docker-ce/ubuntu/))
- Docker Compose (Linux users can use [install instruction](https://docs.docker.com/compose/install/#install-compose))

#### Build and run
```bash
$ make build
```



License
-----------

The contents of this repository are licensed under the [The 3-Clause BSD License](https://opensource.org/licenses/BSD-3-Clause)
