import requests
from bs4 import BeautifulSoup

# Define the URL and headers
url = 'https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppWelcome.aspx?P=b0KsiJlv+LIdjKDvIvW+nLNY7GnUFdfuwQj4DXbs4vo='

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
    "Cookie": "_cfuvid=rTDmecbeLxRMo4w1XZ.4NfzT2XgmM9ZFBUIQOd5Gpb0-1726643042327-0.0.1.1-604800000; cf_clearance=3meA3zIc_jSJgZBke0Mqg2Ic_Co4nxSWWACeKH_J.ro-1726642977-1.2.1.1-wEg9eDr8W1qXR1A_2uWSXRwQCSiAqm4bRFvxSMi2kBI5wjCvS2YKzI5cSO__4QPFVVKzqE6W5zShkhxi5xygoDTPc.4ZVasr.1ELN8fAZWjt3rcvob2NG9Hx3uec.isopcsDW6djS77M59CEJ6luT9n_1zqm0nyCyHZ4LUhPa4574OEpdu269iYeuMgSu1GH3u5Xvy3drpCwSa61Q0SvRoXTa228r38hOUpMsdFVp2wGfpM40suBOqslRN2O.omzCw3ZrHP8Wr9HtSYe_q5IKKlQs.QnT2wzmguNKmYkdCdEfyNH0Aea5Q8jgJyD1Qle0YwH3fEzP1BhiykV6EF1xCPGZyqiwZ6RxFTb0dZPK55h.4OCxmrY1Zr0EgaLvRuzNH5BnoOWPqpzID9oNHQrcxmaDLQBBbqAxJeKG0w0q9w; __cf_bm=crlhjpebQW57b1kZConVN2U_9zaXhYyEoHEb6Sas3v8-1726642958-1.0.1.1-6ufR47MzLXulT5eaDO47NHwCawDVLa9rk9zc0MYtrYOOm4s_yCW_4EzlAPdP5CA15bTY75ajUGtzv0g.HXyViQ;"
}

# Create a session to handle cookies
session = requests.Session()

# Step 1: Get the initial page to extract cookies and view state
response = session.get(url, headers=headers)
response.raise_for_status()

initial_soup = BeautifulSoup(response.text, 'html.parser')

# =================================================================================

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
response1 = session.post(url, headers=headers, data=payload_1)
response1.raise_for_status()

# Step 2: Parse the new page after the first submission
new_page_soup = BeautifulSoup(response1.text, 'html.parser')

# =================================================================================

# # Extract the hidden fields from the new form (second page)
# view_state = new_page_soup.find('input', {'name': '__VIEWSTATE'})['value']
# view_state_generator = new_page_soup.find('input', {'name': '__VIEWSTATEGENERATOR'})['value']
# event_validation = new_page_soup.find('input', {'name': '__EVENTVALIDATION'})['value']

# # Find the correct __EVENTTARGET for the second form submission
# # Ensure you use the correct button or link ID that triggers the form submission
# event_target = 'ctl00$plhMain$btnSubmit'  # This should be the ID of the submit button

# # Define the payload for the second form submission (visa type and details)
# payload_2 = {
#     '__EVENTTARGET': event_target,
#     '__EVENTARGUMENT': '',
#     '__VIEWSTATE': view_state,
#     '__VIEWSTATEGENERATOR': view_state_generator,
#     '__EVENTVALIDATION': event_validation,
#     'ctl00$plhMain$tbxNumOfApplicants': '1',  # Number of applicants
#     'ctl00$plhMain$cboVisaCategory': '966',  # Visa category ID
#     'ctl00$plhMain$btnSubmit': 'Continue'  # Button value to submit the form
# }

# # Step 3: Submit the second form with the required details
# response2 = session.post(url2, headers=headers, data=payload_2)
# response2.raise_for_status()

# # Step 4: Parse the resulting page after the second submission
# final_page_soup = BeautifulSoup(response2.text, 'html.parser')

# # Optional: Scrape the final page for information you need
# print(final_page_soup.prettify())

# Extract hidden fields
hidden_inputs = new_page_soup.find_all('input', type='hidden')
form_data = {input.get('name'): input.get('value') for input in hidden_inputs}

# Form data to submit
form_data.update({
    'ctl00$plhMain$tbxNumOfApplicants': '1',  # Number of applicants
    'ctl00$plhMain$cboVisaCategory': '966',   # Visa category for Passport
    'ctl00$plhMain$btnSubmit': 'Continue'
})

# Submit the form
submit_url = 'https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppSchedulingGetInfo.aspx?P=wpmn7S46C72lQRV%2f1kDyNQ%3d%3d'
response = session.post(submit_url, headers=headers, data=form_data)

# Check the response
if response.status_code == 200:
    print("Form submitted successfully.")
    # Parse the resulting page
    result_soup = BeautifulSoup(response.text, 'html.parser')
    print(result_soup.prettify())
else:
    print(f"Failed to submit form. Status code: {response.status_code}")