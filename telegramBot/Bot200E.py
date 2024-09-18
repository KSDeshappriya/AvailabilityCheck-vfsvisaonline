from pyrogram import Client, filters
from urllib import request, parse
from bs4 import BeautifulSoup
from DrissionPage import WebPage, ChromiumOptions, ChromiumPage
import time
import asyncio
from pyvirtualdisplay import Display

# Import external classes
from CloudflareBypasser import CloudflareBypasser
from Cred import Cred

# API ID and API hash from my.telegram.org
api_id = Cred.API_ID
api_hash = Cred.API_HASH
bot_token = Cred.BOT_TOKEN

# creator
creator_telegram = "@AstroMonsterG"
creator_github = "https://github.com/KSDeshappriya"
creator_email = "ksdeshappriya.official@gmail.com"

# Initialize the bot client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# URL of the website to scrape
url = 'https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppWelcome.aspx?P=b0KsiJlv+LIdjKDvIvW+nLNY7GnUFdfuwQj4DXbs4vo='

# This will hold the chat ID for periodic notifications
user_chat_id = None

# Save the headers globally after successfully retrieving them once
global_headers = None

def load_driver_and_bypass():
    """Function to load Chromium driver and bypass Cloudflare, returns the headers."""
    # Start virtual display
    display = Display(visible=0, size=(1920, 1080))
    display.start()

    try:
        # Create a configuration object
        co = ChromiumOptions()
        co.set_argument("--no-sandbox")  # Add no-sandbox for Docker environments
        co.set_paths(browser_path="/usr/local/bin/chromiumbrowser")

        # Initialize ChromiumPage with the options
        driver = ChromiumPage(addr_or_opts=co)
        driver.get(url)
        
        # Bypass Cloudflare
        cf_bypasser = CloudflareBypasser(driver)
        cf_bypasser.bypass()
        # Get headers and close the driver
        headers = cf_bypasser.get_headers()

        driver.quit()
        return headers
    finally:
        display.stop()

def urllib_get(url, headers):
    """Function to perform a GET request using urllib and return the response body and status code."""
    req = request.Request(url, headers=headers)
    with request.urlopen(req) as response:
        status_code = response.getcode()  # Get the status code
        body = response.read()  # Read the response body
    return status_code, body

def urllib_post(url, headers, data):
    """Function to perform a POST request using urllib and return the response body and status code."""
    data = parse.urlencode(data).encode('utf-8')
    req = request.Request(url, data=data, headers=headers)
    with request.urlopen(req) as response:
        status_code = response.getcode()  # Get the status code
        body = response.read()  # Read the response body
    return status_code, body


async def check_appointments_periodically():
    """Function to check appointments every 60 seconds."""
    global user_chat_id, global_headers

    while True:
        if user_chat_id:
            try:
                await app.send_message(user_chat_id, "Checking for available appointments...")

                # If global headers are None, load the driver and bypass Cloudflare
                if global_headers is None:
                    global_headers = load_driver_and_bypass()
                    print("++++++++++++++++++++++\n", global_headers, "+++++++++++++++++++++++++++++")

                # Step 1: Get the initial page to extract hidden form fields
                status_code, response = urllib_get(url, global_headers)
                print("+++++++\n", status_code, "\n++++++++++++")
                
                # If the response status is not 200, reload the driver and bypass Cloudflare again
                if status_code != 200:
                    await app.send_message(user_chat_id, "Error: Response status not 200, reloading driver...")
                    global_headers = load_driver_and_bypass()
                    status_code, response = urllib_get(url, global_headers)

                # Parse the initial page
                initial_soup = BeautifulSoup(response, 'html.parser')

                # Extract hidden form fields
                view_state = initial_soup.find('input', {'name': '__VIEWSTATE'})['value']
                view_state_generator = initial_soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
                event_validation = initial_soup.find('input', {'name': '__EVENTVALIDATION'})['value']

                # Define the payload for the first form submission
                payload_1 = {
                    '__EVENTTARGET': 'ctl00$plhMain$lnkSchApp',
                    '__EVENTARGUMENT': '',
                    '__VIEWSTATE': view_state,
                    '__VIEWSTATEGENERATOR': view_state_generator,
                    '__EVENTVALIDATION': event_validation,
                    '__VIEWSTATEENCRYPTED': ''
                }

                # Submit the first form
                status_code, response1 = urllib_post(url, global_headers, payload_1)

                # Step 2: Parse the new page after the first submission
                new_page_soup = BeautifulSoup(response1, 'html.parser')

                # Extract hidden form fields
                hidden_inputs = new_page_soup.find_all('input', type='hidden')
                form_data = {input.get('name'): input.get('value') for input in hidden_inputs}

                # Add additional form data for submission
                form_data.update({
                    'ctl00$plhMain$tbxNumOfApplicants': '1',
                    'ctl00$plhMain$cboVisaCategory': '966',   # Example for Passport
                    'ctl00$plhMain$btnSubmit': 'Continue'
                })

                # Submit the second form
                submit_url = 'https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppSchedulingGetInfo.aspx?P=wpmn7S46C72lQRV%2f1kDyNQ%3d%3d'
                status_code, response2 = urllib_post(submit_url, global_headers, form_data)

                if status_code == 200:
                    result_soup = BeautifulSoup(response2, 'html.parser')
                    unavailability_message = result_soup.find('span', {'id': 'plhMain_lblMsg'})

                    if unavailability_message and unavailability_message.text:
                        await app.send_message(user_chat_id, f"Error: {unavailability_message.text}")
                    else:
                        await app.send_message(user_chat_id, f"{time.ctime()} : Available Appointment Dates")
                else:
                    await app.send_message(user_chat_id, f"Failed to submit the form. Status code: {status_code}")

            except Exception as e:
                await app.send_message(user_chat_id, f"An error occurred: {str(e)}")

        # Wait for 60 seconds before the next check
        await asyncio.sleep(60)


# Command: /start
@app.on_message(filters.command("start"))
async def start(client, message):
    print("Bot started by user:", message.chat.id)
    global user_chat_id
    user_chat_id = message.chat.id
    await message.reply(f"Welcome! Now started checking for appointments every 60 seconds.\n\nCreated by: {creator_telegram} | {creator_github} | {creator_email}")

    # Start the periodic task if it’s not already running
    asyncio.create_task(check_appointments_periodically())

# Command: /stop
@app.on_message(filters.command("stop"))
async def stop_checking(client, message):
    global user_chat_id
    user_chat_id = None
    await message.reply("Stopped checking for appointments.")

# Run the bot
app.run()
