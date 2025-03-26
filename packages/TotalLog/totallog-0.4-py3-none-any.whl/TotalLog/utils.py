from datetime import datetime
import inspect


class Fore:
    BLACK = "\x1b[30m"
    RED = "\x1b[31m"
    GREEN = "\x1b[32m"
    YELLOW = "\x1b[33m"
    BLUE = "\x1b[34m"
    MAGENTA = "\x1b[35m"
    CYAN = "\x1b[36m"
    WHITE = "\x1b[37m"
    RESET = "\x1b[39m"
    LIGHTBLACK_EX = "\x1b[90m"
    LIGHTRED_EX = "\x1b[91m"
    LIGHTGREEN_EX = "\x1b[92m"
    LIGHTYELLOW_EX = "\x1b[93m"
    LIGHTBLUE_EX = "\x1b[94m"
    LIGHTMAGENTA_EX = "\x1b[95m"
    LIGHTCYAN_EX = "\x1b[96m"
    LIGHTWHITE_EX = "\x1b[97m"


class Back:
    BLACK = "\x1b[40m"
    RED = "\x1b[41m"
    GREEN = "\x1b[42m"
    YELLOW = "\x1b[43m"
    BLUE = "\x1b[44m"
    MAGENTA = "\x1b[45m"
    CYAN = "\x1b[46m"
    WHITE = "\x1b[47m"
    RESET = "\x1b[49m"
    LIGHTBLACK_EX = "\x1b[100m"
    LIGHTRED_EX = "\x1b[101m"
    LIGHTGREEN_EX = "\x1b[102m"
    LIGHTYELLOW_EX = "\x1b[103m"
    LIGHTBLUE_EX = "\x1b[104m"
    LIGHTMAGENTA_EX = "\x1b[105m"
    LIGHTCYAN_EX = "\x1b[106m"
    LIGHTWHITE_EX = "\x1b[107m"

B = Back()
F = Fore()

def add_log(log: str, format: str, filename: str, lvlname: str, line: int, log_format: bool):
    with open(filename, "a") as file:
        file.write(de_format(log, format, lvlname, line, log_format) + "\n")

def de_format(log: str, format: str, lvlname: str, line: int, log_format: bool):
    now = datetime.now()
    if log_format:
        log_format_list = {"%(lvlname)s": lvlname, "%(line)s": str(line), "%(asctime)s": str(now)}
        for key, value in log_format_list.items():
            log = log.replace(key, value)
    format_list = {"%(asctime)s": str(now), "%(lvlname)s": lvlname, "%(message)s": log, "%(line)s": str(line)}
    for key, value in format_list.items():
        format = format.replace(key, value)
    return format

def del_all_data(filename: str):
    with open(filename, "w") as file:
        file.write("")

def evaluate_expression(match):
    # Извлекаем математическое выражение из группы
    expression = match.group(1)
    try:
        # Вычисляем выражение и возвращаем результат
        result = eval(expression)
        return str(result)  # Преобразуем результат в строку без скобок
    except Exception as e:
        raise AttributeError(f"Error in expression: {e}")


def end_code(self):
    if self.filename:
        add_log("END CODE", "%(message)s", self.filename, "", 0, False)

def find_str():
    frame = inspect.currentframe().f_back.f_back
    return frame.f_lineno