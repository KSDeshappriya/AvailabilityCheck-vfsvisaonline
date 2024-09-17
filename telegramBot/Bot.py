from pyrogram import Client, filters
import requests
from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage
import time

# Import external classes
from CloudflareBypasser import CloudflareBypasser
from Cred import Cred


# API ID and API hash from my.telegram.org
api_id = Cred.API_ID
api_hash = Cred.API_HASH
bot_token = Cred.BOT_TOKEN

# Initialize the bot client
app = Client("my_bot", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

# URL of the website to scrape
url = 'https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppWelcome.aspx?P=b0KsiJlv+LIdjKDvIvW+nLNY7GnUFdfuwQj4DXbs4vo='

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Welcome! Use /check to check for available appointments.")

@app.on_message(filters.command("check"))
async def check_appointments(client, message):
    try:
        await message.reply("Checking for available appointments, please wait...")

        # Initialize ChromiumPage and bypass Cloudflare
        driver = ChromiumPage()
        driver.get(url)

        cf_bypasser = CloudflareBypasser(driver)
        cf_bypasser.bypass()

        # Extract headers from ChromiumPage to mimic real browser behavior
        headers = cf_bypasser.get_headers()

        # Close the driver
        driver.quit()

        # Create a session to handle cookies and requests
        session = requests.Session()

        # Step 1: Get the initial page to extract hidden form fields
        response = session.get(url, headers=headers)
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
        response1 = session.post(url, headers=headers, data=payload_1)
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
        response2 = session.post(submit_url, headers=headers, data=form_data)
        response2.raise_for_status()

        if response2.status_code == 200:
            result_soup = BeautifulSoup(response2.text, 'html.parser')
            error_message = result_soup.find('span', {'id': 'plhMain_lblMsg'})
            
            if error_message and error_message.text:
                await message.reply(f"Error: {error_message.text}")
            else:
                await message.reply(f"{time.ctime()} : Available Appointment Dates")
                # Optionally send more info about the appointment dates
        else:
            await message.reply(f"Failed to submit the form. Status code: {response2.status_code}")

    except Exception as e:
        await message.reply(f"An error occurred: {str(e)}")

# Run the bot
app.run()
