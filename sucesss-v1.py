import requests
from bs4 import BeautifulSoup

# Define the URL and headers
url = 'https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppWelcome.aspx?P=b0KsiJlv+LIdjKDvIvW+nLNY7GnUFdfuwQj4DXbs4vo='

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
    "Cookie": "_cfuvid=kOCj8.C8RXrR1z02.eI8fNw9XTHQP41uggtsXLCGuT0-1726499190246-0.0.1.1-604800000; ASP.NET_SessionId=c5b0olldtpw1mi5ypno4bbkf; cf_chl_rc_i=1; __cf_bm=NACBx7F4a3S8F._foZKXfM58ZSxUCEjGoxXkrOe9lXY-1726505880-1.0.1.1-0zhhzQ20S00tGQc4OjBhrlLpZVDn5FGiDGE0SsywL9hMbh48Grw2WO5B.d.oLvwXaxWU7ksCaLVI5E9K9J9hdA; cf_clearance=gJwzq5_JIBvncPgayYgMMmLKcf090TDTE8.volph8fs-1726505883-1.2.1.1-y7GlBqyhJNFK33Uwgf25rWf0AJinsLhPJ0UBSwUYe7z_baziLseTigrTmjAG7XIKTJ1kAYVRFLzeHqG3jmSGZj3mBHN2k34PKcaxLlXLLWbuqa4k8qGpVxrFk2A1IkZY_Qc49iJsqMRfviAxK8BjA5w1.tCXie2yI37j3NLiZ7QwRiKSRTbc9xyqXAZ9PvoJsVKWu_yO4xs5W5bOHEPlyJO98H8KT6mGrBDTske354lwVQfVaODP7JCS1melvfmqjrZ0BOakt8mZA2dzMTtIPcn2.p2s2AczYRbfqyKlLZPidtw7bhH5JSONobK7XxWTmKSL75bQmf2KU.O2vfEgbu14akdfoLwYLV8obo.OIdm_Vxugq6rCDlbyfp6VsxsY"
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