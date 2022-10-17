# -*- coding: utf-8 -*-

import json
import time
from badminton import Badminton


if __name__ == '__main__':
    badminton = Badminton(
        uuid='',
        upid='',
        username='',
        phonenumber='',
    )

    venue = '中山'
    land = '4F羽球A'
    date = '2022-10-27'
    start_time = '07:00'
    end_time = '08:00'

    while True:
        result = badminton.reserve_location(venue, land, date, start_time, end_time)
        if result['Data']['Status'] == "1":
            print('reverve success!')
            print(json.dumps(result))
            break
        print('reverve failed!')
        print(json.dumps(result))
        time.sleep(0.3)
        break
