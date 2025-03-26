import builtins
from datetime import datetime
import os
from TotalLog import utils
from TotalLog.utils import *
from typing import Union
import atexit
import traceback

print = builtins.print


class MyPrint:
    """Класс-обертка для print(), добавляющий кастомное поведение"""
    def __init__(self):
        self.time = datetime.now()
        self.prefix = f"{F.GREEN}{self.time} -{F.RESET} "  # Добавляем префикс к каждому выводу

    def __call__(self, *args, **kwargs):
        message = " ".join(map(str, args))  # Объединяем аргументы в строку
        print(self.prefix + message, **kwargs)  # Выводим с префиксом

builtins.print = MyPrint()


class Log:
    def __init__(self):
        """
        static settings
        """
        self.color = "GREEN"
        self.lines = 40
        self.lines_even = True
        self.round = True
        self.filename = "app.log"
        self.filemode = "a"
        self.format = "%(line)s - %(asctime)s - %(levelname)s - %(message)s"
        self.error_color = "RED"
        self.info_color = "LIGHTWHITE_EX"
        self.log_format = True
        self.line = "-"
        # ---------------------settings for code-----------------------------
        atexit.register(self.del_all_data)
        self.color_names = ['GREEN', 'RESET', 'RED', 'YELLOW', 'LIGHTYELLOW_EX', 'LIGHTWHITE_EX', 'BLACK', 'WHITE',
                                 'CYAN', 'LIGHTBLACK_EX', 'LIGHTBLUE_EX', 'LIGHTCYAN_EX', 'LIGHTMAGENTA_EX',
                                 'LIGHTRED_EX', 'MAGENTA']

    def settings(self, lines: int= None, round: str= None, color: str= None, filename: str=None, filemode: str= None, format: str= None, error_color: str=None, info_color: str= None, log_format: bool= None, line: str=None):
        if color and color.upper() not in self.color_names:
            raise AttributeError(f"color: `{color.upper()}` Not found")
        if filemode and filemode not in ['a', 'b']:
            raise AttributeError(f"operator: `{filemode}` Not found in a or b")
        if round and round not in ['>', '<', 'left', 'right']:
            raise AttributeError(f"round operator `{round}` not found in < or > or 'left' or 'right'")
        if error_color and error_color.upper() not in self.color_names:
            raise AttributeError(f"color: `{error_color.upper()}` Not found")
        if info_color and info_color.upper() not in self.color_names:
            raise AttributeError(f"color: `{info_color.upper()}` Not found")
        if line and len(line) != 1:
            raise ValueError("operator line should be 1 symbol")
        self.color = color if color != None else self.color
        self.lines = lines if lines != None else self.lines
        self.lines_even = True if self.lines % 2 == 0 else False
        self.round = (True if round in ["<", 'left'] else False) if round is not None else self.round
        if self.filename != filename and filename and os.path.exists("example.txt"):
            with open(self.filename, 'r') as file:
                text = file.readline()
            utils.del_all_data(self.filename)
            with open(filename, 'w')as file:
                file.write(text)
        self.filename = filename if filename != None else self.filename
        self.filemode = filemode if filemode != None else self.filemode
        self.line = line if line and line != "" else self.line
        if filemode == "a":
            atexit.unregister(self.del_all_data)
        else:
            atexit.register(self.del_all_data)
        self.format = format if format != None else self.format
        self.error_color = error_color if error_color else self.error_color
        self.info_color = info_color if info_color else self.info_color
        self.log_format = log_format if log_format is not None else self.log_format
        return {"static color": self.color, "lines": self.lines, "round": self.round, "filename": self.filename, "filemode": self.filemode, "format": self.format, "error color": self.error_color, "info color": self.info_color, "log format": self.log_format}


    def error(self, error):
        color = getattr(Fore, self.error_color.upper())
        stack = traceback.extract_stack()
        line = stack[-2].lineno
        if self.filename:
            add_log(error, self.format, self.filename,"ERROR", line, self.log_format)
        print(color + de_format(error, self.format, "ERROR", line, self.log_format) + Fore.RESET)

    def info(self, info):
        color = getattr(Fore, self.info_color.upper())
        stack = traceback.extract_stack()
        line = stack[-2].lineno
        if self.filename:
            add_log(info, self.format, self.filename, "INFO", line, self.log_format)
        print(color + de_format(info, self.format, "INFO", line, self.log_format) + Fore.RESET)

    def del_all_data(self):
        del_all_data(self.filename)

    def line_(self, color: str=None):
        if color != None and color.upper() not in self.color_names:
            raise ValueError(f"color: `{color.upper()}` Not found")
        elif color == None:
            color = self.color
        color = getattr(Fore, color.upper())
        print(color + (self.line * self.lines) + utils.F.RESET)

    def rainbow(self, text: str, colors: list=['RED', 'YELLOW', 'GREEN', 'CYAN', 'BLUE', 'MAGENTA']):
        num = 0

        back = ""
        for char in text:
            if char == " ":
                back += " "
                continue
            if num == len(colors):
                num = 0
            back += getattr(utils.F, colors[num].upper()) + char
            num += 1
        return back


    def text(self, msg: Union[str, int], color: str = None) -> Union[bool, str]:
        """
        :param msg: message to send
        :param color: color of rhe message
        :return: False = error
        :colors: GREEN RESET RED YELLOW LIGHTYELLOW_EX LIGHTWHITE_EX BLACK WHITE CYAN LIGHTBLACK_EX LIGHTBLUE_EX LIGHTCYAN_EX LIGHTMAGENTA_EX LIGHTRED_EX MAGENTA
        """
        if color and color.upper() not in self.color_names:
            raise ValueError(f"color: `{color.upper()}` Not found")
        elif color == None:
            color = self.color
        if len(msg) > self.lines:
            raise ValueError(f"The message is to long(max {self.lines} symbols)")
        color = getattr(Fore, color.upper())
        text = ""
        nb = ""
        if self.lines_even:
            if len(msg) % 2 == 0:
                text += (self.line * (int((self.lines - len(msg)) / 2)) + msg)
                nb = self.line * (int((self.lines - len(msg)) / 2))
            else:
                if self.round:
                    text += (self.line * ((int(self.lines - len(msg))) // 2) + msg)
                    nb = self.line * ((int(self.lines - len(msg))) // 2 + 1)
                else:
                    text += (self.line * ((int(self.lines - len(msg))) // 2 + 1) + msg)
                    nb = self.line * ((int(self.lines - len(msg))) // 2)
        else:
            if len(msg) % 2 == 0:
                if self.round:
                    text += (self.line * (int(self.lines) // 2 - 1) + msg)
                    nb = self.line * (int(self.lines) // 2)
                else:
                    text += (self.line * (int(self.lines) // 2) + msg)
                    nb = self.line * (int(self.lines) // 2 - 1)
            else:
                text += self.line * (int(self.lines) // 2) + msg
                nb = self.line * (int(self.lines) // 2)
        text += nb
        print(color + text + Fore.RESET)
        return text

    def super_info(self, msg: Union[str, int], color: str = None) -> Union[bool, str]:
        """
        :param msg: message to send
        :param color: color of rhe message
        :return: False = error
        :colors:GREEN RESET RED YELLOW LIGHTYELLOW_EX LIGHTWHITE_EX BLACK WHITE CYAN LIGHTBLACK_EX LIGHTBLUE_EX LIGHTCYAN_EX LIGHTMAGENTA_EX LIGHTRED_EX MAGENTA
        """
        if color != None and color.upper() not in self.color_names:
            raise ValueError(f"color: `{color.upper()}` Not found")
        elif color == None:
            color = self.color
        if len(msg) > self.lines:
            raise ValueError(f"The message is to long(max {self.lines} symbols)")
        color = getattr(Fore, color.upper())
        text = ""
        nb = ""
        if self.lines_even:
            if len(msg) % 2 == 0:
                text += (self.line * (int((self.lines - len(msg)) / 2)) + msg)
                nb = self.line * (int((self.lines - len(msg)) / 2))
            else:
                if self.round:
                    text += (self.line * ((int(self.lines - len(msg))) // 2) + msg)
                    nb = self.line * ((int(self.lines - len(msg))) // 2 + 1)
                else:
                    text += (self.line * ((int(self.lines - len(msg))) // 2 + 1) + msg)
                    nb = self.line * ((int(self.lines - len(msg))) // 2)
        else:
            if len(msg) % 2 == 0:
                if self.round:
                    text += (self.line * ((int(self.lines - len(msg))) // 2 - 1) + msg)
                    nb = self.line * ((int(self.lines - len(msg))) // 2)
                else:
                    text += (self.line * ((int(self.lines - len(msg))) // 2) + msg)
                    nb = self.line * ((int(self.lines - len(msg))) // 2 - 1)
            else:
                text += self.line * ((int(self.lines - len(msg))) // 2) + msg
                nb = self.line * ((int(self.lines - len(msg))) // 2)
        text += nb
        print(color + (self.line * self.lines) + "\n" + text + "\n" + (self.line * self.lines) + Fore.RESET)
        return text


Loger = Log()