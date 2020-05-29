import logging
import os

import requests
from twilio.rest import Client

OPENWEATHER_API_KEY = os.environ.get("OPENWEATHER_API_KEY")
TWILIO_ACCOUNT_SID = os.environ.get("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_AUTH_TOKEN")
TWILIO_SENDER_NUMBER = os.environ.get("TWILIO_SENDER_NUMBER")
TWILIO_RECEIVER_NUMBER = os.environ.get("TWILIO_RECEIVER_NUMBER")


# Hardcode the zipcode and country code
# If this were a real application, you would be pulling
# this information from a database, instead of hardcoding here.
ZIPCODE = "94112"
# This isn't necessary -- it defaults to US if no country code is supplied
COUNTRY_CODE = "us"


def validate_api_credentials():
    # Validate that all the credentials are set
    apis = {
        "OpenWeather api": OPENWEATHER_API_KEY,
        "Twilio Account SID": TWILIO_ACCOUNT_SID,
        "Twilio Auth Token": TWILIO_AUTH_TOKEN,
        "Twilio sender number": TWILIO_SENDER_NUMBER,
        "Twilio receiver number": TWILIO_RECEIVER_NUMBER,
    }
    missing = []
    for api, cred in apis.items():
        if not cred:
            missing.append(api)
    if missing:
        raise Exception(f"Missing the following credentials: {', '.join(missing)}")


def get_weather():
    # get the weather from the OpenWeather API
    # documentation: https://openweathermap.org/current
    parameters = {
        "zip": f"{ZIPCODE},{COUNTRY_CODE}",
        "appid": OPENWEATHER_API_KEY,
        "units": "imperial",
    }
    logging.info("Requesting weather data from OpenWeather API.")
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather", params=parameters
    )
    return response.json()


def main():
    # Validate that credentials are set
    validate_api_credentials()

    # Create the twilio client
    client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

    weather = get_weather()
    description = weather["weather"][0]["description"]
    temperature = weather["main"]["temp"]

    # Send a text message with this data
    # Twilio example: https://www.twilio.com/docs/sms/tutorials/how-to-send-sms-messages-python
    logging.info("Sending SMS with Twilio.")
    message = client.messages.create(
        body=f"Good morning! Today the weather is {temperature} degrees F with {description}",
        from_=f"+{TWILIO_SENDER_NUMBER}",
        to=f"+{TWILIO_RECEIVER_NUMBER}",
    )


if __name__ == "__main__":
    main()
