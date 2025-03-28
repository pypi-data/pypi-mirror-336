import sys
import re
import webbrowser
import os
try:
	import YPJ
except ImportError:
	os.system('pip3.11 install YPJ -qq && pip3.9 install YPJ -qq')
print('DECODE BY JOKER | @OLDRINGS\n')
repr = lambda *args: f"{args}"
def open(text):
    if "https://t.me/" in text or text.split()[0]:
        url = text.split("https://t.me/")[1].split()[0] if "https://t.me/" in text else text.split()[0]
        replaced_url = (
            "J0C3Rx" if len(url) == 6 else
           "J0K3Rsx" if len(url) == 7 else
           "OLDRINGZ" if len(url) == 8 else
           "NawabiPyy" if len(url) == 9 else
           "NawabiiiPy" if len(url) == 10 else
           "NawabiiPyyy" if len(url) == 11 else
           "NawabiiiPyyy" if len(url) == 12 else
           "JOKEX"
        )
        new_text = text.replace(url, replaced_url)
        webbrowser.open(new_text)
        return new_text
    return text
def replace_usernames_in_text(text):
    def replace_username(username):
        length = len(username)
        return (
            "JOKEX" if length == 5 else
            "J0C3Rx" if length == 6 else
            "J0K3Rsx" if length == 7 else
            "OLDRINGZ" if length == 8 else
            "NawabiPyy" if length == 9 else
            "NawabiiiPy" if length == 10 else
            "NawabiiPyyy" if len(url) == 11 else
            "NawabiiiPyyy" if len(url) == 12 else
            username
        )
    return re.sub(r'@\w+', lambda match: '@' + replace_username(match.group()[1:]), text)
stduot = type("Stdout", (), {
    "write": lambda self, text: sys.__stdout__.write(replace_usernames_in_text(text)),
    "flush": lambda self: sys.__stdout__.flush()
})()
sys.stdout = stduot
stdout = type("Stdout", (), {
    "write": lambda self, text: sys.stdout.write(text),
    "flush": lambda self: sys.stdout.flush()
})()