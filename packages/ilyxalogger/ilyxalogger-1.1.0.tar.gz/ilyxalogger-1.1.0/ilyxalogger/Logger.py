import datetime
import os

class Colors:
    BLACK = "\033[0;30m"
    RED = "\033[0;31m"
    BG_RED = "\033[41m"
    GREEN = "\033[0;32m"
    BG_GREEN = "\033[42m"
    BROWN = "\033[0;33m"
    BLUE = "\033[0;34m"
    BG_BLUE = "\033[44m"
    PURPLE = "\033[0;35m"
    CYAN = "\033[0;36m"
    LIGHT_GRAY = "\033[0;37m"
    DARK_GRAY = "\033[1;30m"
    LIGHT_RED = "\033[1;31m"
    LIGHT_GREEN = "\033[1;32m"
    YELLOW = "\033[1;33m"
    BG_YELLOW = "\033[43m"
    LIGHT_BLUE = "\033[1;34m"
    LIGHT_PURPLE = "\033[1;35m"
    LIGHT_CYAN = "\033[1;36m"
    LIGHT_WHITE = "\033[1;37m"
    BOLD = "\033[1m"
    FAINT = "\033[2m"
    ITALIC = "\033[3m"
    UNDERLINE = "\033[4m"
    BLINK = "\033[5m"
    NEGATIVE = "\033[7m"
    CROSSED = "\033[9m"
    END = "\033[0m"

class Logger:
    def __init__(self, colorize=True, write_to_logfile=True, log_filename="Logger.log") -> None:
        self.COLORIZE = colorize
        self.TIME_FORMAT = "%d.%m.%Y-%H:%M:%S"
        self.log_filename = log_filename
        self.write_to_logfile = write_to_logfile
        os.system("") # Нужно для отображение цвета в консоли Windows
        if self.write_to_logfile and not os.path.isfile(self.log_filename):
            with open(self.log_filename, "w", encoding="utf-8") as file:
                file.write("")

    def write_to_file(self, text):
        with open(self.log_filename, "a", encoding="utf-8") as file:
            file.write(text + "\n")

    def log_info(self, message, title="Info", color=Colors.BLUE, bg_color=Colors.BLUE):
        time = datetime.datetime.now().strftime(self.TIME_FORMAT)
        if self.COLORIZE:
            parsed_answer = ""
            for i in range (len(message.split("$"))):
                if i % 2 == 0:
                    parsed_answer += message.split("$")[i]
                else:
                    parsed_answer += bg_color + message.split("$")[i] + Colors.END
            print(f"{color}[{time}] - <<{title}>>{Colors.END}   : {parsed_answer}")
        else:
            print(f"[{time}] - <<{title}>>   : {message}")

        if self.write_to_logfile:
            self.write_to_file(f"[{time}] - <<{title}>>   : {message}")

    def log_success(self, message, title="Success", color=Colors.GREEN, bg_color=Colors.GREEN):
        time = datetime.datetime.now().strftime(self.TIME_FORMAT)
        if self.COLORIZE:
            parsed_answer = ""
            for i in range (len(message.split("$"))):
                if i % 2 == 0:
                    parsed_answer += message.split("$")[i]
                else:
                    parsed_answer += bg_color + message.split("$")[i] + Colors.END
            print(f"{color}[{time}] - <<{title}>>{Colors.END}: {parsed_answer}")
        else:
            print(f"[{time}] - <<{title}>>: {message}")
        
        if self.write_to_logfile:
            self.write_to_file(f"[{time}] - <<{title}>>: {message}")
    
    def log_warning(self, message, title="Warning", color=Colors.YELLOW, bg_color=Colors.YELLOW):
        time = datetime.datetime.now().strftime(self.TIME_FORMAT)
        if self.COLORIZE:
            parsed_answer = ""
            for i in range (len(message.split("$"))):
                if i % 2 == 0:
                    parsed_answer += message.split("$")[i]
                else:
                    parsed_answer += bg_color + message.split("$")[i] + Colors.END
            print(f"{color}[{time}] - <<{title}>>{Colors.END}: {parsed_answer}")
        else:
            print(f"[{time}] - <<{title}>>: {message}")
        
        if self.write_to_logfile:
            self.write_to_file(f"[{time}] - <<{title}>>: {message}")
    
    def log_error(self, message="", error=None, title="Error", color=Colors.RED, bg_color=Colors.RED, solution=None):
        time = datetime.datetime.now().strftime(self.TIME_FORMAT)
        if error and title == "Error":
            title = error.__class__.__name__
            if not message:
                message = str(error)
        if self.COLORIZE:
            parsed_answer = ""
            for i in range (len(message.split("$"))):
                if i % 2 == 0:
                    parsed_answer += message.split("$")[i]
                else:
                    parsed_answer += bg_color + message.split("$")[i] + Colors.END
            if solution:
                print(f"{color}[{time}] - <<{title}>>{Colors.END}  : {parsed_answer}. {Colors.BOLD}\nPotential Solution:{Colors.END} {Colors.CYAN}{solution}{Colors.END}")
            else:
                print(f"{color}[{time}] - <<{title}>>{Colors.END}  : {parsed_answer}")
        else:
            if solution:
                print(f"[{time}] - <<{title}>>  : {message}. \nPotential Solution: {solution}")
            else:
                print(f"[{time}] - <<{title}>>  : {message}")
        
        if self.write_to_logfile:
            if solution:
                self.write_to_file(f"[{time}] - <<{title}>>  : {message}. Potential Solution: {solution}")
            else:
                self.write_to_file(f"[{time}] - <<{title}>>  : {message}")
