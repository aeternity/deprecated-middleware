# aepp-middleware
A middleware layer on top of Epoch

## Installation

```
git clone https://github.com/aeternity/aepp-middleware
```

### Environment variables

Create an `.env` file in the root directory fullfilling the variable set:

```
SECRET_KEY=<A SECRET FOR THE DJANGO SERVER>

ALLOWED_HOSTS=<COMMA SEPARATED LIST OF ALLOWED HOSTS>
EPOCH_PASSWORD=secret

```

### Start the application

```
EPOCH_PORT=3013 APP_PORT=8000 docker-compose up -d
```

## Usage

### Faucet

Curl example
```
curl -X POST \
  http://<YOUR PUBLIC PORT>:<APP_PORT>/faucet/ \
  -H 'content-type: application/json' \
  -d '{
	"key": "<PUBLIC KEY>",
	"amount": 1
}'
```


