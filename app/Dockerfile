FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8000

WORKDIR /app

RUN pip --no-cache-dir install --upgrade pip
COPY ./requirements.txt .
RUN pip install --no-cache-dir --root-user-action=ignore -r requirements.txt

COPY . .

COPY ./entrypoint.sh .
RUN chmod +x entrypoint.sh

ENTRYPOINT ["sh", "entrypoint.sh"]
