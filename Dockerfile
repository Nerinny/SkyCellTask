FROM python:latest

WORKDIR /skycellapi

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest"]