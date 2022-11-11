import json
import datetime

import requests
from hamcrest import assert_that, equal_to

from Martech_API_Automation.test_data.AccountData import AccountLocale
from Martech_API_Automation.test_data.CRMData import Inbox_CF_Access_Client_Id, Inbox_CF_Access_Client_Secret, Inbox_Message_Template, CTA_Type

from Martech_API_Automation.api_business.BaseService import BaseService


class InboxService(BaseService):
    def __init__(self, locale):
        super().__init__("")
        api_locale = AccountLocale.get_api_locale(locale)
        self.headers = {
            'serviceTeam': 'post-man',
            'Authorization': 'Basic YWZ0ZXJwYXk6YWZ0ZXJwYXk=',
            'Content-Type': 'application/json',
            'CF-Access-Client-Id': "{0}".format(Inbox_CF_Access_Client_Id[api_locale]),
            'CF-Access-Client-Secret': "{0}".format(Inbox_CF_Access_Client_Secret[api_locale])
        }

    def add_message(self, uuid, message_type, expired_time=None, has_cta=True, has_cta1=True,
                    template=Inbox_Message_Template.COUPON_TEMPLATE, cta_type=CTA_Type.PROMOTION):
        if expired_time is None:
            expired_time = datetime.datetime.utcnow() + datetime.timedelta(days=3)
            expired_time = expired_time.strftime('%Y-%m-%dT%H:%M:%SZ')

        url = self.host + "/v1/inbox/messages"

        # message format
        message_info = {
            "template": "{0}".format(template),
            "expiredTime": "{0}".format(expired_time),
            "type": "{0}".format(message_type),
            "customerUuid": "{0}".format(uuid)
        }

        # set parameter with template
        if template == Inbox_Message_Template.COUPON_TEMPLATE:
            parameters = {
                    "merchant": "{0}".format(message_type),
                    "discount": "10",
                    "channel": "ONLINE",
                    "minimumOrderTotal": "50",
                    "month": "May",
                    "year": "2025",
                    "date": "5",
                    "time": "12:00:00",
                    "timezone": "UTC"
                }
        elif template == Inbox_Message_Template.F2F_TEMPLATE:
            parameters = {
                    "discount_title": "test",
                    "discount": "10"
                }
        else:
            raise Exception("not supported templated")

        message_info["parameters"] = parameters

        if has_cta:
            message_info["cta"] = {
                "type": "{0}".format(cta_type)
            }

        if has_cta1:
            message_info["cta1"] = {
                "type": CTA_Type.PROMOTION
            }
        payload = json.dumps({
            "messages": [message_info]
        })

        response = requests.post(url, headers=self.headers, data=payload)
        assert_that(response.status_code, equal_to(201))
        print("new message is added: {0}".format(response.text))
        return response.text

    def get_message_list(self, uuid):
        url = self.host + "/mobile/api/v1/inbox/messages?limit=20&locale=en-US&country=US"

        headers = self.headers
        headers["Consumer-UUID"] = uuid

        response = requests.get(url=url, headers=headers)
        assert_that(response.status_code, equal_to(200))
        return response

    def delete_message(self, message_list, uuid):
        url = self.host + "/mobile/api/v1/inbox/messages"
        headers = self.headers
        headers["Consumer-UUID"] = uuid

        payload = json.dumps({
            "ids": message_list
        })
        response = requests.delete(url=url, headers=headers, data=payload)

        assert_that(response.status_code, equal_to(204))
        return response

    def get_unread_count(self, uuid):
        url = self.host + "/mobile/api/v1/inbox/messages/unreadCount"

        headers = self.headers
        headers["Consumer-UUID"] = uuid

        response = requests.get(url=url, headers=headers)
        assert_that(response.status_code, equal_to(200))
        print("unread count is {0}".format(response.text))
        return response.text

    def read_all(self, uuid):
        url = self.host + "/mobile/api/v1/inbox/messages/readAll"

        headers = self.headers
        headers["Consumer-UUID"] = uuid

        response = requests.put(url=url, headers=headers, data={})
        assert_that(response.status_code, equal_to(200))
        return response.text

