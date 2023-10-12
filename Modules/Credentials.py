
import os
import inspect
from dotenv import load_dotenv


class Credentials:

    """This is an instance for collecting all required credentials"""

    # Tracking
    fn = 'Credentials'

    # Public
    keys = None                         # List          Required keys
    credentials = None                  # Dictionary    The credentials


    """
    # #############################################################################################
    # -----------------------------------   INITIALIZE   ------------------------------------------
    # #############################################################################################
    """

    def __init__(self, keys=None):

        """
        :param keys:            List        List of keys to get credentials for

        -------------------------------------------------------------------------------------------
        Description:            This initializes the Credentials instance.
        """

        # Initialize variables
        self.keys = []
        self.credentials = {}

        # Load .env file in development environment
        load_dotenv()

        if isinstance(keys, list):
            for key in keys:
                self.Get(key=key)

    """
    # #############################################################################################
    # -------------------------------------   METHODS   -------------------------------------------
    # #############################################################################################
    """

    def Get(self, key):
        
        """
        :param key:             String      Name of the key to be retrieved

        :return:                None        Retreived keys are stored in the main dictionary
        -------------------------------------------------------------------------------------------
        Description:            This gets the keys from environment variables.
        """

        # Retrieve credential from environment variables
        value = os.environ.get(key)
        
        # Error out if it is not available
        if value is None:
            raise ValueError(f"Missing required credential: {key}")
        
        # Check if it is a list, and store
        self.credentials[key] = value.split(', ') if ', ' in value else value

        return

    """
    # #############################################################################################
    # ------------------------------------   FUNCTIONS   ------------------------------------------c
    # #############################################################################################
    """

    @staticmethod
    def GetTokenNames(classes=None):

        """
        :param classes:         List        List of classes to get required tokens from

        :return:                List        List of required token names
        -------------------------------------------------------------------------------------------
        Description:            This get the required token names from the classes.
        """

        # Create unique set of required token names
        token_names = set()

        for class_x in classes:
            if inspect.isclass(class_x):

                # Check if the has specified required tokens
                required = getattr(class_x, 'token_names', None)

                # If it has, add it to the list
                if required:
                    if isinstance(required, str):
                        token_names.add(required)
                    elif isinstance(required, (list, tuple)):
                        token_names.update(required)

        return list(token_names)


    """
    # #############################################################################################
    # -------------------------------------   IMPLIED   -------------------------------------------
    # #############################################################################################
    """

    def __repr__(self):
        return f'Credentials instance'
