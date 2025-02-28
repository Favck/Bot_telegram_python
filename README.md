# Telegram bot on python
This is a bot for guessing numbers. You can play with it as follows: the bot guesses a number from 1 to 100 and you guess it. You can also change the number of tries (default is 5). You can view your statistics. The minus of the bot is that it saves the data not in the database but in a pickle file.
# Setting up a bot in Telegram.

To do so, navigate to the @BotFather bot. Next, create your own bot. Everything will be written there.

Next, you need to create commands for the bot. The following commands should be added for correct operation:

#### /start - if there are problems
#### /help - game rules
#### /cancel - stop the game 
#### /play - start game
#### /stat - show statistics
#### /atemps - change the number of attempts
After adding the commands, launch the bot and good luck!)


# How to run:
## 1. Don't forget to enter your bot's token.
## 2. Commands:
With this command you will download all the libraries you need
```bash
python -m pip install -r requirements.txt 
```
To start the bot, you need to enter this command 
```bash
python Bot.py
```
