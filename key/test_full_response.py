import requests
import json
import uuid
import random

def test_full_login(uid, pw):
    print(f"\n[*] ANALYZING FULL API RESPONSE FOR: {uid} | {pw}")
    print("-" * 50)
    
    session = requests.Session()
    
    # Payload đầy đủ nhất để kéo mọi dữ liệu có thể
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
        'generate_session_cookies': '1',
        'generate_analytics_claim': '1',
        'generate_machine_id': '1',
        'method': 'auth.login',
        'fb_api_req_friendly_name': 'authenticate',
        'fb_api_caller_class': 'com.facebook.account.login.protocol.Fb4aAuthHandler',
    }
    
    headers = {
        'User-Agent': "[FBAN/FB4A;FBAV/443.0.0.30.117;FBBV/545043810;FBDM/{density=2.0,width=720,height=1280};FBLC/en_US;FBRV/546418861;FBCR/Verizon;FBMF/samsung;FBBD/samsung;FBPN/com.facebook.katana;FBDV/SM-G950F;FBSV/9;FBOP/1;FBCA/armeabi-v7a:armeabi;]",
        'Content-Type': 'application/x-www-form-urlencoded',
        'Host': 'graph.facebook.com',
        'X-FB-Connection-Type': 'MOBILE.LTE',
        'X-FB-HTTP-Engine': 'Liger'
    }

    try:
        response = session.post('https://b-graph.facebook.com/auth/login', data=data, headers=headers)
        
        print(f"[!] HTTP Status: {response.status_code}")
        print("\n[+] FULL JSON DATA FROM FACEBOOK:")
        print("=" * 50)
        
        # In toàn bộ kết quả JSON đẹp đẽ để Anh Tiến soi
        full_result = response.json()
        print(json.dumps(full_result, indent=4, ensure_ascii=False))
        print("=" * 50)
        
        if 'session_cookies' in full_result:
            print("\n[✓] Có Cookie trong mẻ này!")
        if 'access_token' in full_result:
            print("[✓] Có Access Token mới!")
            
    except Exception as e:
        print(f"[×] Error: {e}")

if __name__ == "__main__":
    try:
        print("=== FB API FULL DATA ANALYZER ===")
        u = input("[?] Nhap UID: ").strip()
        p = input("[?] Nhap Pass: ").strip()
        if u and p:
            test_full_login(u, p)
        else:
            print("[!] Vui long khong de trong!")
        input("\n[XONG] Nhan Enter de thoat...")
    except Exception as e:
        print(f"\n[!] Da xay ra loi: {e}")
        input("Nhan Enter de tiep tuc...")
