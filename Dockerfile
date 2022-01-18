FROM tiangolo/uvicorn-gunicorn:python3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY ./requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 80

COPY . .

CMD [ "python3", "wsgi.py" ]
