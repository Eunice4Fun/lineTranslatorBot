FROM python:3.10-alpine


COPY ./ /LineBot
WORKDIR /LineBot

RUN pip3 install -r requirements.txt

CMD ["python3", "bot.py"]