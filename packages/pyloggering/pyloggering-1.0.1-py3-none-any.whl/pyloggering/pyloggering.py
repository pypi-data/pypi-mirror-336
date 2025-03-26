
'''

Simple module for logging

'''


import datetime

from datetime import datetime
from colorama import init
from colorama import Fore, Back, Style

init()




time = datetime.now().strftime('%m-%d %H:%M')

    
class color():
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'
    UNDER = "\033[4m"

class Utility():
    prop: str
 
    def create_file(self,name = any,location = any,type = ".log" or ".txt"):
        """
        creating new log file in directory
        """
        if type.find(".") == -1:
                prop = location + "/" + name + "." + type
                file = open(prop, 'a+')
                file.write(f"[ SYST ]  -> | {time} | Start logging now!\n")
                print(Style.BRIGHT+Fore.CYAN + f"[ SYST ]  -> | {time} | Start logging now!" + Style.RESET_ALL)
                self.prop = prop
                return self.prop
        else:
                prop = location + "/" + name + type
                file = open(prop, 'a+')
                file.write(f"[ SYST ]  -> | {time} | Start logging now!\n")
                print(Style.BRIGHT+Fore.CYAN + f"[ SYST ]  -> | {time} | Start logging now!" + Style.RESET_ALL)

                self.prop = prop
                return self.prop

class Log():
    def __init__(self, utility: Utility):
        self.utility = utility
    
    def info(self,text = any, write : bool = True):  
        '''
        printing your text in class [ INFO ]
        and writing to log file (option)
        
        '''

        print(Style.BRIGHT + f"[ INFO ]  -> | {time} | {text}" + Style.RESET_ALL)
        if write == True:
            try:
                file = open(self.utility.prop, 'a+')
                file.write(f"[ INFO ]  -> | {time} | {text}\n")
            except AttributeError:
                self.critical("Log file is not found!",False)
    

            
    def warning(self,text = any, write : bool = True):  
        '''
        printing your text in class [ WARN ]
        and writing to log file (option)
        
        '''
        print(Style.BRIGHT + Fore.YELLOW +  f"[ WARN ]  -> | {time} | {text}" + Style.RESET_ALL)
        if write == True:
            try:
                file = open(self.utility.prop, 'a+')
                file.write(f"[ WARN ]  -> | {time} | {text}\n")
            except AttributeError:
                self.critical("Log file is not found!",False)


            
    def success(self,text = any, write : bool = True):  
        '''
        printing your text in class [ SUCCESS ]
        and writing to log file (option)
        
        '''

        print(Style.BRIGHT + Fore.GREEN +  f"[SUCCESS] -> | {time} | {text}" + Style.RESET_ALL)
        if write == True:
            try:
                file = open(self.utility.prop, 'a+')
                file.write(f"[SUCCESS] -> | {time} | {text}\n")
            except AttributeError:
                self.critical("Log file is not found!",False)

            

    def critical(self,text = any, write : bool = True):  
        '''
        printing your text in class [ CRIT ]
        and writing to log file (option)
        
        '''

        print(Style.BRIGHT+ Fore.RED + color.UNDERLINE +  f"[ CRIT ]  -> | {time} | {text}" + Style.RESET_ALL + color.END)
        if write == True:
            try:
                file = open(self.utility.prop, 'a+')
                file.write(f"[ CRIT ]  -> | {time} | {text}\n")
            except AttributeError:
                print(Style.BRIGHT+ Fore.RED + color.UNDERLINE +  f"[ CRIT ]  -> | {time} | Log file is not found!" + Style.RESET_ALL + color.END)



    def debug(self,text = any, write : bool = True):  
        '''
        printing your text in class [ DEBUG ]
        and writing to log file (option)
        
        '''

        print(Style.BRIGHT + Fore.YELLOW + Style.DIM +  f"[ DEBUG ] -> | {time} | {text}" + Style.RESET_ALL )
        if write == True:
            try:
                file = open(self.utility.prop, 'a+')
                file.write(f"[ DEBUG ] -> | {time} | {text}\n")
            except AttributeError:
                self.critical("Log file is not found!",False)




