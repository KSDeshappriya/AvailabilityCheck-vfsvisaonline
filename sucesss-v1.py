import requests
from bs4 import BeautifulSoup

# Define the URL and headers
url = 'https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppWelcome.aspx?P=b0KsiJlv+LIdjKDvIvW+nLNY7GnUFdfuwQj4DXbs4vo='

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Cookie": "_cfuvid=jnfcctE.Mup.ObFCvP2F7AbCYbpOOuPJR5xjsjKwnp0-1726461560229-0.0.1.1-604800000; ASP.NET_SessionId=krf1lbmuj5qetrfhv0yy04md; __cf_bm=51nuzL4FKJIpHIAtlnUN8eW03ycJKuhzQTprFfSy12c-1726522051-1.0.1.1-3cenHEqxaIhM3oXYETdUrNw0eJN2Rm6CrFYwwxLcjRGDoRwvb6LpOZND8AHH7Nx9obVPyazQRbsdzeXSHoC8VA; cf_clearance=eWugLbx9Cx0rF2HJPedsUSPeYOHWuBqaAD.M7g9Y5WM-1726522053-1.2.1.1-YFsI4xC9OJjVp5DcoJ1M1Giann5DMpUAQo.PBqD1QtE453FH.FU4mCbUGTTYDgUvJF6lMui5fKoj883phXFRUdWvFSWbKzA9SHt0lnaOBqImwNusi222dJeNsLUUDZ263v3MgOQJg7uPHc8Rdi68Hw88pSQTJW._1H2EwKPVAd5gFzuWZFzvf0VDzx5L7BrXR.J9ZpapZW_F5enzjnXn77dEITebCduIxRC1iscxMVEwnP3gbp5i6dGmlaLNH4jtXgUZ61iLVhwXIMS5oW1ygIeJkUYUK7VaEEzkMMaxhE0QN772sKElvE01Mfv9JSO5IAB89w9sRh.SKGTeZrDzuQ2hTwbCRabcOk86rWPxsucjHquAPE9e1UEoniIKvwfb"
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