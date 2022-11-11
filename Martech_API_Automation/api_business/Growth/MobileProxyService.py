import json

import requests
from hamcrest import assert_that, equal_to

from Martech_API_Automation.api_business.BaseService import BaseService


class MobileProxyService(BaseService):
    def __init__(self):
        super().__init__("")
        self.headers = {
            'Host': 'mobile-api-proxy-staging.afterpay.com',
            'ap-bundle-identifier': 'com.afterpay.afterpay-consumer-sandbox-us',
            # 'authorization': 'Bearer {0}'.format(access_token),
            'content-type': 'application/json'
        }

    def get_inbox_preference(self, uuid, token):
        url = self.host + "/us/v1/inbox/preference"
        self.headers["uuid"] = "{0}".format(uuid)
        self.headers["authorization"] = 'Bearer {0}'.format(token)

        response = requests.request("GET", url, headers=self.headers)
        print(response.text)
        return response

    def put_inbox_preference(self, uuid, token):
        url = self.host + "/us/v1/inbox/preference"
        payload = json.dumps({
            "optIn": False
        })
        self.headers["uuid"] = "{0}".format(uuid)
        self.headers["authorization"] = 'Bearer {0}'.format(token)

        response = requests.request("PUT", url, headers=self.headers, data=payload)
        assert_that(response.status_code, equal_to(204))
        return response

    def get_referral_code(self, access_token, uuid):
        request_url = self.host + "/us/v2/promo/referral/code"
        self.headers["authorization"] = 'Bearer {0}'.format(access_token)
        self.headers["consumer-uuid"] = "{0}".format(uuid)

        response = requests.request("GET", request_url, headers=self.headers)
        assert_that(response.status_code, equal_to(200))
        return json.loads(response.text)['response']['referralCode']

    # not tested
    def redeem_referral_code(self, access_token, referral_code):
        request_url = self.host + "/us/v2/promo/referral/code"

        payload = {
            'referralCode': referral_code
        }

        headers = {
            'authorization': 'Bearer {0}'.format(access_token),
            'content-type': 'application/json'
        }

        response = requests.post(request_url, headers=headers, data=json.dumps(payload))
        assert_that(response.status_code, equal_to(200))
