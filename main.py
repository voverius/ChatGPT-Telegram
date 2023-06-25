
import os
import json
from pathlib import Path

from Modules.ChatGPT import *
from Modules.Telegram import *


def main():

    root = os.path.dirname(os.path.abspath(__file__))
    path = Path(f'{root}\\UserData\\Information.json')

    with open(path, 'r') as fileObject:
        info = json.load(fileObject)

    gpt = ChatGPT(token=info['logins']['openai'])
    telegram = TelegramGPT(token=info['logins']['telegram']['token'],
                           users=info['logins']['telegram']['users'],
                           gpt=gpt)

    telegram()
    return


if __name__ == '__main__':
    main()
