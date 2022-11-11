import json

from hamcrest import assert_that, equal_to, greater_than_or_equal_to, greater_than
from ptest.decorator import TestClass, Test, BeforeClass
from Martech_API_Automation.api_business.Incentive.BillingService import BillingService


@TestClass()
class BillingServiceTest:
    @BeforeClass()
    def before_method(self):
        self.billing_service = BillingService()
        self.advertiser_id = 66406

    @Test(tags="sandbox")
    def test_get_card(self):
        card_info = self.billing_service.get_card(self.advertiser_id)

        assert_that(card_info["last4"], equal_to("1111"), "last4")
        assert_that(card_info["expMonth"], equal_to(3), "expMonth")
        assert_that(card_info["expYear"], equal_to(2030), "expYear")
        assert_that(card_info["cardBrand"], equal_to("VISA"), "Brand")

    @Test(tags="sandbox")
    def test_get_balance(self):
        balance_info = self.billing_service.get_balance(self.advertiser_id)
        print(balance_info)

        assert_that(balance_info["advertiserId"], equal_to("66406"))
        assert_that(balance_info["balance"], greater_than_or_equal_to(0))
        assert_that(balance_info["threshold"], equal_to(2000))

    @Test(tags="sandbox")
    def test_get_completed_payment_record(self):
        status = "COMPLETED"
        record_list = self.billing_service.get_payment_records(self.advertiser_id, status)
        print(record_list)
        assert_that(len(record_list), equal_to(4))
        assert_that(record_list["totalNum"], greater_than(0), "totalNum")
        assert_that(record_list["pageIndex"], equal_to(0), "pageIndex")
        assert_that(record_list["itemNumPerPage"], equal_to(10), "itemNumPerPage")
        assert_that(record_list["list"][0]["status"], equal_to(status), "Status")

    @Test(tags="sandbox")
    def test_get_created_payment_record(self):
        status = "CREATED"
        record_list = self.billing_service.get_payment_records(self.advertiser_id, status)
        print(record_list)
        assert_that(len(record_list), equal_to(4))
        assert_that(record_list["list"][0]["status"], equal_to(status), "Status")

    @Test(tags="sandbox")
    def test_get_failed_payment_record_desc(self):
        status = "FAILED"
        record_list = self.billing_service.get_payment_records(advertiser_id=self.advertiser_id, status=status,
                                                               sort_type="DESC")

        first_create_date = record_list["list"][0]["createTime"]
        second_create_date = record_list["list"][1]["createTime"]
        assert_that(len(record_list), equal_to(4))
        assert_that(record_list["list"][0]["status"], equal_to(status), "Status")
        print(first_create_date)
        print(second_create_date)
        assert_that(first_create_date, greater_than(second_create_date))

    @Test(tags="sandbox")
    def test_get_payment_method_failed(self):
        campaign_id = 80390621
        response = self.billing_service.get_payment_method(self.advertiser_id, campaign_id)
        assert_that(response.status_code, equal_to(404))

        payment_method = json.loads(response.text)
        print(payment_method)

        assert_that(payment_method["code"], equal_to("EXT_PAYMENT_METHOD_NOT_FOUND"), "code")
        assert_that(payment_method["error"], equal_to("payment method not found for campaign: {0}".format(campaign_id)),
                    "error")

    @Test(tags="sandbox")
    def test_get_payment_method_failed(self):
        campaign_id = 80390621
        response = self.billing_service.get_payment_method(self.advertiser_id, campaign_id)
        assert_that(response.status_code, equal_to(404))

        payment_method = json.loads(response.text)
        print(payment_method)

        assert_that(payment_method["code"], equal_to("EXT_PAYMENT_METHOD_NOT_FOUND"), "code")
        assert_that(payment_method["error"], equal_to("payment method not found for campaign: {0}".format(campaign_id)),
                    "error")
