# -*- coding: utf-8 -*-
from django.http import Http404
from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from django.core.context_processors import csrf

from couchbase.bucket import Bucket
from couchbase.exceptions import CouchbaseError
from django_cbtools.sync_gateway import SyncGateway



def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")

def register(request):
    args = {}
    args.update(csrf(request))
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'], password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)
            #Adding user to main bucket
            try:
                c = Bucket('couchbase://localhost/nihongo')
                username = newuser_form.cleaned_data['username']
                password = newuser_form.cleaned_data['password2']
                c_username = 'user_' + username
                new_user = {'username' : c_username, 'password' : password, 'login' : c_username, 'doc_type' : 'user_doc'}
                doc_channels = [c_username]
                new_user['doc_channels'] = doc_channels
                c.upsert(c_username, new_user)
            except CouchbaseError as ce:
                raise Http404("Couchbase server error")
            #Adding user to sync gateway database
            SyncGateway.put_user(c_username, 'some@email.com', password, [c_username])
            return redirect('/')
        else:
            args['form'] = newuser_form
    return render_to_response('register.html', args)
