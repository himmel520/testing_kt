FROM python

WORKDIR /client

COPY /client .
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

CMD pytest -s