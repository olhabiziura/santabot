# Secret Santa Bot

This project is a **Secret Santa** game assistant built using Python and the `aiogram` library, which is designed for building Telegram bots. The bot helps organize the Secret Santa game, manage player registration, match players, and provide an interface for participants to interact with their assigned Secret Santa anonymously.

### Features:
- **Admin Functions:**
  - Start and finish registration.
  - Manage player information (view, delete).
  - Send announcements to all players.
  - Match players for the Secret Santa game.
  - Reveal Secret Santa pairings and enable player chats.
  - Save and load player data.

- **Player Functions:**
  - Join the game, fill in registration info (name, age, contact, etc.).
  - Ask questions anonymously to their Secret Santa.
  - Receive and reply to messages from their Secret Santa.
  - View their Secret Santa information when the revealing phase begins.

---

## How to Run the Bot

### Prerequisites:
1. Python 3.8+ installed.
2. Install the necessary dependencies:
   - `aiogram` for building the Telegram bot.
   - `pandas` for storing and handling player data.

```bash
pip install aiogram pandas
```

### Steps to Run:
1. Clone or download the repository to your local machine.

2. **Create a new bot on Telegram**:
   - Go to [BotFather](https://core.telegram.org/bots#botfather) on Telegram.
   - Start a chat with BotFather, create a new bot, and get the bot token.

3. **Update the `bot = Bot(token='YOUR_BOT_TOKEN')` line** in the script with your own bot token.

4. **Change the Admin Secret Command**:
   - In the script, locate the variable `ADMIN_SECRET_COMMAND`.
   - Update this variable with a secure code of your choice. This code will be used to authenticate admins and allow them to access the administrative commands.

   Example:
   ```python
   ADMIN_SECRET_COMMAND = 'admin_secret'
   ```

5. **Run the bot**:
   - Open a terminal and navigate to the project folder.
   - Execute the Python script:

```bash
python bot.py
```

6. The bot will now be running and ready to interact with users.

---

## Commands:

- **/start**: Start the bot and view available options (register, rules, etc.).
- **/join**: Join the game by providing your details (name, age, about, contact).
- **/rules**: View the game rules.
- **/my_info**: View your current information in the game.
- **/change**: Change your previously entered details.
- **/ask_question**: Ask a question to your Secret Santa.
- **/who_my_santa**: Reveal who your Secret Santa is.
- **/matching_pairs**: View the matching players for Secret Santa.
- **/start_game**: Start the game after matching players.
- **/begin_revealing**: Allow players to discover their Secret Santa.

**Admin Commands** (after authentication with secret code):
- **/begin_registration**: Start the registration process for the game.
- **/finish_registration**: Finish registration for all players.
- **/admin_message**: Send a message to all players.
- **/show_who_in**: List all players registered for the game.
- **/matching_run**: Start the matching process for Secret Santa.
- **/delete_player**: Remove a player from the game.
- **/save_players**: Save player data to a file.
- **/show_abouts**: View information about all players.

---
## How to Use the Bot

### Registering Players

To register, users simply need to send the `/register` command. The bot will guide them through entering their information.

### Admin Authentication

To access admin functions, enter the **secret command** that you set in the script (e.g., `/admin_secret`). After entering the correct command, you will be granted admin rights.
### How to Authenticate as Admin:

1. When you attempt to use an admin command (e.g., `/begin_registration`), the bot will prompt you for the **secret command**.
2. Enter the secret command (which should match the one you have set in the script).
3. If the secret command is correct, you will be granted admin rights and can access the admin commands.

---

---

## How the Code Works

1. **Player Registration**:
   - When a player joins via `/join`, they provide their information (name, age, etc.).
   - The bot stores this data in the `information` dictionary.
   - The bot allows players to update their details if they want to change anything.

2. **Admin Control**:
   - Admins can start registration with `/begin_registration`, view player lists, send messages to all players, and more.
   - Admins can also run the player matching process, where players are matched to become Secret Santa pairs.
   
3. **Game Interaction**:
   - Once the matching process is complete, players receive details about the person they are buying a gift for (anonymously).
   - Players can message their Secret Santa anonymously and ask questions through the bot.
   - The bot ensures anonymity by sending messages to the intended recipient without revealing the sender's identity.
   
4. **Revealing Phase**:
   - When the game reaches the revealing phase, players can request to know who their Secret Santa is.
   - This phase also allows players to reveal their identities to their Secret Santa.

---

## Data Persistence
- The bot uses a CSV file (`dictionary.csv`) to store player data, which includes their names, ages, contacts, and other information. 
- The player data can be saved and loaded between sessions using the `pandas` library.

---
## Security

- Ensure that the **secret command** is not shared publicly.
- The bot will only grant admin rights to users who correctly authenticate using the secret command.

---
## Troubleshooting

- If you encounter issues with bot permissions or bot not starting, ensure that:
  - Your bot token is correct.
  - The necessary libraries (`aiogram`, `pandas`) are installed.
  - Your bot is added to a Telegram group and has the required permissions.
  - You've updated the secret code to access admin commands.

---

## License
This project is open-source and free to use. If you decide to use or modify it, please give credit to the original creators.

---

Feel free to ask any questions or report bugs via GitHub issues or reach out for further assistance. Happy gaming! 🎁

---



