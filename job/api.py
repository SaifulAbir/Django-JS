from rest_framework.decorators import api_view
from rest_framework.utils import json
from rest_framework.response import Response


@api_view(["POST"])
def joblist(request):
    received_json_data = json.loads(request.body)
    email = received_json_data["email"]

    data = {
        'status': 1,
        'code': 200,
        "message": 'ok',
        "result": {
            "user": {
                "email": email
            }
        }
    }

    return Response(data)