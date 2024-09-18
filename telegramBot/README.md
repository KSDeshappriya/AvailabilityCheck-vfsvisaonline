# Appointment Checking Bot (vfsvisaonline)

## Project Overview

This project is a Telegram bot designed to monitor visa appointment availability on the Dutch embassy/consulate website. It scrapes the website for updates, bypassing Cloudflare protection and periodically notifies the user about available appointment slots. The bot is built using Python, Pyrogram, BeautifulSoup, DrissionPage, and a custom Cloudflare bypasser.

## Features

- **Telegram Bot**: Sends periodic updates to users regarding appointment availability.
- **Cloudflare Bypass**: Uses a custom Chromium-based driver to bypass Cloudflare protection.
- **Periodic Checking**: Automatically checks the appointment page every 60 seconds.
- **Error Handling**: Notifies the user in case of errors or unavailability of appointments.
- **Command Support**:
  - `/start` to begin checking for appointments.
  - `/stop` to halt the appointment checks.

## Requirements

### Python Packages

- `pyrogram`
- `beautifulsoup4`
- `urllib`
- `requests`
- `DrissionPage`
- `pyvirtualdisplay`
- `asyncio`

Install the required packages using the command:

```bash
pip install -r requirements.txt
```

### System Dependencies

Ensure the following system dependencies are installed:

- `Google Chrome`
- `Chromedriver`
- `xvfb`
- Other libraries listed in the Dockerfile (e.g., `libx11-xcb1`, `libnss3`, etc.)

## Credentials Setup

A separate file named `Cred.py` is required for storing API credentials:

```python
class Cred:
    API_ID = "your_api_id"
    API_HASH = "your_api_hash"
    BOT_TOKEN = "your_bot_token"
```

Make sure to replace the values with the appropriate credentials from your [my.telegram.org](https://my.telegram.org).

## Cloudflare Bypasser

A custom module `CloudflareBypasser.py` is used to bypass Cloudflare's protection on the target website. This module utilizes the DrissionPage library to load the website in a headless Chrome browser and extract the necessary headers for making subsequent requests.

## How it Works

1. **Bot Initialization**: The bot is initialized with `api_id`, `api_hash`, and `bot_token`. When the user sends the `/start` command, the bot begins checking the specified URL for appointment availability.
2. **Bypassing Cloudflare**: The bot uses a Chromium browser to load the webpage, bypass Cloudflare, and extract necessary headers for further requests.
3. **Form Submissions**: After bypassing Cloudflare, the bot performs a series of GET and POST requests to navigate through the appointment booking process, scraping hidden fields, and submitting form data.
4. **Notifications**: If appointments are available, the bot notifies the user. It also handles error cases like Cloudflare reauthentication or page access issues.
5. **Periodic Checking**: The bot checks for updates every 60 seconds.

## Bot Commands

- **/start**: Starts the bot and begins checking for available appointments every 60 seconds.
- **/stop**: Stops the appointment checking process.

## Docker Setup

To run the bot inside a Docker container:

1. **Build the Docker Image**:

   ```bash
   docker build -t appointment-checker-bot .
   ```
2. **Run the Docker Container**:

   ```bash
   docker run -d appointment-checker-bot
   ```

### Dockerfile Breakdown

- **Base Image**: The base image is `python:3.12.6-slim`.
- **Chrome and ChromeDriver**: Google Chrome and ChromeDriver are installed to enable Chromium-based browsing for bypassing Cloudflare.
- **Python Dependencies**: All necessary Python libraries are installed.
- **Bot Script**: The bot script (`Bot200E.py`) is copied into the container and executed.

## Usage

After starting the bot, it will periodically check the Dutch embassy/consulate website for available appointments. Users will be notified directly through Telegram.

### Start Bot

To start the bot, use the `/start` command. The bot will then begin sending periodic updates about appointment availability every 60 seconds.

### Stop Bot

To stop the bot from checking appointments, use the `/stop` command.

## License

This project is licensed under the **CC BY-NC 4.0 License**. See the [LICENSE](https://creativecommons.org/licenses/by-nc/4.0/) file for more details.

## Author Information

- **Telegram**: [@AstroMonsterG](https://t.me/AstroMonsterG)
- **GitHub**: [KSDeshappriya](https://github.com/KSDeshappriya)
- **Email**: [ksdeshappriya.official@gmail.com](ksdeshappriya.official@gmail.com)
