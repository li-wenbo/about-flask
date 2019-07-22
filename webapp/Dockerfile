FROM python:3.6.8-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install -i http://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com -r requirements.txt

ARG user=gunicorn
ARG group=gunicorn
ARG uid=1000
ARG gid=1000

RUN addgroup --gid ${gid} ${group} \
    && adduser --uid ${uid} --gid ${gid} --disabled-password --disabled-login --gecos '' --home /var/lib/${user} ${user}

RUN mkdir logs

RUN chown -R ${uid}:${gid} /app

USER ${user}



# Make port 80 available to the world outside this container
EXPOSE 8888

# Run app.py when the container launches
ENTRYPOINT ["gunicorn", "-c", "gunicorn_conf.py", "main:app"]

