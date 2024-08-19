FROM python:3.12.4-alpine AS base
WORKDIR /app
ADD src .
RUN apk update && \
  apk upgrade && \
  apk add --no-cache -u && \
  rm -rf /var/cache/apk/*
RUN python -m pip install --upgrade pip && \
  python -m pip install pyOpenSSL

FROM base AS frontend
RUN rm web_api.py sql_server.py
CMD python run.py

FROM base AS api
RUN python -m pip install SQLAlchemy mysql-connector-python
RUN sed -i -E -e '21i \ \ \ \ sql_server.init_db()' \
  -e 's/(import\ )(https_server)/\1sql_server,\ \2/g' core.py && \
  sed -i -e 's/web_page/web_api/g' https_server.py && \
  rm web_page.py && \
  rm -r web
CMD python run.py