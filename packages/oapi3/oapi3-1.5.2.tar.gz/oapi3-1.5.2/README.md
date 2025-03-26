# oapi3
Validator of openapi3 Requests and Responses

1. Open and resolve openapi3 schema

```
>>>    import openapi3
>>>    schema = openapi3.open_schema('api.yaml')
```

2. Validate requests and responses


```
>>>    schema.validate_request(path, operation, query, media_type, body)
>>>    schema.validate_response(path, operation, status_code, media_type, body)
```

3. Create client to remote api

```
>>>    client = oapi3.Client('http://server/api', schema)
>>>    client.operations['some.operation_id'](
>>>        params={'item_id': 10},
>>>        body={'some_key': 'some_date'},
>>>    )
```
