FROM python:3.10-slim-buster as build

ENV PYTHONUNBUFFERED=1
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone


WORKDIR /app
RUN python -m venv /app/venv
ENV PATH="/app/venv/bin:$PATH"

COPY requirements.txt ./
RUN pip install --upgrade pip &&\
    pip install -r requirements.txt

FROM python:3.10-slim-buster
WORKDIR /app
COPY --from=build /app/venv ./venv


COPY settings.py .
COPY main.py .

COPY entrypoint.sh .
RUN chmod +x entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]

