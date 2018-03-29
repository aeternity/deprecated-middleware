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
CORS_ORIGIN_WHITELIST=<COMMA SEPARATED LIST OF CORS WHITLISTED HOSTS>

EPOCH_PASSWORD=secret

GITHUB_OAUTH_CLIENT_SECRET=<YOUR GIRHUB OAUTH CLIENT SECRET>
GITHUB_OAUTH_CLIENT_ID=<YOUR GIRHUB OAUTH CLIENT ID>
```

### Start the application

```
docker-compose up -d
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


