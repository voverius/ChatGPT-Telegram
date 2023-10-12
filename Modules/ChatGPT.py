
import openai
import datetime as dt


class ChatGPT:

    """This is an instance for communicating with the Chat-GPT API"""

    # Tracking
    fn = 'ChatGPT'

    # Public
    sessionTokens = 0                   # Integer       How many tokens used in the session
    conversationTokens = 0              # Integer       How many tokens used in this chat
    age = dt.timedelta(hours=2)         # TimeDelta     Memory cut-off
    token_names = ['OPENAI_KEY']        # List          Required keys

    # Private
    _character = ''                     # String        Prompt for how chat should behave
    _memory = False                     # Boolean       Keep memory of the conversation
    _history = None                     # List          The history of the conversation
    _model = 'gpt-3.5-turbo'            # String        Which model to use

    """
    # #############################################################################################
    # -----------------------------------   INITIALIZE   ------------------------------------------
    # #############################################################################################
    """

    def __init__(self, credo):

        """
        :param credo:           Class       Credentials class with token value

        -------------------------------------------------------------------------------------------
        Description:            This initializes the ChatGPT instance.
        """

        openai.api_key = credo.credentials[self.token_names[0]]
        self.Reset()

    # --------------------------------------   CALL   ---------------------------------------------

    def __call__(self, message):

        """
        :param message:         String          The actual prompt

        :return:                String          The answer from the GPT model.

        -------------------------------------------------------------------------------------------
        Description:            This method calls the GPT model API and returns the response.
        """

        ct = dt.datetime.now()
        message = str(message) if not isinstance(message, str) else message

        if len(self.history) > 1:
            first = self.ClearMemory()
            latest = {time: query for time, query in list(self.history.items())[1:] if
                      (ct - time).total_seconds() < self.age.total_seconds()}
            self._history = {**first, **latest}

        self._history.update({self.Timestamp(): {'role': 'user', 'content': message}})

        try:
            response = openai.ChatCompletion.create(
                model=self.model,
                messages=list(self._history.values()),
            )
        except:
            self._history = self.ClearMemory()
            return '*<SYSTEM>*   Error occurred, try again.'

        self.sessionTokens += response['usage']['total_tokens']
        self.conversationTokens += response['usage']['total_tokens']

        reply = response['choices'][0]['message']['content']

        if self.memory:
            self._history.update({self.Timestamp(): {'role': 'assistant', 'content': reply}})
        else:
            self._history = self.ClearMemory()

        return reply

    # #############################################################################################
    # -----------------------------------   PROPERTIES   ------------------------------------------
    # #############################################################################################

    @property
    def model(self):
        return self._model

    @property
    def memory(self):
        return self._memory

    @property
    def history(self):
        return self._history

    @property
    def character(self):
        return self._character

    """
    # #############################################################################################
    # -------------------------------------   METHODS   -------------------------------------------
    # #############################################################################################
    """

    def Reset(self):

        """Reset to standard state"""

        self.Persist()
        self.StandardCharacter()

        self.conversationTokens = 0
        self._history = {dt.datetime.now(): {'role': 'system', 'content': self.character}}
        return

    def SetCharacter(self, message):

        """
        :param message:         String      Prompt message to set the GPT

        -------------------------------------------------------------------------------------------
        Description:            This updates the GPT profile.
        """

        self._character = message
        return

    def Persist(self):

        """Turn on the memorization of the conversation"""

        self._memory = True
        return

    def StandardCharacter(self):
        self._character = 'You are an assistant worthy of a european billionaire. You are smart, '\
                          'witty and most importantly you are are brief, exact and concise.'
        return

    def ClearMemory(self):

        return {time: query for time, query in list(self.history.items())[:1]}

    def Timestamp(self):
        return dt.datetime.now() + dt.timedelta(microseconds=len(self.history))

    """
    # #############################################################################################
    # -------------------------------------   IMPLIED   -------------------------------------------
    # #############################################################################################
    """

    def __repr__(self):
        return f'ChatGPT instance'
