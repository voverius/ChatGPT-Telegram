
import logging

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters


class TelegramGPT:

    """This is a telegram bot that forwards messages to Chat GPT and returns the response"""

    # Tracking
    fn = 'TelegramGPT'

    # Private
    _users = None                       # List      IDs of approved users
    _character = False                  # Boolean   Flag that character needs to be changed

    # Logging
    logging.basicConfig(format='%(levelname)s | %(asctime)s | %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.INFO)
    logging.getLogger('httpx').setLevel(logging.WARNING)

    """
    # #############################################################################################
    # -----------------------------------   INITIALIZE   ------------------------------------------
    # #############################################################################################
    """

    def __init__(self, token, users, gpt):

        self.gpt = gpt
        self.app = Application.builder().token(token).build()

        self.users = {} if not isinstance(users, dict) else users

        self.app.add_handler(CommandHandler('help', self.Help))
        self.app.add_handler(CommandHandler('start', self.Start))
        self.app.add_handler(CommandHandler('reset', self.Reset))
        self.app.add_handler(CommandHandler('persist', self.Persist))
        # self.app.add_handler(CommandHandler('character', self.Character))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.Talk))

    def __call__(self):
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

    """
    # #############################################################################################
    # -------------------------------------   METHODS   -------------------------------------------
    # #############################################################################################
    """

    async def Start(self, update: Update, _):

        """Return the starting message"""

        name = self.CheckUser(update=update)
        if not name:
            return
        name = '' if isinstance(name, bool) else name
        return await self.Reply(update=update, message=f'Hi {name}, I will be your assistant')

    async def Echo(self, update: Update, _):

        """Be a parrot"""

        if not self.CheckUser(update=update):
            return
        return await self.Reply(update=update, message=update.message.text)

    async def Help(self, update: Update, _):

        """Return the commands available"""

        if not self.CheckUser(update=update):
            return

        message = '*General commands:* \n' \
                  '/Start - Initializes the bot \n' \
                  '/Help - Prints out available info \n' \
                  '/Reset - Reinitialize GPT session \n' \
                  '/Persist - Memorize the current conversation \n' \
                  '/Character - Change the profile of the assistant \n' \

        return await self.Reply(update=update, message=message)

    # --------------------------------------   GPT   ----------------------------------------------

    async def Reset(self, update: Update, _):

        """Turn on the memory for the AI model"""

        if not self.CheckUser(update=update):
            return

        self.gpt.Reset()
        return await self.Reply(update=update, message='*Conversation has been Re-initialized*')

    async def Persist(self, update: Update, _):

        """Turn on the memory for the AI model"""

        if not self.CheckUser(update=update):
            return

        self.gpt.Persist()
        return await self.Reply(update=update, message='*Great, let\'s have a conversation*')

    # -------------------------------------   MASTER   --------------------------------------------

    async def Talk(self, update: Update, _):

        """This method communicates with the Chat GPT instance"""

        if not self.CheckUser(update=update):
            return

        prompt = update.message.text
        if not prompt:
            return

        return await self.Reply(update=update, message=self.gpt(message=prompt))

    def CheckUser(self, update: Update):

        """Check if the user has been approved to use the bot"""

        info = update.to_dict()['message']
        userID = str(info['from']['id'])
        name = str(info['from']['first_name'])

        if userID not in self.users:
            self.Reply(update=update, message=f'Hi {name}, unfortunately I do not know you')
            return False

        return name if name else True

    """
    # #############################################################################################
    # ------------------------------------   FUNCTIONS   ------------------------------------------
    # #############################################################################################
    """

    @staticmethod
    async def Reply(update, message, **kwargs):
        await update.message.reply_text(text=message, parse_mode='markdown', **kwargs)
        return

    """
    # #############################################################################################
    # -------------------------------------   IMPLIED   -------------------------------------------
    # #############################################################################################
    """

    def __repr__(self):
        return f'Telegram Bot'
