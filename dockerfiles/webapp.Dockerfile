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
RUN sed -i -E -e '21i \ \ \ \ session = sql_server.main()' \
  -e 's/(import\ )(https_server)/\1sql_server,\ \2/g' \
  -e 's/(https_server.parse_args\(\))/\1,\ session/g' core.py && \
  sed -i -e 's/web_page/web_api/g' \
  -e 's/WebRequestHandler/WebRequestHandler\(session\)/g' https_server.py && \
  rm web_page.py && \
  rm -r web
CMD python run.py