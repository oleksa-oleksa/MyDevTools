import keyring
import os
import logging
import sys

"""
Secrets Service Keyring Tool Documentation:

This tool provides a way to securely store and retrieve passwords for specific services and users. To use the tool,
run the script with the appropriate SECURITY_MODE value. The 'get' mode will retrieve the password for the given
service and user from the Keyring, while the 'set' mode will securely store a password for the given service and
user in the Keyring.

Usage:
python keyring_tool.py SECURITY_MODE=<SECURITY_MODE>

SECURITY_MODE must be provided from either the command line argument or the environment variable. 

SECURITY_MODE: [set, get]

For 'SECURITY_MODE=get' use environment variables SERVICE and USER to obtain a password.
For 'SECURITY_MODE=set' use additionally environment variable PASSWORD to securely save <password> for <username> and <service>.

To use the 'get' mode, set the SECURITY_MODE value to 'get' and set the environment variables SERVICE and USER to
the appropriate values for the password to retrieve.

To use the 'set' mode, set the SECURITY_MODE value to 'set' and set the environment variables SERVICE, USER, and
PASSWORD to the appropriate values for the password to store securely.

Examples:
- To retrieve a password for the 'service1' and 'user1' values:
    python keyring_tool.py SECURITY_MODE=get SERVICE=service1 USER=user1

- To store a password for the 'service2' and 'user2' values:
    python keyring_tool.py SECURITY_MODE=set SERVICE=service2 USER=user2 PASSWORD=mypassword
"""


def get_env_variable(env_variable_name: str):
    """
    Get the value of an environment variable.
    Parameters:
    - env_variable_name (str): The name of the environment variable to retrieve.
    Returns:
    - str or None: The value of the environment variable, or None if it does not exist.
    If the specified environment variable does not exist, an error message will be printed
    """
     # if variable does not exist, 'os.getenv()' returns 'None'
    env_variable_value = os.getenv(env_variable_name)

    if env_variable_value is None:
        print(f"ValueError: {env_variable_name} environment variable is not set")
        return
    
    print(f"The value of {env_variable_name} is {env_variable_value}")    
    return env_variable_value


def set_data(SECURITY_MODE: str):
    """
    Set the password for obtained service_name and user and save in Keyring backend
    Preconditions: Environment variables SECURITY_MODE must be set to "set", 
                   Set environment variables SERVICE and USER to the appropriate 
                   values for the PASSWORD to retrieve.
    Parameters:
    - SECURITY_MODE (str): must be set to "set". Otherwise function exits
    Returns:
    - None or error: After the pasword was saved returns "None". 
                     In case of error the error messages will be created by get_env_variable and keyring. 
    """
    if SECURITY_MODE=="set":
        logging.info("SET: Using environment variable as <username> for setting <pasword> for <service>")
        USER = get_env_variable("USER")     
        PASS = get_env_variable("PASS")
        SERVICE = get_env_variable("SERVICE")

        """
        The obtained above environment variables are parameters to be passed into Keyring function:
        :param service_name: string that identifies the service name that password is associated with
        :param username: string identifies the user of the service
        :param password: string identifies the pasword that is to store in Keyring
        """
        keyring.set_password(service_name=SERVICE, username=USER, password=PASS)
        print("Password saved!")
    else:
        print("Wrong SECURITY_MODE!")


def get_data(SECURITY_MODE: str):
    """
    Get the password for obtained service_name and user and save in Keyring backend
    Preconditions: Environment variables SECURITY_MODE must be set to "get", 
                   variables USER and SERVICE must be provided with correct information 
                   to obtain the corresponding PASSWORD
    Parameters:
    - SECURITY_MODE (str): must be set to "set". Otherwise function exits
    Returns:
    - str or error: Password returned if password was securely saved in Keyring backend for provided SERVICE and USER
                    In case password does not exists or environment variables are not set, 
                    an error message will be created by get_env_variable and keyring.                    
    """
    if SECURITY_MODE=="get":
        logging.info("LOGIN: Using environment variables <service> and <username> to get saved <pasword>")
        USER = get_env_variable("USER")     
        SERVICE = get_env_variable("SERVICE")

        PASS = keyring.get_password(service_name=SERVICE, username=USER)
        if PASS is None:
            logging.info("Password value not found!")
            raise ValueError("No login data in Keyring, can not continue. Aborting...")
        print(f"Keyring password: {PASS}")
        return PASS
    else:
        print("Wrong SECURITY_MODE!")


def print_mode_error_information():
    print("SECURITY_MODE argument is missed is incorrect!")
    print_usage_information()


def print_usage_information():
    print("Usage: python <script_name.py> SECURITY_MODE=<SECURITY_MODE>")
    print("SECURITY_MODE: [set, get]")
    print("For 'SECURITY_MODE=get' use environment variables SERVICE and USER to obtain a password")
    print("For 'SECURITY_MODE=set' use additionally environment variable PASSWORD to save securely <password> for <username> and <service>")


def load_security_mode():
    """
    Load the security mode from either the command line argument or the environment variable.

    Returns:
    str: The security mode value obtained from either the command line argument or the environment variable.
         Returns None if the security mode value cannot be obtained from both sources.
    """
    SECURITY_MODE = None
    # first try whether SECURITY_MODE was passed as argument from command line
    # case for single script executing
    for arg in sys.argv[1:]:
        if arg.startswith("SECURITY_MODE="):
            SECURITY_MODE = arg.split("=")[1]

    # if SECURITY_MODE is not passed from command line, try to get it from enviroment 
    # case for asseccing secrets from controller inside container
    if SECURITY_MODE is None:
        SECURITY_MODE = get_env_variable("SECURITY_MODE")
    
    return SECURITY_MODE

def select_security_mode(SECURITY_MODE: str):
    """
    Selects the appropriate function based on the given security mode value.

    The function checks if the given security mode value matches the keys in the SECURITY_MODE_SWITCH dictionary.
    If there is a match, it executes the corresponding function. If not, it prints an error message.

    Args:
    SECURITY_MODE (str): The security mode value to select the appropriate function for.

    Returns:
    None
    """
    SECURITY_MODE_SWITCH = {
        "get": get_data,
        "set": set_data,
    }

    if SECURITY_MODE in SECURITY_MODE_SWITCH:
        SECURITY_MODE_SWITCH[SECURITY_MODE](SECURITY_MODE)
    else:
        print_mode_error_information()


def main():
    """
    Main function for the Keyring tool.

    This function calls several helper functions to provide information on how to use the Keyring tool,
    loads the security mode value from either the command line argument or the environment variable,
    and selects the appropriate function based on the given security mode value.

    Returns:
    None
    """

    print("Tool for Keyring.")
    print_usage_information()

    SECURITY_MODE = load_security_mode()
    select_security_mode(SECURITY_MODE)


if __name__ == "__main__":
    main()