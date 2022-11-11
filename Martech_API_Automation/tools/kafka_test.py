from kafka import KafkaConsumer
import requests

TOPIC = "us-qa.event.marketing.event-tracking.v1"


def get_event_by_topic_and_offset(env, topic, offset):
    domain = "https://event-dashboard.v1.uswe2.beta.platform.afterpay.cloud"
    # "https://event-dashboard.v1.uswe2.beta.platform.afterpay.cloud/api/v1/events/envs/us-qa/topics/us-qa.event.marketing.event-tracking.v1?offset=32783601&partition=0"
    url = domain + "/api/v1/events/envs/{0}/topics/{1}?offset={2}&partition=0".format(env, topic, offset)

    headers = {
        "accept": "application/json",
        "authority": "event-dashboard.v1.uswe2.beta.platform.afterpay.cloud",
        "cookie": "CF_Auth"
                  "orization=eyJhbGciOiJSUzI1NiIsImtpZCI6IjkxNDlkZmQ2NWI4MjI2YjZhMzczOTJmMWJkYjU2YzYwNDQwZGFiZjBmYmI3ZWQxZGExMzNiMjU0NjgwMjhmNzYifQ.eyJhdWQiOlsiZDBlNjQxZTEzZDhjOWI5OGNmMzUyZDllNDZkMWU3NzdkNzU5NWM1Y2ZmMzk3MWUzZGJmYzgzMDhmNDE5NjU0MCJdLCJlbWFpbCI6InNpbmkuc2hhb0BhZnRlcnBheS5jb20iLCJleHAiOjE2NTM4NDkzODcsImlhdCI6MTY1MzgwNjE4NywibmJmIjoxNjUzODA2MTg3LCJpc3MiOiJodHRwczovL2FmdGVycGF5LmNsb3VkZmxhcmVhY2Nlc3MuY29tIiwidHlwZSI6ImFwcCIsImlkZW50aXR5X25vbmNlIjoicXBkbjZpNnc4bzVWVHJURSIsInN1YiI6IjZkMGFlZmNlLTBlMTItNDUxYi1hNWRjLTczZTkyZTQ0ODA5YiIsImNvdW50cnkiOiJVUyJ9.b6NKsp5oPPeGTlkeZU0K7DU_nLQxJ8npqdavw6XjQ0scpFgbT69Ld86t6SWBuM5ZtoKFEarevW-6tHCEq6mfLdfUSwgupc6OJ90aw7k3v7AM8vmdPculEtnNcaPZz8C-umxQTACbAY15h90m34c5lPpHoS1QiECrwJ03CIxnhOdUmu8MRWBxauhqiFwGwDMD0MyELJ_K3nSsLKPFxLowAUETawaiWdz_pPbzmWJjtVJ5svDgpAcEwZyPRruv5gS-M8CPm4h246lywksQYKjwv1uRxx8pHedJRHBUeDHAvquK4ysuLToFoYIM4eNZPUIfo3DSWabuJeU_Fh1P0vW8Kw"
    }

    response = requests.request("GET", url, headers=headers)
    print(response)


def get_event_topic():
    url = "https://event-dashboard.v1.usea1.beta.platform.afterpay.cloud/api/v1/events/envs/us-qa/topics/us-qa.event.marketing.event-tracking.v1?decryptpii=false&offset=-1"
    headers = {
        "accept": "application/json"}

    response = requests.request("GET", url)
    print(response.text)


get_event_topic()
