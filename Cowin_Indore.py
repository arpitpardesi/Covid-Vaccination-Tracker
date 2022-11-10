import re
import time
from datetime import datetime, timedelta

import requests


def center_data(hit, centers, file):
    centersData = centers["centers"]
    withvaccine = 0
    oneCenter: object
    #    (str(oneCenter["block_name"]).lower() == "indore") and
    for oneCenter in centersData:
        if (
                oneCenter["sessions"][0]["min_age_limit"] == 18) and (
                oneCenter["sessions"][0]["available_capacity_dose1"] > 1):
            withvaccine += 1
            resp = "Center: {0}, {3}, {4}\nVaccine: {1}\nDose 1 Slot: {2} | Date: {5} \n".format(oneCenter["name"],
                                                                                                  oneCenter["sessions"][
                                                                                                     0]["vaccine"],
                                                                                                 oneCenter["sessions"][
                                                                                                     0][
                                                                                                     "available_capacity_dose1"],
                                                                                                 oneCenter["address"],
                                                                                                 oneCenter[
                                                                                                     "block_name"],
                                                                                                 oneCenter["sessions"][
                                                                                                     0][
                                                                                                     "date"])

            # print(hit)
            print(resp)
            response_tracker(hit=hit, resp=resp, file=file)
    if withvaccine == 0:
        # print(hit)
        print("{0} vaccination centers found at your location but with {1} slots!!😂😂\n".format(len(centersData),
                                                                                                 withvaccine))

    # res = oneCenter["sessions"][0]["available_capacity_dose1"]


def count_tracker(count):
    with open("count.txt", 'r+') as ct:
        text = ct.read()
        text = re.sub(str(count - 1), str(count), text)
        ct.seek(0)
        ct.write(text)
        ct.truncate()


def response_tracker(hit, resp, file):
    C = open(file, "a")
    C.write(hit + "\n" + resp + "\n\n")
    C.close()


# pin = "452001"
x = datetime.now()
todayDate = x.strftime("%d") + "-" + x.strftime("%m") + "-" + x.strftime("%Y")
t = x + timedelta(1)
tomDate = t.strftime("%d") + "-" + t.strftime("%m") + "-" + t.strftime("%Y")
date = [todayDate, tomDate]

# API search through Pincode & Date
# url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?" + 'pincode=' + str(pin) + '&date=' + str(todayDate)
# Response Output
# file = pin + " - " + x.strftime("%b") + " " + x.strftime("%d") + ", " + x.strftime("%Y") + ".txt"


# API search through DistrictCode & Date
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=314&date={0}".format(
    date[0])
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
# Response Output
file = "Indore" + " - " + x.strftime("%b") + " " + x.strftime("%d") + ", " + x.strftime("%Y") + ".txt"

# Previous count
pc = open("count.txt", 'r')
count = int(pc.read())

while requests.status_codes != 200:
    count += 1
    count_tracker(count)

    # Get
    response = requests.get(url, headers=header)

    # print(response.status_code)
    if response.status_code == 200:
        hit = "Request hit #{0} ".format(count) + str(datetime.now())
        res = response.json()
        # print(hit + "\n" + str(res) + "\n")
        print(hit)
        center_data(hit=hit, centers=res, file=file)
        time.sleep(0.4)

    else:
        print("Due to high traffic from your IP. Refreshing API 5 min")
        time.sleep(300)
        """
        # Todo - For 5 min refreshing counter
        for i in range(300, 0):
            print("Refreshing API for you IP in {0}".format(i) + " secs")
            print("\r",end="")
            time.sleep(1)
        """
    time.sleep(2.48)