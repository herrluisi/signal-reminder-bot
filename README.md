# Signal Reminder - A CLI Interface which sends you reminders over Signal
### Setup of the signal rest api
This project uses the signal rest api from [this repo](https://github.com/bbernhard/signal-cli-rest-api).
Furthermore

### Start the bot
- docker compose up -d
- pip install -r requirements.txt
- python3 main.py


### Features

- Send a message to the specific channel you defined in the main.py
  - Example 1: "remindme 5 do not forget to drink water"
    - Now you get a reminder in 5 minutes to you default number that you have to drink water
  - Example 2: "remindme 5 do not forget to drink water +49123456789"
    - Now +49123456789 get a reminder in 5 minutes which reminds the person to drink water


### Ideas

- Schema to setup repeating reminders
