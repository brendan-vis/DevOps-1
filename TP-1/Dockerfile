FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN useradd -m brendan

USER brendan

EXPOSE 8000

CMD ["python", "main.py"]