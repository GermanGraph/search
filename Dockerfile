FROM python:3.6

WORKDIR /usr/src/app

RUN apt-get install git && pip install --no-cache-dir \
    aiodns==1.1.1 \
    aiohttp==2.3.2 \
    aiohttp-cors==0.5.3 \
    async-timeout==2.0.0 \
    cchardet==2.1.1 \
    chardet==3.0.4 \
    evalidate==0.7.1 \
    git+http://test:testtesttest@37.46.129.197:10080/i2rdt/MrRest.git \
    multidict==3.3.2 \
    pycares==2.3.0 \
    typing==3.6.2 \
    yarl==0.14.2 \
    psycopg2 \
    peewee

COPY app.py ./app.py
COPY prod_db.py ./db.py

ENTRYPOINT ["python", "app.py"]
