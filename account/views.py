from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from django.contrib.auth import login, logout, authenticate

from account.forms import LoginForm
from c_portal.models import *

REDIRECT_TO = 'https://c-portal.c-base.org/'

def auth_login( request ):
    members = Member.objects.active()
    projects = Project.objects.all()
    redirect_to = request.REQUEST.get( 'next', '' ) or REDIRECT_TO
    if request.method == 'POST':
        form = LoginForm( request.POST )
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate( username=username, password=password )
            if user is not None:
                if user.is_active:
                    login( request, user )
                    member, created = Member.objects.get_or_create(
                            nickname=username)
                    if created:
                        member.save()
                    return HttpResponseRedirect( redirect_to )
    else:
        form = LoginForm()
    return render_to_response( 'login.django', RequestContext( request, locals() ) )

def auth_logout( request ):
    redirect_to = request.REQUEST.get( 'next', '' ) or REDIRECT_TO
    logout( request )
    return HttpResponseRedirect( redirect_to )

def c_profile(request):
    members = Member.objects.active()
    projects = Project.objects.all()
    return render_to_response( 'c-profile.django', locals() )

