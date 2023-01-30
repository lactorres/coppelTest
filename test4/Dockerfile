FROM alpine:3.10

RUN apk add --no-cache python3-dev \
&& pip3 install --upgrade pip

ENV URI "mongodb+srv://testdb:aCw14lPb6QTfW3dl@cluster0.fxzchei.mongodb.net/?retryWrites=true&w=majority"

WORKDIR /WORKDIR
ADD . /WORKDIR

COPY . /app/

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3", "src/app.py"]