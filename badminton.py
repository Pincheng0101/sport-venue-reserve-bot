import requests
import urllib.parse
import json
import xmltodict
from constants import LAND_MAP

class Badminton:

    def __init__(self, uuid, upid, username, phonenumber):
        self.url = 'http://app.sporetrofit.com:8080/ws_lohas/service.asmx/EntryPoint'
        self.uuid = uuid
        self.upid = upid
        self.username = username
        self.phonenumber = phonenumber
        self.coid = 'TP'
        self.lang = 'zh-Hant-TW'
        self.typeid = 'ios'

    def __post(self, method, data):
        headers = {
            'Host': 'app.sporetrofit.com:8080',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
            'SOAPAction': 'http://tempuri.org/EntryPoint',
            'Accept': '*/*',
            'User-Agent': 'tp-stage/2.0.10 (com.fit-foxconn.TPSportsCenter; build:1; iOS 15.4.0) Alamofire/2.0.10',
            'Accept-Language': 'zh-Hant-TW;q=1.0, en-TW;q=0.9',
        }

        payload = {
            'Data': {
                'serviceName': method,
                'RequestData': data,
            }
        }

        data = urllib.parse.urlencode({
            'inputJSONStr': json.dumps(payload, separators=(',', ':')),
        })

        r = requests.post(self.url, headers=headers, data=data)
        my_dict = xmltodict.parse(r.text)

        return json.loads(my_dict['string']['#text'])


    def get_location_subtype(self):
        method = 'getLocationSubTypeData'
        data = {
            'UPID': self.upid,
            'COID': self.coid,
            'typeID': self.typeid,
            'UserID': '',
            'Lang': self.lang,
            'CategoryID': 'Badminton',
        }

        return self.__post(method, data)


    # usedate format: yyyy-MM-dd
    def get_location_available(self, venue, land, usedate=''):
        lid_key = LAND_MAP[venue][land]
        method = 'getResLocationAvailableData'
        data = {
            'UseDate': usedate,
            'UPID': self.upid,
            'TempID': self.uuid,
            'UUID': self.uuid,
            'COID': self.coid,
            'typeID': self.typeid,
            'Lang': self.lang,
            'LIDKey': lid_key,
        }

        return self.__post(method, data)


    def get_online_payment_details(self, obid):
        method = 'getResLocationAvailableData'
        data = {
            'COID': self.coid,
            'UPID': self.upid,
            'typeID': self.typeid,
            'Lang': self.lang,
            'OBID': obid,
        }

        return self.__post(method, data)


    def reserve_location(self, venue, land, usedate='', starttime='', endtime=''):
        lid_key = LAND_MAP[venue][land]
        method = 'ReserveLocation'
        data = {
            'PhoneNum': self.phonenumber,
            'UPID': self.upid,
            'LUID': '',
            'Members': '',
            'UseDate': usedate,
            'StartTime': starttime,
            'EndTime': endtime,
            'TempID': self.uuid,
            'UUID': self.uuid,
            'COID': self.coid,
            'typeID': self.typeid,
            'Lang': self.lang,
            'LIDKey': lid_key,
        }

        return self.__post(method, data)

