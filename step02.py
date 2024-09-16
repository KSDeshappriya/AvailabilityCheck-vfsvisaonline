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

# Get the initial page to extract cookies and view state
response = session.get(url, headers=headers)
response.raise_for_status()
initial_soup = BeautifulSoup(response.text, 'html.parser')

# Extract hidden form fields
view_state = initial_soup.find('input', {'name': '__VIEWSTATE'})['value']
event_validation = initial_soup.find('input', {'name': '__EVENTVALIDATION'})['value']

# Define the payload for the form submission
payload = {
    '__EVENTTARGET': 'ctl00$plhMain$lnkSchApp',
    '__EVENTARGUMENT': '',
    '__VIEWSTATE': view_state,
    '__VIEWSTATEGENERATOR': 'B57DB8CB',
    '____Ticket': '1',
    '__VIEWSTATEENCRYPTED': '',
    '__EVENTVALIDATION': event_validation
}

# Submit the form
response = session.post(url, headers=headers, data=payload)
response.raise_for_status()

# Parse the new page
new_page_soup = BeautifulSoup(response.text, 'html.parser')
print(new_page_soup.prettify())
