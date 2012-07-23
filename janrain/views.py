from django.http import HttpResponseRedirect
from django.contrib import auth
from django.views.decorators.csrf import csrf_exempt

from janrain import api
from janrain.models import JanrainUser
from janrain.signals import *


@csrf_exempt
def login(request):
    pre_login.send(JanrainSignal, request=request)
    try:
        token = request.POST['token']
    except KeyError:
        # TODO: set ERROR to something
        login_failure.send(
            JanrainSignal,
            message='Error retreiving token',
            data=None
        )

        return HttpResponseRedirect('/')

    try:
        profile_data = api.auth_info(token)
    except api.JanrainAuthenticationError:
        login_failure.send(
            JanrainSignal,
            message='Error retreiving profile',
            data=None
        )

        return HttpResponseRedirect('/')

    post_profile_data.send(JanrainSignal, profile_data=profile_data)

    user = None
    profile = profile_data['profile']

    user = auth.authenticate(profile=profile)
    post_authenticate.send(
        JanrainSignal,
        user=user,
        profile_data=profile_data,
        request=request
    )

    if user is not None:
        janrain_user = JanrainUser.objects.get_or_create(
            user=user,
            username=profile.get('preferredUsername', ''),
            provider=profile.get('providerName', '').lower(),
            identifier=profile.get('identifier', ''),
            avatar=profile.get('photo', ''),
            url=profile.get('url', ''),
        )[0]

        janrain_user.save()
        post_janrain_user.send(
            JanrainSignal,
            janrain_user=janrain_user,
            profile_data=profile_data
        )

        request.user = user
        auth.login(request, user)
        post_login.send(JanrainSignal, user=user, profile_data=profile_data)

    try:
        redirect = pre_redirect.send(
            JanrainSignal,
            type='login',
            redirect=request.GET.get('next', '/')
        )[-1][1]
    except IndexError:
        redirect = '/'

    return HttpResponseRedirect(redirect)


def logout(request):
    pre_logout.send(JanrainSignal, request=request)
    auth.logout(request)

    try:
        redirect = pre_redirect.send(JanrainSignal, type='logout',
                redirect=request.GET.get('next', '/'))[-1][1]
    except IndexError:
        redirect = '/'

    return HttpResponseRedirect(redirect)
