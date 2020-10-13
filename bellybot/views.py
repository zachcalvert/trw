from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from bellybot.models import GroupMeBot


@csrf_exempt
@require_http_methods(["POST"])
def new_message(request):
    # if 'group_id' not in request.POST or request.POST['group_id'] != '63320852':
    #     return HttpResponse(status=204)

    try:
        message_content = request.POST['text']
        sender = request.POST['name']
    except KeyError:
        print('ERROR parsing GroupMe message: {}'.format(request.POST))
        return

    GroupMeBot().respond(sender, message_content)
    return HttpResponse(status=204)




