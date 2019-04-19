from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404,  HttpResponseRedirect
from django.contrib import messages
import bcrypt
from models import User

def index(request):
    return render(request, 'register/index.html')

def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors):
        for tag, error in errors.iteritems():
            messages.error(request, error, extra_tags=tag)
        return redirect('/')

    hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=hashed_password, email=request.POST['email'])
    user.save()
    request.session['id'] = user.id
    return redirect('/success')

def login(request):
    if (User.objects.filter(email=request.POST['email']).exists()):
        user = User.objects.filter(email=request.POST['email'])[0]
        if (bcrypt.checkpw(request.POST['pass'].encode(), user.password.encode())):
            request.session['id'] = user.id
            return redirect('/success')
    return redirect('/')

def success(request):
    user = User.objects.get(id=request.session['id'])
    context = {
        "user": user
    }
    return render(request, 'register/success.html', context)
def test_redirect(request):
    return HttpResponseRedirect("http://10.0.0.235:8080/guacamole/#/client/V2luZG93cyAxMABjAGRlZmF1bHQ=?username=USERNAME&password=PASSWORD")
