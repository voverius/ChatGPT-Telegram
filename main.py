
from Modules.ChatGPT import *
from Modules.Telegram import *
from Modules.Credentials import *


def main():

    # Get required credentials
    credo = Credentials(keys=Credentials.GetTokenNames(classes=[ChatGPT, TelegramGPT]))

    # Initialize GPT instance
    gpt = ChatGPT(credo=credo)
    telegram = TelegramGPT(credo=credo, gpt=gpt)

    # Run telegram bot indefinitely
    telegram()

    return


if __name__ == '__main__':
    main()
