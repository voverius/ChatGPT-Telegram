
# Import python
FROM python:3.11-alpine
RUN apk update && apk add bash

# Set working directory
WORKDIR /app

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# COPY the code
COPY . /app

# start the server
CMD ["python", "./main.py"]
