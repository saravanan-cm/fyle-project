# Fyle Project  V1.0.1


## Languages and Tools involved
- Python, Flask, HTML/CSS, JavaScript, Heroku

## Methods and Params
- GET:  **https://fyle-project.herokuapp.com/banks**
- `ifsc, name, city` are used as query params

## Authentication headers
- API is authenticated using basic auth technique.
- `username and password` is required to authorize the API calls
- username = `testuser`
- password = `secretfyle`
- Sample curl request with Auth headers,
```
curl -X GET \
  'https://fyle-project.herokuapp.com/banks?ifsc=ZSBL0000341' \
  -H 'Authorization: Basic dGVzdHVzZXI6c2VjcmV0ZnlsZQ==' 
```

## Response formats
- `[UPDATE]` Response limited to 200 for all API queries for better performance
### Response for IFSC code based API calls
- GET: **https://fyle-project.herokuapp.com/banks?ifsc=ZSBL0000341**
 ```
  
  {
      "banks": [
          {
              "address": "HANSH AUTO MOBILS LONI GHAZIABAD",
              "bank_id": "101",
              "bank_name": "ZILA SAHAKRI BANK LIMITED GHAZIABAD",
              "branch": "LONI",
              "city": "LONI",
              "district": "GHAZIABAD",
              "ifsc": "ZSBL0000341",
              "state": "UTTAR PRADESH"
          }
      ],
      "count": 1,
      "status": 200
  }
```
### Response for Bank name and City based API calls (also works for partial names)
- GET: **https://fyle-project.herokuapp.com/banks?name=Zila shakari bank&city=Loni**
- This search also works with partial bank name or city names.
- Supports listing using either City name or Bank name or both. Returns the full list of response where bank/city names match. 
 ```
  
  {
      "banks": [
          {
              "address": "HANSH AUTO MOBILS LONI GHAZIABAD",
              "bank_id": "101",
              "bank_name": "ZILA SAHAKRI BANK LIMITED GHAZIABAD",
              "branch": "LONI",
              "city": "LONI",
              "district": "GHAZIABAD",
              "ifsc": "ZSBL0000341",
              "state": "UTTAR PRADESH"
          }
      ],
      "count": 1,
      "status": 200
  }
```

### Change Log
- V1.0.1 `[UPDATE]`
  - Integrated PostgreSQL.
  - Response limited to 200 for all API queries for better performance
  - Query param key changed from `bank_name` to `name` while making name and city API calls.

