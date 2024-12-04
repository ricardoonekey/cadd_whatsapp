# Set base image (host OS)
FROM python:3.12-alpine

# By default, listen on port 5000
EXPOSE 5000/tcp

# Set the working directory in the container
WORKDIR /app

# Copy the dependencies file to the working directory
COPY requirements.txt .
COPY config.ini .

# Install any dependencies
RUN apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY __main__.py .

# Specify the command to run on container start
CMD [ "python", "./__main__.py" ]
