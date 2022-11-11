class AccountLocale:
    US = "us"
    CA = "ca"
    UK = "uk"
    AU = "au"
    NZ = "uz"

    @staticmethod
    def get_api_locale(account_locale):
        if account_locale == AccountLocale.US or account_locale == AccountLocale.CA:
            api_locale = "us"
        elif account_locale == AccountLocale.NZ or account_locale == AccountLocale.AU:
            api_locale = "au"
        elif account_locale == AccountLocale.UK:
            api_locale = "eu"
        else:
            raise Exception("Invalid account locale is supplied: {0}".format(account_locale))

        return api_locale


class Account:
    Accounts = {
        'sandbox': {
            AccountLocale.US: [{"username": "testus_order1@rr.com", 'password': 'aptest@123',
                                "uuid": "a32356d3-fcf5-4945-a386-074091c60c13", "referral_code": "OAKEN-PH462"}],
            AccountLocale.CA: [{'username': 'tb3.cn.01', 'password': '12345'}],
            AccountLocale.UK: [{'username': 'testuk@sini.com', 'password': 'aptest@123',
                                "uuid": "b8114dd0-05a8-42d7-af68-6282e63c5c4d", "referral_code": "AAAAA-6Y8QN"}],
            AccountLocale.AU: [{'username': 'testau_refer1@rr.com', 'password': 'aptest@123',
                                "uuid": "7f7dfc48-43b3-47cc-a5a3-88cc6edd754b", "referral_code": "AAAAA-6Y8QN"}],
            AccountLocale.NZ: [{'username': 'hf3.cn.02', 'password': '12345'}]
        },
        'product': {}
    }

    @staticmethod
    def get_test_account(locale=AccountLocale.US, env='sandbox'):
        try:
            return Account.Accounts[env][locale][0]
        except:
            raise ValueError("Failed to get test account")
