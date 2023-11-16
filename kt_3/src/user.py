import json

from base_request import BaseRequest


def user_request(base_url: str) -> None:
    user_req = BaseRequest(
        base_url,
        headers={
            'Content-Type': 'application/json'
        }
    )

    # POST /user
    body = json.dumps({
        "id": 0,
        "username": "string",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "password": "string",
        "phone": "string",
        "userStatus": 0
    })
    user_req.post('user', '', body)

    # GET /user/{username}
    user_req.get('user', 'string')

    # PUT /user/{username}
    body = json.dumps({
        "id": 0,
        "username": "new_name",
        "firstName": "string",
        "lastName": "string",
        "email": "string",
        "password": "string",
        "phone": "string",
        "userStatus": 0
    })
    user_req.put('user', 'string', body)

    # DELETE /user/{username}
    user_req.delete('user', 'new_name')
