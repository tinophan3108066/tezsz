import requests

# URL of the registration page
url = 'https://moneyveo.vn/vi/registernew/'

# Headers to mimic a browser request
headers = {
 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
 'Accept-Language': 'vi,en-US;q=0.9,en;q=0.8,fr-FR;q=0.7,fr;q=0.6',
 'Accept-Encoding': 'gzip, deflate, br',
 'Connection': 'keep-alive',
 'Upgrade-Insecure-Requests': '1',
 'Cache-Control': 'max-age=0',
 'Sec-Fetch-Dest': 'document',
 'Sec-Fetch-Mode': 'navigate',
 'Sec-Fetch-Site': 'none',
 'Sec-Fetch-User': '?1',
 'TE': 'trailers',
}

# Cookies to include in the request
cookies = {
 'language': 'vi',
 'UserTypeMarketing': 'L0',
 'GN_USER_ID_KEY': '0a15f5eb-570b-449d-92fd-0b931e2a21b4',
 '__sbref': 'fnqfucsksnpqhiowlatkofrqmuiqshvxowhnsduj',
 'privacyAgreementAccepted': 'true',
 'ASP.NET_SessionId': 'znrbqjdptmlrhtqkhps3jbx4',
 'RequestData': 'e133c835-c77c-494a-a060-952e15a493a6',
 'LeadPartner31B92E50BCF7EFC6A1': 'lgid=6&lpid=utm_medium%3daffiliate%26utm_campaign%3dgoodaff%26utm_term%3d9259%26click_id%3de0bf1503d794e3f5672096a79c3b2d5b',
 'ET31B92E50BCF7EFC6A1': '-8584266338153276779',
 '_gcl_au': '1.1.941717305.1772381170',
 '_gid': 'GA1.2.1724867957.1772381171',
 'UserMachineId_png': '8d933ec8-5185-4302-9fa9-3b801f8afdc3',
 'UserMachineId_etag': '8d933ec8-5185-4302-9fa9-3b801f8afdc3',
 'UserMachineId_cache': '8d933ec8-5185-4302-9fa9-3b801f8afdc3',
 'UserMachineId': '8d933ec8-5185-4302-9fa9-3b801f8afdc3',
 'TrafficSourceData': 'Guid=caa04ed5-ea82-43d2-8997-cfa86edb5baf&Tied=&Sign=-1815591120&Pdt=639079803507749746',
 'cf_clearance': 'qHNl._JIBZPHs2xiB4I990l44jjuVq484Nc9VfSDPIc-1772381139-1.2.1.1-rytKDXDz6GeOfVXDAmrSmKTasRm94NYgJ.10jPJvRxcl8beS2LZJGwU_.2BbFO_T7CBj4BT0wK3G6KALo_XX2QLUHDCM2fw6pEjA1JNIUugC2k6sJvgMjmAV5VrVOuEwCZUtOu3SzWMrj0oUuDki1bgbwdw3yGUS4pdJAmZsys36UK9bMFXmayGbnQmK.UtDyhAzsGGeYbHVECE.YzUFWmpil1rjt0K7OGVhex.xBPE',
 '_ga': 'GA1.2.1814966347.1746363167',
 '_ga_LCPCW0ZYR8': 'GS2.1.s1772381170$o6$g1$t1772381710$j60$l0$h0',
}

# Data to send in the POST request
data = {
 'Phone': '0937576173', # Replace with the desired phone number
 'CaptchaInputText': '302' # Replace with the actual CAPTCHA text
}

# Send the POST request to log the client behavior
response = requests.post('https://moneyveo.vn/vi/registernew/sendsmsjson/', headers=headers, cookies=cookies, data=data)

# Print the response to check if the request was successful
print(response.status_code)
print(response.text)
