import requests
import time
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message

app = Flask(__name__)
baseurl = 'https://cdn-api.co-vin.in/api/v2/'
date = time.localtime()
datetoday = str(date.tm_mday) + '-'+str(date.tm_mon)+'-' + str(date.tm_year)
is_num = False
resp = MessagingResponse()
msg = resp.message()


@app.route('/bot', methods=['POST'])
def bot():
    incoming_msg = request.values.get('Body', '').lower()

    responded = False
    try:
        pincode = int(incoming_msg)
        print('pincode==>', pincode)
        cowin(pincode)
    except ValueError:
        print('CONVERSION ERROR')
        msg.body('Enter a valid pincode')
    return str(resp)


def convertTuple(tup):
    str = ''.join(tup).replace(' ', '\n')
    return str


def cowin(args):
    pincode = str(args)
    print('cowin pin', pincode)
    resp = MessagingResponse()
    msg = resp.message()
    header_dict = {'Host': 'cdn-api.co-vin.in',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36', 'Accept-Language': 'hi_IN'}
    r = requests.get(baseurl+'appointment/sessions/public/calendarByPin?pincode=' +
                     pincode+'&date='+datetoday, headers=header_dict)
    if r.status_code == 200:
        print('api res ok')
        result = r.json()
        if len(result['centers']) > 0:
            for center in result['centers']:
                if center['sessions'][0]['available_capacity'] > 0:
                    for details in center['sessions']:
                        location = 'Location : ' + \
                            str(center['name']) + str(center['address'])+'\n'
                        age = 'Age :' + str(details['min_age_limit'])+'\n'
                        slot = 'Slot : ' + convertTuple(details['slots'])+'\n'
                        d1 = str(details['available_capacity_dose1'])+'\n'
                        d2 = str(details['available_capacity_dose2'])+'\n'
                        print(location, age, slot, d1, d2)
                        info = location + age + slot
                        msg.body('info')
                        # slots = ('Location :', center['name'] + center['address'], '\n', 'Age Group :', details['min_age_limit'], '\n', 'Slots :',
                        #          details['slots'], '\n', 'DOSE 1 :', details['available_capacity_dose1'], '\n', 'DOSE 2:', details['available_capacity_dose2'])
                        # msg.body(info)
        else:
            msg.body('No Vaccination drive yet')
    else:
        error = r.json()
        err = f'{error["error"]}'
        print('api res not ok', err)
        msg.body(err)

    return str(resp)


if __name__ == '__main__':
    app.run()
