import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bellybot.bbot import BellyBot, TestBot


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
        user_id = content['user_id']
    except KeyError:
        print('ERROR parsing GroupMe message: {}'.format(request.POST))
        return HttpResponse(status=204)

    if content["sender_type"] != "bot":
        bot = BellyBot()
        bot.respond(sender, user_id, message_content)

        if "bass" in message_content:
            print('someone mentioned the bass god')
            conversation_id = content['group_id']
            message_id = content['message_id']
            bot.like_message(conversation_id, message_id)

    return HttpResponse(status=204)


@csrf_exempt
@require_http_methods(["POST"])
def new_test_message(request):
    try:
        content = json.loads(request.body)
    except json.decoder.JSONDecodeError:
        content = request.POST
    except Exception:
        return HttpResponse(status=204)

    try:
        message_content = content['text'].lower()
        sender = content['name']
        user_id = content['user_id']
    except KeyError:
        print('ERROR parsing GroupMe message: {}'.format(request.POST))
        return HttpResponse(status=204)

    if content["sender_type"] != "bot":
        TestBot().respond(sender, user_id, message_content)

    return HttpResponse(status=204)
