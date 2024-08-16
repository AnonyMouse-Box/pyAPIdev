FROM python:3.12.4-alpine AS base
WORKDIR /app
ADD src .
RUN apk update && \
  apk upgrade && \
  apk add --no-cache -u && \
  rm -rf /var/cache/apk/*
RUN python -m pip install --upgrade pip

FROM base AS ssl
RUN python -m pip install pyOpenSSL
RUN rm sql_server.py

FROM ssl AS frontend
RUN rm web_api.py
CMD python run.py

FROM ssl AS api
RUN sed -i -e 's/web_page/web_api/g' https_server.py && \
  rm web_page.py && \
  rm -r web
CMD python run.py

FROM base AS db
RUN python -m pip install SQLAlchemy
RUN sed -i -e 's/https_server\.parse_args()//g' -e 's/https_server/sql_server/g' core.py && \
  rm web_api.py web_page.py https_server.py self_signed.py && \
  rm -r web
CMD python run.py