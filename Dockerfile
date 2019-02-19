FROM python:3.7-stretch as builder
WORKDIR /install
COPY /app/requirements.txt /tmp/

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install -r /tmp/requirements.txt

FROM python:3.7-alpine as base
COPY --from=builder /opt/venv /opt/venv
COPY app /app/app
WORKDIR /app

ENV PATH="/opt/venv/bin:$PATH"
