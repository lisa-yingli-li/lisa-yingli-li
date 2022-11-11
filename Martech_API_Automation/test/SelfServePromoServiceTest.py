import json

from hamcrest import assert_that, equal_to
from ptest.decorator import TestClass, Test, BeforeClass

from Martech_API_Automation.api_business.Growth.MobileService import MobileService
from Martech_API_Automation.api_business.Growth.PromoService import PromoV2Service
from Martech_API_Automation.settings import env_key
from Martech_API_Automation.test_data.PromoData import Merchant_Info


@TestClass()
class PromoV2ServiceTest:
    @BeforeClass()
    def before_method(self):
        self.promo_service = PromoV2Service()
        self.mobile_service = MobileService()

    @Test(tags="sandbox", data_provider={"us", "uk", "au"})
    def test_get_promotion_list(self, locale):
        print("start testing in region: {0}".format(locale))
        merchant_id = Merchant_Info[env_key][locale]["merchant_id"]
        response = self.promo_service.get_campaign_list(locale, merchant_id)
        campaign_list = json.loads(response.text)["response"]
        print(campaign_list)

    @Test(tags="sandbox", data_provider={"us", "uk", "au"})
    def test_get_empty_promotion_list(self, locale):
        merchant_id = "11111111"
        response = self.promo_service.get_campaign_list(locale, merchant_id)
        campaign_list = json.loads(response.text)["response"]
        print(campaign_list)
        assert_that(campaign_list, equal_to([]))

    # @Test(tags="sandbox", data_provider={"us"})
    # def test_create_new_promotion(self, locale):
    #     merchant_id = MerchantId["us"]
    #     response = self.promo_service.create_campaign(locale, merchant_id)
    #     # campaign_list = json.loads(response.text)["response"]

