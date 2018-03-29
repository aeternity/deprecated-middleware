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

### Epoch configuration

The repository contains an Epoch configuration file which has to be edited in order to make the node inside the docker network sync with the testnet:

In `docker/epoch/epoch_config.yaml` change
```
...
http:
    external:
        peer_address: http://epoch:3013/
...

```

to 
```
http:
    external:
        peer_address: <YOUR_PUBLIC_IP_AND_PORT>/
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
  http://<YOUR PUBLIC IP>:<APP_PORT>/faucet/ \
  -H 'content-type: application/json' \
  -d '{
	"key": "<PUBLIC KEY>",
	"amount": 1
}'
```

## License

ISC

