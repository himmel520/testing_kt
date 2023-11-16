import json

from base_request import BaseRequest


def store_request(base_url: str) -> None:
    store_req = BaseRequest(
        base_url,
        headers={
            'Content-Type': 'application/json'
        }
    )

    # POST /store/order
    body = json.dumps({
        "id": 1,
        "petId": 0,
        "quantity": 0,
        "shipDate": "2023-11-13T13:03:56.439Z",
        "status": "placed",
        "complete": True
    })
    store_req.post('store/order', '', body)

    # GET /store/order/{orderId}
    store_req.get('store/order', 1)

    # GET /store/inventory
    store_req.get('store/inventory', '')

    # DELETE /store/order/{orderId}
    store_req.delete('store/order', 1)
