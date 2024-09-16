import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


url = 'https://www.vfsvisaonline.com/Netherlands-Global-Online-Appointment_Zone2/AppScheduling/AppWelcome.aspx?P=b0KsiJlv+LIdjKDvIvW+nLNY7GnUFdfuwQj4DXbs4vo='

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:129.0) Gecko/20100101 Firefox/129.0",
   "Cookie": "_cfuvid=kOCj8.C8RXrR1z02.eI8fNw9XTHQP41uggtsXLCGuT0-1726499190246-0.0.1.1-604800000; ASP.NET_SessionId=c5b0olldtpw1mi5ypno4bbkf; cf_chl_rc_i=1; __cf_bm=NACBx7F4a3S8F._foZKXfM58ZSxUCEjGoxXkrOe9lXY-1726505880-1.0.1.1-0zhhzQ20S00tGQc4OjBhrlLpZVDn5FGiDGE0SsywL9hMbh48Grw2WO5B.d.oLvwXaxWU7ksCaLVI5E9K9J9hdA; cf_clearance=gJwzq5_JIBvncPgayYgMMmLKcf090TDTE8.volph8fs-1726505883-1.2.1.1-y7GlBqyhJNFK33Uwgf25rWf0AJinsLhPJ0UBSwUYe7z_baziLseTigrTmjAG7XIKTJ1kAYVRFLzeHqG3jmSGZj3mBHN2k34PKcaxLlXLLWbuqa4k8qGpVxrFk2A1IkZY_Qc49iJsqMRfviAxK8BjA5w1.tCXie2yI37j3NLiZ7QwRiKSRTbc9xyqXAZ9PvoJsVKWu_yO4xs5W5bOHEPlyJO98H8KT6mGrBDTske354lwVQfVaODP7JCS1melvfmqjrZ0BOakt8mZA2dzMTtIPcn2.p2s2AczYRbfqyKlLZPidtw7bhH5JSONobK7XxWTmKSL75bQmf2KU.O2vfEgbu14akdfoLwYLV8obo.OIdm_Vxugq6rCDlbyfp6VsxsY"
}

# Create a session
session = requests.Session()

# Define a retry strategy
retry_strategy = Retry(
    total=3,  # Number of retries
    status_forcelist=[429, 500, 502, 503, 504],  # Retry on these status codes
    allowed_methods=["HEAD", "GET", "OPTIONS", "POST"],  # Retry on these methods
    backoff_factor=1  # Wait time between retries
)

# Mount the retry strategy to the session
adapter = HTTPAdapter(max_retries=retry_strategy)
session.mount("https://", adapter)
session.mount("http://", adapter)

try:
    response = session.post(url, headers=headers, timeout=10)  # Set a timeout
    response.raise_for_status()  # Raise an exception for HTTP errors
    print(response.text)
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")