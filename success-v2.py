import requests
from bs4 import BeautifulSoup
from DrissionPage import ChromiumPage
from CloudflareBypasser import CloudflareBypasser
import time

# URL of the website to scrape
url = 'https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppWelcome.aspx?P=b0KsiJlv+LIdjKDvIvW+nLNY7GnUFdfuwQj4DXbs4vo='

# Initialize the browser and bypass Cloudflare
driver = ChromiumPage()
driver.get(url)

cf_bypasser = CloudflareBypasser(driver)
cf_bypasser.bypass()

# Extract headers from ChromiumPage to mimic the real browser
headers = cf_bypasser.get_headers()

# Close the driver as we don't need it anymore
driver.quit()

# Create a session to handle cookies and requests
session = requests.Session()

# Step 1: Get the initial page to extract hidden form fields
response = session.get(url, headers=headers)
print(response.status_code)  # Debugging line
response.raise_for_status()

# Parse the initial page
initial_soup = BeautifulSoup(response.text, 'html.parser')

# Extract hidden form fields from the first page
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
response1 = session.post(url, headers=headers ,data=payload_1)
print(response1.status_code)  # Debugging line
response1.raise_for_status()

# Step 2: Parse the new page after the first submission
new_page_soup = BeautifulSoup(response1.text, 'html.parser')

# Extract hidden fields
hidden_inputs = new_page_soup.find_all('input', type='hidden')
form_data = {input.get('name'): input.get('value') for input in hidden_inputs}

# Add additional form data for submission
form_data.update({
    'ctl00$plhMain$tbxNumOfApplicants': '1',  # Number of applicants
    'ctl00$plhMain$cboVisaCategory': '966',   # Visa category for Passport
    'ctl00$plhMain$btnSubmit': 'Continue'
})

# Submit the second form
submit_url = 'https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppSchedulingGetInfo.aspx?P=wpmn7S46C72lQRV%2f1kDyNQ%3d%3d'
response2 = session.post(submit_url, headers=headers ,data=form_data)
print(response2.status_code)  # Debugging line

# Check the response
if response2.status_code == 200:
    print("Form submitted successfully.")
    # Parse and print the resulting page
    result_soup = BeautifulSoup(response2.text, 'html.parser')

    # <span class="Validation" id="plhMain_lblMsg">
    error_message = result_soup.find('span', {'id': 'plhMain_lblMsg'})
    if error_message.text:
        print(error_message.text)
    else:
        print(f"{time.ctime()} : Available Appointment Dates")
        # print(result_soup.prettify())
else:
    print(f"Failed to submit form. Status code: {response2.status_code}")
    print(response2.text)  # Debugging line
