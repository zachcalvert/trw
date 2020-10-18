import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bellybot.models import GroupMeBot


@csrf_exempt
@require_http_methods(["POST"])
def new_message(request):
    try:
        content = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        content = request.POST
    except Exception:
        return HttpResponse(status=204)

    try:
        message_content = content['text'].lower()
        sender = content['name']
    except KeyError:
        print('ERROR parsing GroupMe message: {}'.format(request.POST))
        return HttpResponse(status=204)

    if content["sender_type"] != "bot":
        GroupMeBot().respond(sender, message_content)

    return HttpResponse(status=204)
