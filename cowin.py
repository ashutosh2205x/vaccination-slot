import requests
import time
baseurl = 'https://cdn-api.co-vin.in/api/v2/'
date = time.localtime()
datetoday = str(date.tm_mday) +'-'+str(date.tm_mon)+'-'+ str(date.tm_year)
is_num =False
print('Enter pincode : ')
pincode = input()

try:
    int(pincode)
    is_num = True
except ValueError:
    is_num = False

if is_num:
    header_dict = {'Host': 'cdn-api.co-vin.in', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36','Accept-Language':'hi_IN'}
    r = requests.get(baseurl+'appointment/sessions/public/calendarByPin?pincode='+pincode+'&date='+datetoday,headers=header_dict)

    if r.status_code==200:
        result = r.json()
        
        if len(result['centers'])  > 0 :
            for center in result['centers']:
                if center['sessions'][0]['available_capacity'] > 0 :
                    for details in center['sessions']:
                        print('location :', center['name']+ center['address'], '\n','min_age_limit :', details['min_age_limit'], '\n', 'slots :', details['slots'], '\n', details['available_capacity_dose1'] ,'\n', 'available_capacity_dose2', details['available_capacity_dose2'])
        else:
            print('No Vaccination drive yet')

    else:
       error = r.json()
       print(error['error'])
else:
    print('wrong pincode')