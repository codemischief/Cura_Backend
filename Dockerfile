FROM python:3.10

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

ENV PORT 6789

COPY . /code/
CMD exec ./cloud-sql-proxy noted-terra-425611-e9:asia-south1:cura-app-pgdb --port 9999 &
CMD exec uvicorn main:app --host 0.0.0.0 --port ${PORT} --workers 1