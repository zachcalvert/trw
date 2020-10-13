from django.http import HttpResponse
from django.views.decorators.http import require_http_methods

from bellybot.models import GroupMeBot


@require_http_methods(["POST"])
def new_message(request):
    # if 'group_id' not in request.POST or request.POST['group_id'] != '63320852':
    #     return HttpResponse(status=204)

    try:
        bot = GroupMeBot()
        message_content = request.POST['text']
        sender = request.POST['name']
    except KeyError:
        print('ERROR parsing GroupMe message: {}'.format(request.POST))
        return

    bot.respond(sender, message_content)
    return HttpResponse(status=204)




