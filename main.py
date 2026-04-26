import requests
from test import spamcall2
from a import spamcall1
from spamsms import spamcall3
from view import spamcall4
from spamcaller import spamcall5
import concurrent.futures

# API URLs từ call1 đến call7
API_CALLS = [
    "https://traodoituongtac.click/call/call1.php?phone={sdt}&solan={solan}",
    "https://traodoituongtac.click/call/call2.php?phone={sdt}&solan={solan}",
    "https://traodoituongtac.click/call/call3.php?phone={sdt}&solan={solan}",
    "https://traodoituongtac.click/call/call4.php?phone={sdt}&solan={solan}",
    "https://traodoituongtac.click/call/call5.php?phone={sdt}&solan={solan}",
    "https://traodoituongtac.click/call/call6.php?phone={sdt}&solan={solan}",
    "https://traodoituongtac.click/call/call7.php?phone={sdt}&solan={solan}",
]

def call_single_api(api_url: str, sdt: str, solan: int, api_index: int):
    """Gọi một API riêng lẻ"""
    url = api_url.format(sdt=sdt, solan=solan)
    try:
        response = requests.get(url, timeout=10)
        return {
            'api_index': api_index + 1,
            'url': url,
            'success': True,
            'response': response.json() if response.text else {"status": "success"},
            'status_code': response.status_code
        }
    except Exception as e:
        return {
            'api_index': api_index + 1,
            'url': url,
            'success': False,
            'error': str(e)
        }

def call_all_apis(sdt: str, solan: int, use_concurrent: bool = True):
    """Gọi tất cả các API từ call1 đến call7"""
    results = []
    
    if use_concurrent:
        # Chạy đồng thời các API để tăng tốc độ
        with concurrent.futures.ThreadPoolExecutor(max_workers=7) as executor:
            futures = [
                executor.submit(call_single_api, api_url, sdt, solan, idx)
                for idx, api_url in enumerate(API_CALLS)
            ]
            for future in concurrent.futures.as_completed(futures):
                results.append(future.result())
    else:
        # Chạy tuần tự
        for idx, api_url in enumerate(API_CALLS):
            result = call_single_api(api_url, sdt, solan, idx)
            results.append(result)
    
    return results

def call_apis_sequential(sdt: str, solan_per_api: int):
    """Gọi lần lượt từng API, mỗi API gọi nhiều lần"""
    total_calls = 0
    successful_calls = 0
    
    for api_idx, api_url in enumerate(API_CALLS, 1):
        print(f"\n  📞 Đang gọi API call{api_idx}...")
        
        for i in range(solan_per_api):
            try:
                url = api_url.format(sdt=sdt, solan=1)
                response = requests.get(url, timeout=10)
                total_calls += 1
                
                if response.status_code == 200:
                    successful_calls += 1
                    print(f"    ✅ Call{api_idx} - Lần {i+1}: Thành công (Status: {response.status_code})")
                else:
                    print(f"    ❌ Call{api_idx} - Lần {i+1}: Thất bại (Status: {response.status_code})")
                    
            except Exception as e:
                total_calls += 1
                print(f"    ❌ Call{api_idx} - Lần {i+1}: Lỗi - {str(e)}")
    
    return total_calls, successful_calls

if __name__ == "__main__":
    print("-" * 40)
    print("      TOOL SPAM CALL/SMS - ENHANCED")
    print("-" * 40)
    
    run_sms = input("Bạn có muốn chạy spam SMS không? (y/n): ").strip().lower() == 'y'
    run_call = input("Bạn có muốn chạy spam call không? (y/n): ").strip().lower() == 'y'
    sdt = input("Nhập số điện thoại: ")
    
    try:
        solan = int(input("Nhập số lần [vòng lặp]: "))
    except ValueError:
        print("Vui lòng nhập số hợp lệ.")
        exit()
    
    # Chọn chế độ call
    call_mode = "sequential"
    if run_call:
        print("\nChọn chế độ gọi API:")
        print("1. Gọi tất cả API (call1-call7) mỗi lần")
        print("2. Gọi tuần tự mỗi API nhiều lần")
        mode_choice = input("Chọn (1/2): ").strip()
        
        if mode_choice == "2":
            call_mode = "multi_per_api"
            try:
                solan_per_api = int(input("Nhập số lần gọi cho mỗi API: "))
            except ValueError:
                solan_per_api = 1
    
    print(f"\n[+] Bắt đầu tiến trình cho số: {sdt}")
    
    sms_modules = [spamcall1, spamcall2, spamcall3, spamcall4]
    total_sms_calls = 0
    total_api_calls = 0
    
    for i in range(1, solan + 1):
        print(f"\n" + "="*20 + f" VÒNG {i} " + "="*20)
        
        # 1. Chạy SMS modules (xoay vòng)
        if run_sms:
            module_idx = (i - 1) % len(sms_modules)
            module_name = ["a.py", "test.py", "spamsms.py", "view.py"][module_idx]
            print(f"[Lần {i}] 1. Đang chạy SMS Module: {module_name}...")
            try:
                sms_modules[module_idx](sdt, 1)
                total_sms_calls += 1
            except Exception as e:
                print(f"Lỗi SMS ({module_name}): {e}")

        # 2. Chạy spamcaller
        if run_call:
            print(f"[Lần {i}] 2. Đang chạy SpamCaller (Tổng hợp API)...")
            try:
                spamcall5(sdt, 1)
            except Exception as e:
                print(f"Lỗi SpamCaller: {e}")

        # 3. Chạy API calls (call1 đến call7)
        if run_call:
            print(f"[Lần {i}] 3. Đang chạy Call APIs (call1-call7)...")
            
            if call_mode == "sequential":
                # Chế độ 1: Gọi tất cả API mỗi lần
                results = call_all_apis(sdt, 1, use_concurrent=True)
                
                # Hiển thị kết quả
                success_count = sum(1 for r in results if r['success'])
                print(f"  📊 Kết quả: {success_count}/7 API thành công")
                
                for result in results:
                    if result['success']:
                        print(f"  ✅ API call{result['api_index']}: Thành công")
                    else:
                        print(f"  ❌ API call{result['api_index']}: Thất bại - {result.get('error', 'Unknown error')}")
                
                total_api_calls += 7
                
            else:  # multi_per_api
                # Chế độ 2: Gọi mỗi API nhiều lần
                total, successful = call_apis_sequential(sdt, solan_per_api)
                total_api_calls += total
                print(f"  📊 Tổng kết API: {successful}/{total} cuộc gọi thành công")

    print("\n" + "="*20 + " HOÀN TẤT " + "="*20)
    print(f"📊 Thống kê tổng quan:")
    if run_sms:
        print(f"  - SMS đã gửi: {total_sms_calls} lần")
    if run_call:
        print(f"  - API calls đã thực hiện: {total_api_calls} lần")
    print("="*40)