FROM alpine:3.10

RUN apk add --no-cache python3-dev \
&& pip3 install --upgrade pip

ENV PUBLIC_KEY "0485946f992426c58cba3c0d5d6bb823"
ENV PRIVATE_KEY "c19ae992eeaa5ebd439c9ea4b96efc631cc2894b"
ENV API_ENDPOINT "https://gateway.marvel.com:443/v1/public/"

WORKDIR /WORKDIR
ADD . /WORKDIR

COPY . /app/

RUN pip3 --no-cache-dir install -r requirements.txt

CMD ["python3", "src/app.py"]