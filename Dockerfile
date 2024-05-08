FROM python:3.12

# Установка telnet
RUN apt-get update && apt-get install -y telnet

WORKDIR /usr/src/app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]

#CMD ["python", "main.py"]

EXPOSE 80/tcp
