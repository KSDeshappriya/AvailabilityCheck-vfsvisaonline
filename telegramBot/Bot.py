from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage
import time
import asyncio

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
    driver = ChromiumPage()
    driver.get(url)
    
    cf_bypasser = CloudflareBypasser(driver)
    cf_bypasser.bypass()

    # Get headers and close the driver
    headers = cf_bypasser.get_headers()
    driver.quit()
    
    return headers

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

                # Create a session to handle cookies and requests
                session = requests.Session()

                # Step 1: Get the initial page to extract hidden form fields
                response = session.get(url, headers=global_headers)
                
                # If the response status is not 200, reload the driver and bypass Cloudflare again
                if response.status_code != 200:
                    await app.send_message(user_chat_id, "Error: Response status not 200, reloading driver...")
                    global_headers = load_driver_and_bypass()
                    response = session.get(url, headers=global_headers)

                response.raise_for_status()

                # Parse the initial page
                initial_soup = BeautifulSoup(response.text, 'html.parser')

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
                response1 = session.post(url, headers=global_headers, data=payload_1)
                response1.raise_for_status()

                # Step 2: Parse the new page after the first submission
                new_page_soup = BeautifulSoup(response1.text, 'html.parser')

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
                response2 = session.post(submit_url, headers=global_headers, data=form_data)
                response2.raise_for_status()

                if response2.status_code == 200:
                    result_soup = BeautifulSoup(response2.text, 'html.parser')
                    error_message = result_soup.find('span', {'id': 'plhMain_lblMsg'})

                    if error_message and error_message.text:
                        await app.send_message(user_chat_id, f"Error: {error_message.text}")
                    else:
                        await app.send_message(user_chat_id, f"{time.ctime()} : Available Appointment Dates")
                else:
                    await app.send_message(user_chat_id, f"Failed to submit the form. Status code: {response2.status_code}")

            except Exception as e:
                await app.send_message(user_chat_id, f"An error occurred: {str(e)}")

        # Wait for 60 seconds before the next check
        await asyncio.sleep(60)

# Command: /start
@app.on_message(filters.command("start"))
async def start(client, message):
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