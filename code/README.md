# ESP8266 Smart Irrigation System

## Project Description
This project is a smart irrigation system that utilizes the ESP8266 microcontroller to monitor environmental conditions and control watering through a Telegram bot interface. The system reads temperature and moisture levels using a DHT11 sensor and logs this data, which can be accessed and controlled remotely.

## Features
- Real-time temperature and moisture monitoring.
- Data logging with timestamped entries.
- Remote watering control via Telegram bot commands.
- Easy retrieval of logged data through Telegram bot.

## Hardware Requirements
- ESP8266 WiFi Module
- DHT11 Temperature and Humidity Sensor
- Soil Moisture Sensor
- Relay Module (for controlling water pump or solenoid valve)

## Software Dependencies
- Arduino IDE for ESP8266 code deployment.
- Python 3.x for running the Telegram bot.
- `python-telegram-bot` library.

## Installation & Setup
### ESP8266
1. Connect the DHT11 sensor and soil moisture sensor to the ESP8266.
2. Update the `ssid` and `password` in the code to match your WiFi credentials.
3. Flash the `ESP8266_code.ino` to the ESP8266 module using the Arduino IDE.

### Telegram Bot
1. Create a new bot on Telegram using BotFather and obtain the bot token.
2. Replace `MYTOKEN` in `bot.py` with your obtained bot token.
3. Run `bot.py` on your server or local machine to start the bot.

## Usage Instructions
- Send `/start` to the Telegram bot to initiate interaction.
- Use `/water_on` to turn on the watering system.
- Use `/water_off` to turn off the watering system.
- Send `/log` followed by a timestamp to retrieve logged data for a specific time.

## Code Explanation
### ESP8266 Code
- Manages HTTP GET requests to provide the latest sensor readings.
- Manages HTTP POST requests to receive and act on commands from the Telegram bot.

### Get Code
- A Python script that periodically fetches data from the ESP8266 and logs it into files.

### Bot Code
- A Python script that uses the `python-telegram-bot` library to facilitate user interaction with the system.

## Contributing
Contributions to this project are welcome! Please feel free to fork the repository, submit pull requests, or report any issues you encounter.

