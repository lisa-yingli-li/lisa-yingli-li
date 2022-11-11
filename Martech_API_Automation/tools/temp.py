from datetime import datetime, timezone, timedelta

import requests
import json

def redeem(number):

    url = "https://promotion.marketing.us.platform.afterpay-beta.com/v1/promo/codes/redeem"

    payload = json.dumps({
      "user": {
        "id": "100000sfs2dfj00{0}".format(number),
        "country": "US",
        "is_new_user": "true"
      },
      "order": {
        "token": "100000wsdljlsj1ss{0}".format(number),
        "country": "US",
        "merchant_id": "100142852",
        "total": {
          "currency": "USD",
          "amount": "100"
        },
        "channel": "ONLINE"
      }
    })
    headers = {
      'Authorization': 'Basic e3tBVVRIX1VTRVJ9fTp7e0FVVEhfUEFTU1dPUkR9fQ==',
      'Content-Type': 'application/json',
      'Cookie': '__cf_bm=P5Tm4BJh7O0SmjTS1N9mXF7EZzlWo0U_cDw_HK_njEI-1648792271-0-ARrtQHl3YC07nYd04ccE8aAfvIn7neatxpgAaxaWoNR54UHZ400Zxt38ZyNiNOfI83vsFzDCAC2sXv0XflD1oIo='
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)


# for i in range(151,152):
#     redeem(i)

AUTZ = timezone(timedelta(hours=+11))
BJTZ = timezone(timedelta(hours=+8))
USTZ = timezone(timedelta(hours=-8))


zoned_time4 = datetime(2022, 4, 21, 00, 00, 00, 000, tzinfo=AUTZ)

# fmt = '%Y-%m-%dT%H:%M:%S.%f%z'
# zoned_time1 = datetime.today().astimezone(tz)

# utc_now = datetime.now(timezone.utc)
dt = zoned_time4.astimezone(BJTZ)
utc = zoned_time4.astimezone(timezone.utc)
usdt = zoned_time4.astimezone(USTZ)
print(dt)
print(utc)
print(usdt)
