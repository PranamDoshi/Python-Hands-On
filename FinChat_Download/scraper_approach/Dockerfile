# Specify the base image
# FROM --platform=linux/amd64 python:3.10.10-slim-bullseye
FROM --platform=linux/amd64 python:3.11.2-slim-bullseye 

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    WORKDIR=/home/ubuntu \
    APP_ROOT=/home/ubuntu

# Set the working directory
WORKDIR $WORKDIR

# Install Chrome and Chromedriver dependencies
RUN apt-get update \
    && apt-get -y install xvfb unzip wget gnupg gnupg1 gnupg2 apt-transport-https ca-certificates hicolor-icon-theme libcanberra-gtk* libgl1-mesa-dri libgl1-mesa-glx libpangox-1.0-0 libpulse0 libv4l-0 fonts-symbola libgtk-3-0 libasound2 libdbus-glib-1-2 --no-install-recommends \
    && rm -rf /var/lib/apt/lists/* 

# # Install Chrome
# RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
#     && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list \
#     && apt-get update -qqy --no-install-recommends \
#     && apt-get install -qqy --no-install-recommends google-chrome-stable \
#     && rm -rf /var/lib/apt/lists/*

# # Install Chromedriver
# RUN CHROME_VERSION=$(google-chrome-stable --version | awk '{print $3}' | cut -d '.' -f 1) \
#     && CHROMEDRIVER_VERSION=$(wget -q -O - https://chromedriver.storage.googleapis.com/LATEST_RELEASE_$CHROME_VERSION) \
#     && wget -q -O /tmp/chromedriver_linux64.zip https://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip \
#     && unzip -qq /tmp/chromedriver_linux64.zip -d $WORKDIR \
#     && rm /tmp/chromedriver_linux64.zip \
#     && chmod +x $WORKDIR/chromedriver

# Install latest stable Chromedriver
RUN wget -qq chromedriver.storage.googleapis.com/LATEST_RELEASE \
    # && CHROME_VERSION=$(cat LATEST_RELEASE) \
    # && mv LATEST_RELEASE chromedriver_LATEST_RELEASE \
    # && wget -q -O /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROME_VERSION/chromedriver_linux64.zip \
    # Downloading the latest Chrome release from a different source, Uncomment above 3 line and comment out below line if need to change it to latest realease. 
    && wget -q -O /tmp/chromedriver_linux64.zip https://storage.googleapis.com/chrome-for-testing-public/124.0.6367.91/linux64/chromedriver-linux64.zip \
    && unzip -qq /tmp/chromedriver_linux64.zip -d $WORKDIR \
    && rm -r /tmp/chromedriver_linux64.zip \
    # Comment out below line when switing to latest releases setup.
    && mv $WORKDIR/chromedriver-linux64/chromedriver $WORKDIR \
    && chmod +x $WORKDIR/chromedriver

# Install Chrome compatible with downloaded Chromedriver (Which is the Latest One.)
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && sh -c 'echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list' \
    && apt-get update -qqy --no-install-recommends && apt-get install -qqy --no-install-recommends google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Install Geckodriver
RUN GECKODRIVER_VERSION=$(wget -qO - https://github.com/mozilla/geckodriver/releases/latest | grep -oP '(?<=tag/)[^"]+' | sed -n '2p') \
    && echo "$GECKODRIVER_VERSION" > geckodriver_LATEST_RELEASE \
    && wget -O geckodriver.tar.gz https://github.com/mozilla/geckodriver/releases/download/${GECKODRIVER_VERSION}/geckodriver-${GECKODRIVER_VERSION}-linux64.tar.gz \
    && tar -xzf geckodriver.tar.gz \
    && rm -r geckodriver.tar.gz \
    && chmod +x geckodriver

# Install Python dependencies
COPY ./requirements.txt $WORKDIR/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . $APP_ROOT/

# Set ownership and permissions
RUN groupadd -r ubuntu && useradd -r -g ubuntu ubuntu \
    && mkdir -p /nonexistent/.local/share/applications \
    && chown -R ubuntu:ubuntu /nonexistent $WORKDIR

# Create and provid permissions to write to log files.
RUN mkdir /home/ubuntu/logs \
    && chown -R ubuntu:ubuntu /home/ubuntu/logs \
    && chmod -R 777 /home/ubuntu/logs

# Switch to a non-root user
USER ubuntu

# Specify the command to run the Python script
# CMD python3 $APP_ROOT/pdp_links_scraper/testCode/test_pdp_extraction_service_general.py
CMD python3 $APP_ROOT/main.py
