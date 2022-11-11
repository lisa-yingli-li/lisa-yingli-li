import json

import requests
from hamcrest import assert_that, equal_to
from Martech_API_Automation.api_business.BaseService import BaseService


class BillingService(BaseService):
    def __init__(self):
        super().__init__("")
        self.headers = {
            'content-type': 'application/json',
            "accept": "*/*",
            'Authorization': 'Basic YWZ0ZXJwYXk6YWZ0ZXJwYXk='
        }

    def get_card(self, advertiser_id):
        request_url = self.host + "/v1/payment/advertisers/{0}/card".format(advertiser_id)

        response = requests.get(request_url, headers=self.headers, data=json.dumps({}))
        assert_that(response.status_code, equal_to(200))
        return json.loads(response.text)

    def get_balance(self, advertiser_id):
        request_url = self.host + "/v1/payment/advertisers/{0}/balance".format(advertiser_id)

        response = requests.get(request_url, headers=self.headers, data=json.dumps({}))
        assert_that(response.status_code, equal_to(200))
        return json.loads(response.text)

    def get_payment_records(self, advertiser_id, status, start_date="", end_date="", sort_type="ASC", page_index=0,
                            number_per_page=10):
        sub_url = "/v1/payment/advertisers/{0}/records?status={1}&sortType={2}&pageIndex={3}&itemNumPerPage={4}".format(
            advertiser_id, status, sort_type, page_index, number_per_page)

        if start_date != "" and end_date != "":
            sub_url = sub_url + "&startDate={5}&endDate={6}".format(start_date, end_date)

        request_url = self.host + sub_url

        response = requests.get(request_url, headers=self.headers, data=json.dumps({}))
        assert_that(response.status_code, equal_to(200))

        return json.loads(response.text)

    def get_payment_method(self, advertiser_id, campaign_id):
        request_url = self.host + "/v1/payment/advertisers/{0}/method/{1}".format(advertiser_id, campaign_id)

        response = requests.get(request_url, headers=self.headers, data=json.dumps({}))
        # assert_that(response.status_code, equal_to(200))
        return response

