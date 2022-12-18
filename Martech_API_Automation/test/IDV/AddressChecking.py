from time import sleep

import requests
import uuid


def registration(i):
    registration_body = { "email": "test{i}@test.com".format(i=i),
                          "mobile": "469600{i}".format(i=i),
                          "password": "ABCDE123!@#",
                          "deviceId" : str(uuid.uuid4()),
                          "countryCode": "US"
                          }
    registration = requests.post("http://localhost:8194/v1/registrations", json=registration_body)
    print(registration.status_code)
    return registration.json()["id"]


def get_access(registration_id):

    mobile_verify = requests.post("http://localhost:8194/v1/registrations/{r}/verify".format(r=registration_id),
                                  json={"code": "111111"})
    print(mobile_verify.status_code)
    return mobile_verify.json()["accessToken"]

def create_profile(access_token):
    profile_body = {
        "name": {
            "givenNames": "SCOTT",
            "otherGivenNames": "",
            "surname": "GALLAGHER"
        },
        "dob": "2004-03-20",
        "address": {
            "line1": "1500 East Main street",
            "suburb": "Newark",
            "state": "OH",
            "postcode": "43055"
        },
        "shouldDoDuplicateIdentityCheck": True,
        "creditPolicyAgree": True,
        "preferredLocale": "en-US"
    }
    headers = {"Authorization": "Bearer {b}".format(b=access_token)}
    create_profile = requests.post("http://localhost:8194/v1/consumers/profile", json=profile_body, headers=headers)
    if create_profile.status_code != 201:
        print(create_profile.json()["errorCode"])
        print(create_profile.json()["message"])


def get_consumer(access_token):
    headers = {"Authorization": "Bearer {b}".format(b=access_token)}
    consumer_response = requests.get("http://localhost:8194/v1/consumers", headers=headers)
    print(consumer_response.json()["profileConfirmed"])


i = 1003
id = registration(i)
sleep(1)
access_token = get_access(id)
print(access_token)
sleep(1)
create_profile(access_token)
