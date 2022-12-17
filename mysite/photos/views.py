from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Category, Photo
from .forms import RegisterForm, LoginForm
from django.contrib.auth import login, logout, authenticate, views as auth_views
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm

from threading import Timer
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

@login_required(login_url='login')
def gallery(request):
    category = request.GET.get('category', None)

    if category == None:
        photos = Photo.objects.all()
        page = request.GET.get('page', 1)
        paginator = Paginator(photos, 6)
        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            photos = paginator.page(1)
        except EmptyPage:
            photos = paginator.page(paginator.num_pages)

    else:
        photos = Photo.objects.filter(category__name__contains=category)
    categories = Category.objects.all()



    context = {'categories': categories, 'photos': photos }
    return render(request, 'photos/gallery.html', context)


@login_required(login_url='login')
def viewPhoto(request, pk):
    photo = get_object_or_404(Photo, id=pk)

    return render(request, 'photos/photo.html', {'photo': photo})


@login_required(login_url='login')
def addPhoto(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')
        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None
        photo = Photo.objects.create(
            category=category,
            description=data['description'],
            image=image,
        )
        return redirect('gallery')

    context = {'categories': categories}
    return render(request, 'photos/add.html', context)


def user_register(request):
    if request.method == "POST":
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            username = register_form.cleaned_data['username']
            email = register_form.cleaned_data['email']
            password = register_form.cleaned_data['password']
            first_name = register_form.cleaned_data['first_name']
            last_name = register_form.cleaned_data['last_name']
            User.objects.create_user(username=username, email=email, first_name=first_name, last_name=last_name,
                                     password=password)
            messages.success(request, 'User registration successful!')
            usr = authenticate(username=username, password=password)
            login(request, usr)
            return redirect('login')
    else:
        register_form = RegisterForm()
    return render(request, template_name='photos/register.html', context={'form': register_form})


def user_login(request):
    if request.method == "POST":
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(
                username=request.POST['username'],
                password=request.POST['password']
            )
            if user is not None:
                login(request, user)
                messages.success(request, f'you are now Logged in as {username} successful.')
                return redirect('gallery/')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        login_form = LoginForm()
    return render(request, template_name='photos/login.html', context={'form': login_form})


@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('login')


def error_404_view(request, exception):
    # we add the path to the 404.html file
    # here. The name of our HTML file is 404.html
    return render(request, template_name='photos/404NotFound.html')
