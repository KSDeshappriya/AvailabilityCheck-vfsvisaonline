# Use Python 3.12.6 as the base image
FROM python:3.12.6-slim

# Install necessary packages for Chrome and chromedriver
RUN apt-get update && \
    apt-get install -y wget gnupg --no-install-recommends && \
    apt-get install -y \
    libx11-xcb1 \
    libx11-dev \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libxss1 \
    libnss3 \
    libgdk-pixbuf2.0-0 \
    libgtk-3-0 \
    libgbm1 \
    fonts-liberation \
    libappindicator3-1 \
    libasound2 \
    libnspr4 \
    libu2f-udev \
    libcurl4 \
    libdrm2 \
    lsb-release \
    unzip \
    xvfb \
    && apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Add Google Chrome repository
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list'

# Install Google Chrome
RUN apt-get update && \
    apt-get install -y google-chrome-stable --no-install-recommends && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install chromedriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/100.0.4896.20/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Set Chrome and ChromeDriver environment variables
ENV CHROME_BIN=/usr/bin/google-chrome
ENV CHROMEDRIVER=/usr/local/bin/chromiumbrowser

# Copy Python files to the container
COPY Bot200E.py .
COPY Cred.py .
COPY CloudflareBypasser.py .
COPY requirements.txt .

# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt
RUN pip3 install pyvirtualdisplay

# EXPOSE 9222

CMD ["python3", "Bot200E.py"]