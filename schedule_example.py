import schedule

from main import main

schedule.every().day.at("10:00").do(main)
# Uncomment for debugging:
# schedule.every(1).minutes.do(main)

while True:
    schedule.run_pending()
