from bardapi import Bard
import os
import requests
# Visit https://bard.google.com/
# F12 for console
# Session: Application → Cookies → Copy the value of __Secure-1PSID cookie.
os.environ['_BARD_API_KEY'] = "aQh0fWc0CrOiP93Bmr03DT1JzI6LOGC1BWx08FrcH7L5lJTJ7rgzDH2XVE-kmyvVmko8yA."


session = requests.Session()
session.headers = {
            "Host": "bard.google.com",
            "X-Same-Domain": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
            "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
            "Origin": "https://bard.google.com",
            "Referer": "https://bard.google.com/",
        }
session.cookies.set("__Secure-1PSID", os.getenv("_BARD_API_KEY")) 
# session.cookies.set("__Secure-1PSID", token) 


bard = Bard(token=token, session=session, timeout=30)
bard.get_answer("Write a story about puppies")['content']


# Continued conversation without set new session
bard.get_answer("What is my last prompt??")['content']

