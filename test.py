import datetime

import requests

pin = 452001
x = datetime.datetime.now()
todayDate = x.strftime("%d") + "-" + x.strftime("%m") + "-" + x.strftime("%Y")
par = {
    "pincode": pin,
    "date": todayDate
}
# url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?" + 'pincode=' + str(pin) + '&date=' + str(todayDate)
url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id=314&date=21-05-2021"
header = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}

response = requests.get(url, headers=header)
res = response.json()

centersData = res["centers"]
withvaccine = 0
for oneCenter in centersData:
    if (str(oneCenter["block_name"]).lower() == "indore") and (oneCenter["sessions"][0]["min_age_limit"] == 18) and (
            oneCenter["sessions"][0]["available_capacity_dose1"] > 0):
        withvaccine += 1
        print("Center: {0}\n Vaccine: {1}\n Dose 1: {2} ".format(oneCenter["name"],
                                                                 oneCenter["sessions"][0]["vaccine"],
                                                                 oneCenter["sessions"][0][
                                                                     "available_capacity_dose1"]))

print("{0} vaccination centers found at your location but {1} with vaccine!!😂😂".format(len(centersData), withvaccine))
