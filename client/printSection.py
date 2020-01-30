import os
from util import *

def printSection(STATE, hasNewMessage = False, welcomeMessage = False):
    terminal_width = os.get_terminal_size().columns
    section = "\n" + "=" * terminal_width + "\n"
    space = ' ' * terminal_width

    print(colored(section, THEME_col, THEME_hi))
    print(colored(space, THEME_col, THEME_hi))
    
    if (welcomeMessage):
        print(colored("Welcome to cnMessage".center(terminal_width), THEME_col, THEME_hi, attrs=[THEME_attr]))
    elif (STATE == "NON_LOGIN"):
        print(colored("(0)Sign Up , (1)Sign In , (2)Change Password , (3)Exit".center(terminal_width), THEME_col, THEME_hi, attrs=[THEME_attr]))
    elif (STATE == "LOGGED"):
        print(colored("(0)Choose Recipient , (1)Log Out".center(terminal_width), THEME_col, THEME_hi, attrs=[THEME_attr]))
    elif (STATE == "MESSAGE"):
        print(colored("(0)Send Messages, (1)Send Files, (2)View Message History, (3)Switch Recipient, (4)Log Out".center(terminal_width), THEME_col, THEME_hi, attrs=[THEME_attr]))
    elif (STATE == "EXIT"):
        print(colored("~See you next time~".center(terminal_width), THEME_col, THEME_hi, attrs=[THEME_attr]))
        
    print(colored(space, THEME_col, THEME_hi))
    print(colored(section, THEME_col, THEME_hi))

    if (hasNewMessage):
        print(colored("*** You have new messages ***\n".center(terminal_width), NOTIFY_col, attrs=[NOTIFY_attr]))