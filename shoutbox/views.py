from shoutbox.models import *
from c_portal.models import *

from shoutbox.forms import *

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext


def list(request):
    shoutboxes = Box.objects.all()
    return render_to_response('list.django', locals())


def show(request, box_id):
    shoutbox = get_object_or_404(Box, id=box_id)
    return render_to_response('show.django', locals())


@login_required
def shout_add(request, box_id):
    try:
        redirect_to = request.GET['next']
    except:
        redirect_to = '/'
    if request.method == 'POST':
        form = AddShoutForm(request.POST)
        member = Member.objects.get(nickname=request.user.username)
        shoutbox = get_object_or_404(Box, id=box_id)
        if form.is_valid():
            shout = Shout()
            shout.box = shoutbox
            shout.nickname = member.nickname
            shout.shout = form.cleaned_data['shout']
            shout.save()
        else:
            form = AddShoutForm()
    return HttpResponseRedirect(redirect_to)


@login_required
def shout_delete(request, box_id, shout_id):
    try:
        redirect_to = request.GET['next']
    except:
        redirect_to = '/'
    shout = get_object_or_404(Shout, id=shout_id)
    if shout.nickname == request.user.username:
        shout.delete()
    return HttpResponseRedirect(redirect_to)


