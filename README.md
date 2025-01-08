
# Secret Santa Bot for Telegram

A Telegram bot to organize and manage Secret Santa events. This bot allows you to register players, match them randomly, and send announcements. It also includes an admin feature with secret command authentication to allow for managing the event and player data.

## Features

- **Admin Commands**: Admin can start registration, match players, send announcements, and manage data.
- **Player Registration**: Players can register for the event, enter their information, and join the Secret Santa event.
- **Matching**: Once registration is complete, players are randomly matched with other participants for Secret Santa gifting.
- **Announcements**: Admin can send announcements to all players.
- **Admin Rights Authentication**: Access admin functions by entering a secret command.

## Requirements

- Python 3.x
- `python-telegram-bot` library
- A running Telegram bot (created via BotFather)

## Setup

### 1. Install Dependencies

To install the required dependencies, run:

```bash
pip install python-telegram-bot
```

### 2. Set Up the Bot Token

Create a bot on Telegram using [BotFather](https://core.telegram.org/bots#botfather) and get your bot's API token.

In the script, set your bot token:

```python
updater = Updater("YOUR_BOT_TOKEN", use_context=True)
```

### 3. Set the Admin Secret Command

In the script, define your secret command (e.g., `/admin_secret`):

```python
ADMIN_SECRET_COMMAND = 'admin_secret'
```

This command grants you admin rights once you enter it correctly.

### 4. Set Up Player Registration

In the script, you can adjust the parameters for registration (e.g., fields like names, emails, etc.):

```python
players = []
```

The bot will collect information for each player during registration.

### 5. Set Your Admin ID

Set the `ADMIN_ID` variable to your Telegram user ID to ensure only you (or other designated admins) can access admin commands:

```python
ADMIN_ID = 123456789  # Replace with your actual Telegram user ID
```

You can find your Telegram user ID by sending a message to [@userinfobot](https://t.me/userinfobot).

---

## How to Use the Bot

### Registering Players

To register, users simply need to send the `/register` command. The bot will guide them through entering their information.

### Admin Authentication

To access admin functions, enter the **secret command** that you set in the script (e.g., `/admin_secret`). After entering the correct command, you will be granted admin rights.

Once authenticated, you can use admin commands such as:

- `/begin_registration` to start player registration.
- `/match_players` to randomly assign Secret Santa matches.
- `/send_announcement` to send announcements to all players.
- `/view_data` to view registered player data.

### Admin Commands

- **/begin_registration**: Start the registration process for players.
- **/match_players**: Randomly match players for the Secret Santa event.
- **/send_announcement [message]**: Send a message to all registered players.
- **/view_data**: View the list of registered players.

### How to Authenticate as Admin:

1. When you attempt to use an admin command (e.g., `/begin_registration`), the bot will prompt you for the **secret command**.
2. Enter the secret command (which should match the one you have set in the script).
3. If the secret command is correct, you will be granted admin rights and can access the admin commands.

---

## Example Flow

1. The bot sends a welcome message and prompts players to register.
2. Players send `/register` and provide their details.
3. After registration ends, the bot prompts the admin to start matching players.
4. Admin sends `/match_players`, and the bot randomly assigns Secret Santa matches.
5. Admin can then send messages to all players using `/send_announcement`.

---

## Security

- Ensure that the **secret command** is not shared publicly.
- The bot will only grant admin rights to users who correctly authenticate using the secret command.

---


