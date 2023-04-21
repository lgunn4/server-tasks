FROM python:3.9.6

WORKDIR /app

# Copy the script and required libraries into the container
COPY . /app
RUN pip install exifread configparser extensions 

# Install cron
RUN apt-get update && apt-get -y install cron

# Specify that the script requires data to be mounted
# VOLUME /source_data
# VOLUME /destination_data

# Add crontab file in the cron directory
ADD crontab /etc/cron.d/simple-cron

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/simple-cron

# Create the log file to be able to run tail
RUN touch /var/log/cron.log

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
