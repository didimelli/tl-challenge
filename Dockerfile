FROM python:3.11-alpine

WORKDIR /opt/tl_challenge
ENV PYTHONPATH=/opt/tl_challenge

COPY requirements.txt ./
RUN python -m pip install -r requirements.txt

COPY ./tl_challenge/*.py ./tl_challenge/

EXPOSE 8000

CMD uvicorn tl_challenge.app:app --host 0.0.0.0
