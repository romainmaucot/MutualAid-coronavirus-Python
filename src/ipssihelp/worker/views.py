from django.contrib.auth import get_user, decorators, authenticate, login
from django.contrib.auth import logout as django_logout
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.decorators.csrf import csrf_protect, requires_csrf_token
from django.contrib.auth.decorators import login_required
from .forms import SignupForm, SigninForm, UpdateForm
from .models import Ad
from .models import User
from django.db.models import Count



def home(request):
    template = loader.get_template('home.html')
    get_top_user = User.objects.annotate(num_ads=Count('ad')).order_by('-num_ads')[:5]
    get_last_supply = Ad.objects.filter(type='supply', status__exact='online').order_by('-created')[:5]
    get_last_demand = Ad.objects.filter(type='demand', status__exact='online').order_by('-created')[:5]
    context = {
        'top_users': get_top_user,
        'last_supplies': get_last_supply,
        'last_demands': get_last_demand
    }
    return HttpResponse(template.render(context, request))


@csrf_protect
@requires_csrf_token
def signup(request):
    template = loader.get_template('accounts/signup.html')

    user = get_user(request)
    if not user.is_authenticated:
        if request.method == 'POST':
            form = SignupForm(request.POST)
            context = {
                'form': form
            }
            if form.is_valid():
                form.save()
                email = form.cleaned_data['email']
                raw_password = form.cleaned_data['password1']
                user = authenticate(email=email, password=raw_password)
                login(request, user)
                return redirect('worker:home')
        else:
            form = SignupForm()
            context = {
                'form': form
            }

        return HttpResponse(template.render(context, request))

    return redirect('worker:home')

@csrf_protect
@requires_csrf_token
def update_profil(request, slug):
    template = loader.get_template('accounts/update_profil.html')
    user = get_user(request)
    if user.slug == slug:
        if request.method == 'POST':
            data = {
                'email': user.email
            }
            form = UpdateForm(request.POST, initial=data)
            form.has_changed()
            context = {
                'form': form
            }
            if form.is_valid():
                email = form.cleaned_data['email']
                raw_password = form.cleaned_data['password1']
                context = {
                    'form': form
                }

                return HttpResponse(template.render(context, request))
        else:
            form = UpdateForm()
            context = {
                'form': form
            }

        return HttpResponse(template.render(context, request))
    else:
        return redirect('worker:home')

@csrf_protect
@requires_csrf_token
def signin(request):
    template = loader.get_template('accounts/signin.html')

    user = get_user(request)
    if not user.is_authenticated:
        if request.method == 'POST':
            form = SigninForm(request.POST)
            context = {
                'form': form
            }
            if form.is_valid():
                email = form.cleaned_data['email']
                raw_password = form.cleaned_data['password']
                user = authenticate(email=email, password=raw_password)
                if user:
                    login(request, user)
                    return redirect('worker:home')
                else:
                    form = SigninForm()
                    context = {
                        'form': form,
                        'message': 'Identifiants non valides! Veuillez recommencez'
                    }
        else:
            form = SigninForm()
            context = {
                'form': form
            }

        return HttpResponse(template.render(context, request))

    return redirect('worker:home')


def supply(request):
    template = loader.get_template('ad/supply.html')
    context = {
        'supply_ads': Ad.objects.filter(type='supply', status__exact='online')
    }
    return HttpResponse(template.render(context, request))


def demand(request):
    template = loader.get_template('ad/demand.html')
    context = {
        'demand_ads': Ad.objects.filter(type='demand', status__exact='online')
    }
    return HttpResponse(template.render(context, request))


def detail(request, slug):
    template = loader.get_template('ad/detail.html')
    try:
        get_ad = Ad.objects.get(slug=slug)
        context = {
            'ad': get_ad
        }
    except ObjectDoesNotExist:
        context = {
            'ad': None
        }

    return HttpResponse(template.render(context, request))

def profil(request, slug):
    template = loader.get_template('accounts/profil.html')
    try:
        get_user = User.objects.get(slug=slug)
        demand_ads = Ad.objects.filter(user_id=get_user.id, type='demand', status__exact='online')
        supply_ads = Ad.objects.filter(user_id=get_user.id, type='supply', status__exact='online')
        context = {
            'profil': get_user,
            'demand_ads': demand_ads,
            'supply_ads': supply_ads
        }
    except ObjectDoesNotExist:
        context = {
            'profil': None,
            'demand_ads': None,
            'supply_ads': None
        }


    return HttpResponse(template.render(context, request))

@login_required
def logout(request):
        django_logout(request)
        return redirect('worker:home')


@decorators.login_required(login_url='/your_login_page')
def protected_page_view(request):
    template = loader.get_template('your_template.html')
    # something
    return HttpResponse(template.render(None, request))
