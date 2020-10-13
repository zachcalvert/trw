import json

from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bellybot.models import GroupMeBot


@csrf_exempt
@require_http_methods(["POST"])
def new_message(request):
    # if 'group_id' not in request.POST or request.POST['group_id'] != '63320852':
    #     return HttpResponse(status=204)

    print(request.body)
    content = json.loads(request.body)

    try:
        message_content = content['text']
        sender = content['name']
    except KeyError:
        print('ERROR parsing GroupMe message: {}'.format(request.POST))
        return HttpResponse(status=204)

    GroupMeBot().respond(sender, message_content)
    return HttpResponse(status=204)




