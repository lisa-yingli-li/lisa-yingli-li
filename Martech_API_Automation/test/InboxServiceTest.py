import json
import time
import datetime

from hamcrest import *
from ptest.decorator import TestClass, Test, BeforeClass

from Martech_API_Automation.api_business.Growth.InboxService import InboxService
from Martech_API_Automation.settings import env_key
from Martech_API_Automation.test_data.AccountData import Account
from Martech_API_Automation.test_data.CRMData import MESSAGE_TYPE_LIST, CTA_Type, Inbox_Message_Template


@TestClass()
class InboxServiceTest:
    @BeforeClass()
    def before_method(self):
        self.inbox_service = InboxService("us")
        self.account_uuid = Account.get_test_account("us", env_key)["uuid"]

    @Test(tags="sandbox", data_provider=MESSAGE_TYPE_LIST)
    def test_add_message_with_two_cta(self, message_type):
        print("create messages for {0}".format(message_type))
        response = self.inbox_service.add_message(self.account_uuid, message_type)
        message_list = json.loads(response)['messageIds']
        print(message_list)
        assert_that(len(message_list), 1)

    @Test(tags="sandbox")
    def test_add_message_with_cta(self):
        response = self.inbox_service.add_message(self.account_uuid, "PROMOTION_MARKETING", has_cta1=False)
        message_list = json.loads(response)['messageIds']
        print(message_list)
        assert_that(len(message_list), equal_to(1))

    @Test(tags="sandbox")
    def test_add_message_with_cta1(self):
        response = self.inbox_service.add_message(self.account_uuid, "PROMOTION_MARKETING", has_cta=False)
        message_list = json.loads(response)['messageIds']
        print(message_list)
        assert_that(len(message_list), equal_to(1))

    @Test(tags="sandbox")
    def test_add_message_without_cta(self):
        response = self.inbox_service.add_message(self.account_uuid, "PROMOTION_MARKETING", has_cta=False,
                                                  has_cta1=False)
        message_list = json.loads(response)['messageIds']
        print(message_list)
        assert_that(len(message_list), equal_to(1))

    @Test(tags="sandbox")
    def test_add_f2f_message(self):
        response = self.inbox_service.add_message(self.account_uuid, "PROMOTION_MARKETING", has_cta1=False,
                                                  cta_type=CTA_Type.INVITE,
                                                  template=Inbox_Message_Template.F2F_TEMPLATE)
        message_list = json.loads(response)['messageIds']
        print(message_list)
        assert_that(len(message_list), equal_to(1))


    @Test(tags="sandbox")
    def test_get_message_list(self):
        response = self.inbox_service.get_message_list(self.account_uuid)
        message_list = json.loads(response.text)["messages"]
        print(message_list)
        assert_that(len(message_list), equal_to(20))


    @Test(tags="sandbox", data_provider=MESSAGE_TYPE_LIST)
    def test_delete_message(self, message_type):
        response = self.inbox_service.add_message(self.account_uuid, message_type)
        message_list = json.loads(response)['messageIds']

        response = self.inbox_service.delete_message(message_list, self.account_uuid)
        assert_that(response.ok)


    @Test(tags="sandbox")
    def test_get_unread_count(self):
        response = self.inbox_service.get_unread_count(self.account_uuid)
        unread_count = json.loads(response)['count']

        response = self.inbox_service.add_message(self.account_uuid, "SERVICING")
        message_list = json.loads(response)['messageIds']
        expect_unread_count = unread_count + 1

        response = self.inbox_service.get_unread_count(self.account_uuid)
        actual_unread_count = json.loads(response)['count']
        assert_that(actual_unread_count, equal_to(expect_unread_count))


    @Test(tags="sandbox")
    def test_read_all(self):
        self.inbox_service.add_message(self.account_uuid, "SERVICING")

        response = self.inbox_service.get_unread_count(self.account_uuid)
        actual_unread_count = json.loads(response)['count']
        assert_that(actual_unread_count > 0, True)

        self.inbox_service.read_all(self.account_uuid)
        response = self.inbox_service.get_unread_count(self.account_uuid)
        unread_count = json.loads(response)['count']
        assert_that(unread_count, equal_to(0))


    @Test(tags="sandbox")
    def test_not_load_expired_message(self):
        # insert a message whose expire time is 5 seconds later
        expired_time = datetime.datetime.utcnow() + datetime.timedelta(seconds=5)
        expired_time = expired_time.strftime('%Y-%m-%dT%H:%M:%SZ')
        response = self.inbox_service.add_message(self.account_uuid, "SERVICING", expired_time)
        message_id = json.loads(response)['messageIds'][0]

        # check message is inserted
        response = self.inbox_service.get_message_list(self.account_uuid)
        message_list = json.loads(response.text)["messages"]
        first_message = message_list[0]
        print("check the first message is new added {0}".format(first_message))
        assert_that(message_id, first_message)

        # check message is not loaded after 5 seconds
        time.sleep(5)
        response = self.inbox_service.get_message_list(self.account_uuid)
        message_list = json.loads(response.text)["messages"]
        first_message = message_list[0]
        print("check the first message is new added {0}".format(first_message))
        assert_that(message_id, not_(first_message))
