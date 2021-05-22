import requests
import time
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse, Message

app = Flask(__name__)
baseurl = 'https://cdn-api.co-vin.in/api/v2/'
date = time.localtime()
datetoday = str(date.tm_mday) + '-'+str(date.tm_mon)+'-' + str(date.tm_year)
is_num = False


@app.route('/bot', methods=['POST'])
def bot():
    resp = MessagingResponse()
    msg = resp.message()
    incoming_msg = request.values.get('Body', '').lower()
    listresp = []
    msgtoBeSent = ''
    try:
        pincode = int(incoming_msg)
        listresp = cowin(pincode)
        print('listToStr', listresp)
        if len(listresp) > 0:
            for item in listresp:
                if item['status'] == 200:
                    available_slot = 'Location: ' + str(item['location'])+'\n'+'Age_Group: ' + str(item['age'])+'\n' + 'Date: ' + str(item['date'])+'\n'+'Slots: ' + str(
                        item['slots'])+'\n'+'Vaccine: ' + str(item['vaccine'])+'\n' + 'Dose 1: ' + str(item['dose1'])+'\n' + 'Dose 2: ' + str(item['dose2'])+'\n'+'----'
                    available_slot.join('\n')
                    print('item ==>', available_slot)
                    msg.body(available_slot)

                else:
                    msg.body(item['Error'])
        else:
            msg.body('No slots available')
    except ValueError:
        msg.body('Enter a valid pincode')
    return str(resp)


def convertTuple(tup):
    str = ''.join(tup).replace('-', ' - ').replace('PM', 'PM  ')
    return str


def cowin(args):

    response = []
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
                        response.append({'status': 200,
                                         'location':
                                         str(center['name']) +
                                         str(center['address']),
                                         'age': str(details['min_age_limit']),
                                         'date': str(details['date']),
                                         'slots': convertTuple(details['slots']),
                                         'vaccine': str(details['vaccine']),
                                         'dose1': str(details['available_capacity_dose1']),
                                         'dose2': str(details['available_capacity_dose2'])})

        else:
            response.append(
                {'status': 400, 'Error': 'No Vaccination drive yet'})
    else:
        error = r.json()
        err = f'{error["error"]}'
        msg.body(err)
        response.append({'status': 400, 'Error': err})
    return response


if __name__ == '__main__':
    app.run()
