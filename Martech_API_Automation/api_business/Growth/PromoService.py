import json
import requests
from hamcrest import assert_that, equal_to

from Martech_API_Automation.api_business.BaseService import BaseService
from Martech_API_Automation.settings import env_key
from Martech_API_Automation.test_data.AccountData import AccountLocale
from Martech_API_Automation.test_data.CRMData import Promo_CF_Access_Client_Id, Promo_CF_Access_Client_Secret
from Martech_API_Automation.test_data.PromoData import Merchant_Info


class PromoV2Service(BaseService):
    def __init__(self):
        super().__init__("")

    def get_referral_code_v2(self, locale, consumer_uuid):
        api_locale = AccountLocale.get_api_locale(locale)
        request_url = self.host.format(api_locale) + "/mobile/api/v2/promo/referral/code"
        payload = {}

        headers = {
            'content-type': 'application/json',
            'CF-Access-Client-Id': "{0}".format(Promo_CF_Access_Client_Id[api_locale]),
            'CF-Access-Client-Secret': "{0}".format(Promo_CF_Access_Client_Secret[api_locale]),
            'Consumer-UUID': consumer_uuid
        }

        response = requests.get(request_url, headers=headers, data=json.dumps(payload))
        assert_that(response.status_code, equal_to(200))
        print(response.text)
        return response

        # response = requests.get(request_url, headers=headers)
        # assert_that(response.status_code, equal_to(200))
        # return json.loads(response.text)['response']['referralCode']

    def redeem_referral_code_V2(self, access_token, referral_code):
        request_url = self.host.format("us") + "/mobile/api/v2/promo/referral/code"

        payload = {
            'promoCode': referral_code
        }

        headers = {
            'content-type': 'application/json',
            'CF-Access-Client-Id': "{0}".format(Promo_CF_Access_Client_Id["us"]),
            'CF-Access-Client-Secret': "{0}".format(Promo_CF_Access_Client_Secret["us"]),
            'Consumer-UUID': access_token
        }

        response = requests.post(request_url, headers=headers, data=json.dumps(payload))
        assert_that(response.status_code, equal_to(400))
        return response

    def get_campaign_list(self, locale, merchant_id=902903903):
        api_locale = AccountLocale.get_api_locale(locale)
        request_url = self.host.format(api_locale) + "/v2/promo/self-promo/merchant/{0}/campaigns".format(merchant_id)

        response = requests.request("GET", request_url, headers={}, data="")
        assert_that(response.status_code, equal_to(200))
        return response

    def create_campaign(self, locale, start_time, end_time):
        api_locale = AccountLocale.get_api_locale(locale)
        url = self.host.format(api_locale) + "/v2/promo/self-promo/campaign"

        merchant_id = Merchant_Info[env_key][locale]["merchant_id"]
        merchant_name = Merchant_Info[env_key][locale]["merchant_name"]

        payload = json.dumps(
            {
                "merchantId": "{0}".format(merchant_id),
                "merchantName": "{0}".format(merchant_name),
                "campaignName": "Automation Campaign",
                "startTime": "2022-04-01T00:00:00.134Z",
                "endTime": "2022-04-06T09:44:26.134Z",
                "discountType": "AMOUNT",
                "discountValue": 10,
                "condition": {
                    "minimumOrderAmount": 30,
                    "channel": ["ONLINE"],
                    "country": "US",
                    "targetAudience": ["AFTERPAY_NEW_USER"]
                },
                "budget": {
                    "campaignTotalDiscount": 5000,
                    "customerBudget": {
                        "redemptionTimes": 1,
                        "window": "LIFETIME"
                    }
                },
                "billingDepartment": "MARKETING_GROWTH_AND_LIFECYCLE"

            })
        # payload = json.dumps({
        #     "merchantId": "902903903",
        #     "merchantName": "Nike",
        #     "campaignName": "Sini'test campaign",
        #     "startTime": "2022-03-02T22:44:26.134Z",
        #     "endTime": "2022-07-03T22:44:26.134Z",
        #     "discountType": "AMOUNT",
        #     "discountValue": 10,
        #     "condition": {
        #         "minimumOrderAmount": 100,
        #         "channel": [
        #             "ONLINE"
        #         ],
        #         "country": "GB",
        #         "targetAudience": [
        #             "AFTERPAY_NEW_USER"
        #         ]
        #     },
        #     "budget": {
        #         "campaignTotalDiscount": 20000,
        #         "customerBudget": {
        #             "redemptionTimes": 1,
        #             "window": "LIFETIME"
        #         }
        #     }
        # })
        headers = {
            'Content-Type': 'application/json',
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        print(response.text)
