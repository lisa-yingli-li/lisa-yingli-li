from hamcrest import assert_that
from ptest.decorator import TestClass, Test, BeforeClass

from Martech_API_Automation.api_business.Growth.MobileProxyService import MobileProxyService
from Martech_API_Automation.api_business.Growth.MobileService import MobileService
from Martech_API_Automation.settings import env_key
from Martech_API_Automation.test_data.AccountData import Account


@TestClass()
class MobileProxyServiceTest:
    @BeforeClass()
    def before_method(self):
        self.account_uuid = Account.get_test_account("us", env_key)["uuid"]
        self.mobile_proxy_service = MobileProxyService()
        self.mobile_service = MobileService()

    @Test(tags="sandbox")
    def test_get_inbox_preference(self):
        username = Account.get_test_account("uk", env_key)["username"]
        password = Account.get_test_account("uk", env_key)["password"]
        token = self.mobile_service.get_token(username, password, "uk")
        response = self.mobile_proxy_service.get_inbox_preference(self.account_uuid, token)
        print(response)

    @Test(tags="sandbox")
    def test_put_inbox_preference(self):
        username = Account.get_test_account("uk", env_key)["username"]
        password = Account.get_test_account("uk", env_key)["password"]
        token = self.mobile_service.get_token(username, password)
        response = self.mobile_proxy_service.put_inbox_preference(self.account_uuid, token)
        print(response)

    @Test(tags="sandbox")
    def test_get_refer_code(self):
        account_info = Account.get_test_account("us", env_key)
        username = account_info["username"]
        password = account_info["password"]
        token = self.mobile_service.get_token(username, password)
        referral_code = self.mobile_proxy_service.get_referral_code(token, account_info["uuid"])
        assert_that(account_info["referral_code"], referral_code)

