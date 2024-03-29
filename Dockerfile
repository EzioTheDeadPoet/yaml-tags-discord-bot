FROM python:3.12

COPY requirements.txt ./

RUN pip install -U -r requirements.txt

COPY . .

CMD ["python","main.py"]