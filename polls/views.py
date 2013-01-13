from polls.models import *

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required


def poll_view(request, poll_id):
    return HttpResponse('poll_view')


@login_required
def vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    nickname = request.user.username
    if not nickname in [m.username for m in poll.participants.all()]:
        try:
            selected_choice = poll.choice_set.get(pk=request.POST['choice'])
            selected_choice.votes += 1
            selected_choice.save()
            poll.participants.add(request.user)
            poll.save()
        except: pass
    return HttpResponseRedirect('/members/%s/' % request.user.username)
