import requests
import os
from twilio.rest import Client
from twilio.http.http_client import TwilioHttpClient
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ['API_KEY']
end_point = "https://api.openweathermap.org/data/2.5/forecast?"

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']


parameters = {
    "lat" : 39.585676,
    "lon" : 2.679648,
    "appid" : api_key,
    "units" : "metric"
}

response = requests.get(end_point, params= parameters)
response.raise_for_status()
weather_data = response.json()
weather_slice = weather_data['list'][:5]

will_rain = False

for each_item in weather_slice:
    condition_code = each_item['weather'][0]['id']
    if int(condition_code) < 700:
        will_rain = True

if will_rain:
    proxy_client = TwilioHttpClient()
    proxy_client.session.proxies = {'https': os.environ['https_proxy']}
    client = Client(account_sid, auth_token, http_client=proxy_client)
    message = client.messages.create(
                              body='It is going to rain today. Remember to bring an umbrella!',
                              from_='whatsapp:+14155238886',
                              to='whatsapp:+34610608797'
                          )

    print(message.status)