import json

import requests
from hamcrest import assert_that, equal_to

from Martech_API_Automation.api_business.BaseService import BaseService
from Martech_API_Automation.test_data.AccountData import AccountLocale


class MobileService(BaseService):
    def __init__(self):
        super().__init__("")

    def get_token(self, user_name, password, account_local="us"):
        api_locale = AccountLocale.get_api_locale(account_local)
        url = self.host.format(api_locale) + "/v2/login/basic"

        payload = json.dumps({
            "email": user_name,
            "password": password,
            "deviceId": "wef899823ui",
            "notification": "asfiuiuweiiwk",
            "shouldCheckEmailVerificationEligibility": True
        })

        headers = {
            'Content-Type': 'application/json',
        }
        response = requests.post(url, headers=headers, data=payload)
        assert_that(response.status_code, equal_to(200))
        return json.loads(response.text)['accessToken']
