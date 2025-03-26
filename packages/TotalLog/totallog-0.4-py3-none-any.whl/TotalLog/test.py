import TotalLog


# 🏁settings:
TotalLog.sett(lines=80, round="left",
              color="MaGeNta",  filename="",
              filemode="a",
              format="%(lvlname)s - %(asctime)s - %(line)s - %(message)s",
              error_color="ReD", info_color="YeLLow",
              log_format=False, line="━"
              )
# Settings 🏁🏁🏁


# 🏁text:
TotalLog.text("text line:16")
TotalLog.text("RED Text line:17", "RED")
# text 🏁🏁🏁


# 🏁info:
# adds to file the info
TotalLog.info("info line:22")
# info 🏁🏁🏁


# 🏁error:
# adds to file the error
TotalLog.error("error")
# error 🏁🏁🏁


# 🏁Fore, Back + print:
# Fore = F, Back = B
print(TotalLog.Fore.YELLOW + "Fore " + TotalLog.Fore.RESET + TotalLog.Back.YELLOW + "Back" + TotalLog.Back.RESET + " line:34")
# to print with out date
TotalLog.print("to print with out date line:37")
# Fore, Back + print 🏁🏁🏁


# 🏁Title:
TotalLog.Title("Titel line:42")
# Title 🏁🏁🏁


# 🏁error_log:
@TotalLog.error_log
def integer(text: str):
    return int(text)
# make error:
TotalLog.print("line:52")
print(integer("hi"))
# with out error:
TotalLog.print("line:55")
print(integer("999"))
# error_log 🏁🏁🏁


# 🏁line:
TotalLog.print("line line:61")
TotalLog.line()
TotalLog.print("RED line line:63")
TotalLog.line("REd")
# line 🏁🏁🏁


# 🏁rainbow:
print(TotalLog.rainbow("Rainbow line:68"))
TotalLog.info(TotalLog.rainbow("Rainbow autor line:69", ['red', 'red', 'yellow', 'yellow', 'green', 'green', 'cyan', 'cyan', 'blue', 'blue', 'magenta', 'magenta']))
# rainbow 🏁🏁🏁
