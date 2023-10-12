
# ChatGPT Telegram Bot
## Description

The ChatGPT Telegram Bot functions as a personal assistant using the capabilities of OpenAI's 
ChatGPT. Designed to address a broad spectrum of queries, it offers assistance via Telegram. 
Users have the flexibility to run the bot either as a standalone application or within a 
containerized environment.


## Prerequisites
- A registered Telegram bot. Follow [this guide](https://core.telegram.org/bots#6-botfather) for 
  comprehensive instructions for obtaining a bot token from BotFather.
- A specific Telegram user ID. [This tool](https://www.alphr.com/find-telegram-user-id/) will 
  help to find it out.
- An active API key from OpenAI dedicated for ChatGPT usage.
- The Python environment, set according to the directives in the `requirements.txt` file.
- Docker desktop is needed if wanted to launch as a container.


## Setup
### Development
1. Clone the repository.
2. Create a `.env` file in the root directory with the following variables:
```
OPENAI_KEY=<Open AI API Key>
TELEGRAM_BOT_TOKEN=<Telegram bot token>
APPROVED_USERS=<Telegram user ID>
```
3. Install the required Python packages:
```
pip install -r requirements.txt
```
4. Run the bot:
```
python main.py
```

### Production
1. Pull the image from docker hub:
```
docker pull voverius/chatgpt
```
2. Run the container with provided environment variables:
```
docker run -d -e OPENAI_KEY=<Open AI API Key> -e TELEGRAM_BOT_TOKEN=<Telegram bot token> -e 
APPROVED_USERS=<Telegram user ID> chatgpt
```


## Usage
Once the bot is running, you can communicate with it on Telegram. The following commands are 
supported:

- `/Start` - Initializes the bot.
- `/Help` - Provides information about available commands.
- `/Reset` - Reinitialize the GPT session.
- `/Persist` - Memorize the current conversation.
- `/Character` - Change the profile of the assistant.

For other inquiries, simply message the bot, and it'll respond as a chatbot.


## Release Notes
### Version 0.1.0
Initial release with basic functionality.
