## Python SDK for GTN Embed
<img src="https://img.shields.io/badge/Python-3.10 -- 3.12-green"/>

This is a lightweight SDK which wraps the REST APIs of the GTN Embed set as documented in the [API Portal](https://developer.globaltradingnetwork.com/rest-api-reference)

### installing packages
The GTN Embed SDK is available on PYPI. Install with pip:<br>
```bash
    pip install gtn-embed-sdk
```

### API Authentication
The GTN Embed uses the notion of Institutions, which represent customers that build their platform upon the GTN Embed. 
The end-users of the institution, are referred to as customers. 
An institution is able to manage their customers directly and is also able to initiate actions on the user's behalf.

As describe in the [API Portal](https://developer.globaltradingnetwork.com/rest-api-reference) you are required to authenticate
first to the Institution and then as a customer. And resulting keys expire in a certain period, which require
renewing using authentication APIs. However when using the SDK, key renewing is not required since it is 
handled by the SDK in background.

The <code>api_url</code> is the API hub where customers are connected to access the GTN Embed. This URL can change depending on 
customer's registered country.

#### Initiating API connection
For a connection to be establish, it is required to have following information
  * API URL, provided by GTN. Can vary depending on the environment (Sandbox, UAT, Production)
  * App Key, provided by GTN
  * App Secret, provided by GTN
  * Institution Code, provided by GTN
  * Customer Number of the customer initiating the connection. (Optional: only in the customer mode)
  * Private Key of the institution, provided by GTN

```python
    import gtnapi

    api_data = {
        "api_url": "https://api-mena-uat.globaltradingnetwork.com",
        "app_key": "my-app-key",
        "app_secret": "my-app-secret",
        "institution": "MY-INST-CODE",
        "customer_number": "12345678",
        "private_key": "RTRGDBCNKVGJTURI49857YURIEOLFMKJTU5I4O847YRHFJDKDKVFLKTUEJFHRU"
    }

    status = gtnapi.init(**api_data)
```

authentication **status** is in the format
```json
    {
        "http_status": 200, 
        "auth_status": "SUCCESS"
    }
```
Once the _**gtnapi.init()**_ is success (i.e. <code>http_code == 200</code>), it is possible to access any REST endpoint (authorised to the customer) by using the SDK

### Getting customer details
```python
    response = gtnapi.Requests.get('/trade/bo/v1.2.1/customer/account', customerNumber="12345678")
    print(json.dumps(response, indent=4))
```
Response is in the format
```python
    {
        "http_status" : 200,  # http status of the api call as per the API documentation
        "response" : {data dict}  # response data of the api as per the API documentation
    }
```
### Getting market data
```python
    search_params = {
        "source-id": 'DFM',
        "keys": "DFM~EMAAR"
    }
    response = gtnapi.Requests.get('/market-data/realtime/keys/data', **search_params)
    print(json.dumps(response, indent=4))
``````
### Initiate the market data websocket connection
Can initiate the WS session by passing call-back method references 
```python
    gtnapi.Streaming.MarketData.connect(on_open, on_message, on_error, on_close)
```
### close the websocket connection
can close the WS session by calling
```python
    gtnapi.Streaming.MarketData.disconnect()
```
### terminate the session
The while GTN Embed session will be terminated by calling the following
```python
    gtnapi.stop()
```