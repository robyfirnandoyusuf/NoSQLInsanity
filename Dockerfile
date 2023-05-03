FROM python:3.8-slim-buster

LABEL description="NoSQLInsanity: Tool for Security Assesment NoSQL (Linear Search VS Binary Search)"
LABEL repository="https://github.com/robyfirnandoyusuf/NoSQLInsanity"
LABEL maintainer="Roby Firnando Yusuf "

WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .

# COPY --from=build / /
ENTRYPOINT ["python", "/app/NoSQLInsanity.py"]