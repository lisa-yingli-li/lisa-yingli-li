import json

from hamcrest import assert_that
from ptest.decorator import TestClass, Test, BeforeClass

from Martech_API_Automation.api_business.Growth import MobileService
from Martech_API_Automation.api_business.Growth.PromoService import PromoV2Service
from Martech_API_Automation.settings import env_key
from Martech_API_Automation.test_data.AccountData import Account


@TestClass()
class PromoV2ServiceTest:
    @BeforeClass()
    def before_method(self):
        self.promo_service = PromoV2Service()
        self.mobile_service = MobileService()

    @Test(tags="sandbox", data_provider={"us", "uk", "au"})
    def test_get_referral_code_V2(self, locale):
        account_info = Account.get_test_account(locale, env_key)
        referral_code = self.promo_service.get_referral_code_v2(locale, account_info["uuid"])

        assert_that(account_info["referral_code"], referral_code)
        print(referral_code)

    @Test(tags="sandbox")
    def test_redeem_referral_code_V2(self):
        # code is redeemed already, verify error message
        consumer_uuid = "900526e9-7428-458e-93de-c5dbc4236892"
        response = self.promo_service.redeem_referral_code_V2(consumer_uuid, "F-843H2")
        redeem_error_code = json.loads(response.text)['error']['error_code']
        redeem_error_message = json.loads(response.text)['error']['error_message']

        assert_that(redeem_error_message, "code not accepted")
        assert_that(redeem_error_code, "CODE_NOT_ACCEPTED")


