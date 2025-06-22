# Dutch Embassy Appointment Availability Checker

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/KSDeshappriya/AvailabilityCheck-vfsvisaonline)

This project is designed to automate the appointment scheduling process for the Dutch embassy/consulate-general in London using Python's `requests` and `BeautifulSoup` libraries for web scraping and Appointment Availability Checking.

## Project Overview

The script performs the following tasks:
1. Fetches the initial page to extract necessary hidden form fields.
2. Submits a form to navigate to the next step of the scheduling process.
3. Extracts additional hidden fields and submits another form to proceed further.

## Requirements

- Python 3.x
- `requests` library
- `beautifulsoup4` library

You can install the required libraries using pip:

```bash
pip install requests beautifulsoup4
```

## Script Breakdown 
(success-v1.py)

1. **Initial Page Request**

   - The script starts by making a GET request to the appointment scheduling URL to gather cookies and hidden fields needed for form submissions.
   - Hidden fields like `__VIEWSTATE`, `__VIEWSTATEGENERATOR`, and `__EVENTVALIDATION` are extracted from the response.

2. **Form Submission**

   - The first form submission navigates to the appointment scheduling page.
   - The script submits the necessary data, including event target and argument parameters, along with hidden fields.

3. **Subsequent Form Handling**

   - After receiving the new page's response, additional hidden fields are extracted.
   - The script submits another form with updated data, including the number of applicants and visa category.

4. **Final Submission**

   - The script then submits the final form with the gathered information and extracts the data required for booking an appointment.
   - The extracted data contains the available appointment slots, if any.
   - If available slots are found, the script prints them to the console, allowing the user to choose a suitable time.
   - If no slots are available, the script informs the user accordingly.


## Usage

**Clone the repository**:

```sh
git clone <repository-url>
cd <repository-directory>
```

### Step 1: Fist-Step Try


![Cloudflare](<docs/explain 01.png>)
![1st page](<docs/explain 02.png>)

*Cloudflare Protection --> Appointment Scheduling (01st page)*

```sh
python Step01.py
```

This script sets up the session, mounts a retry strategy, and makes the initial request to the VFS Global website.

### Step 2: Form Submission

![alt text](<docs/explain 03.png>)

```sh
python step02.py
```

This script extracts hidden form fields from the initial page, prepares the payload, and submits the form to proceed with the appointment scheduling process.

### Step 3: Availability Check

![alt text](<docs/explain 04.png>)
```sh
python sucesss-v1.py
```

This script continues the process by handling cookies, extracting additional hidden fields, and making further requests as needed.

## Notes

- Ensure that you have the necessary permissions and legal rights to scrape the VFS Global website.

## Notes

- Ensure that you have the correct URL and form parameters, as they may change over time.
- The script uses cookies and session handling to manage state across multiple requests.
- Make sure to comply with the website’s terms of service when scraping and submitting forms.

## Troubleshooting

- If you encounter issues with form submission, verify that the hidden fields and form parameters are correctly extracted and updated.
- Check for changes in the website's structure or parameters that may require updates to the script.

## Telegram Bot Integration

This project also includes a Telegram bot that can be deployed as a Docker container. You can find the bot's code and Dockerfile in the [`telegramBot`](./telegramBot/) directory. This bot allows you to check for appointment availability and receive notifications when slots open up, directly through Telegram. 

**To run the bot:**

1. **Build the Docker image:** 
   ```bash
   cd telegramBot
   docker build -t telegram-bot .
   ```

## License

This project is licensed under the **CC BY-NC 4.0 License**. See the [LICENSE](https://creativecommons.org/licenses/by-nc/4.0/) file for more details.

## Contact

For any questions or issues, please contact [ksdeshappriya.official@gmail.com](ksdeshappriya.official@gmail.com).
