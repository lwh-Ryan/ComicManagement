from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required
from django.contrib.auth.models import User
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from management.models import MyUser, Comic, Img
from django.core.urlresolvers import reverse
from management.utils import permission_check


def index(request):
    user = request.user if request.user.is_authenticated() else None
    content = {
        'active_menu': 'homepage',
        'user': user,
    }
    return render(request, 'management/index.html', content)


def signup(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        password = request.POST.get('password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if password == '' or repeat_password == '':
            state = 'empty'
        elif password != repeat_password:
            state = 'repeat_error'
        else:
            username = request.POST.get('username', '')
            if User.objects.filter(username=username):
                state = 'user_exist'
            else:
                new_user = User.objects.create_user(username=username, password=password,
                                                    email=request.POST.get('email', ''))
                new_user.save()
                new_my_user = MyUser(user=new_user, nickname=request.POST.get('nickname', ''))
                new_my_user.save()
                state = 'success'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None,
    }
    return render(request, 'management/signup.html', content)


def login(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('homepage'))
    state = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('homepage'))
        else:
            state = 'not_exist_or_password_error'
    content = {
        'active_menu': 'homepage',
        'state': state,
        'user': None
    }
    return render(request, 'management/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('homepage'))


@login_required
def set_password(request):
    user = request.user
    state = None
    if request.method == 'POST':
        old_password = request.POST.get('old_password', '')
        new_password = request.POST.get('new_password', '')
        repeat_password = request.POST.get('repeat_password', '')
        if user.check_password(old_password):
            if not new_password:
                state = 'empty'
            elif new_password != repeat_password:
                state = 'repeat_error'
            else:
                user.set_password(new_password)
                user.save()
                state = 'success'
        else:
            state = 'password_error'
    content = {
        'user': user,
        'active_menu': 'homepage',
        'state': state,
    }
    return render(request, 'management/set_password.html', content)


@user_passes_test(permission_check)
def add_comic(request):
    user = request.user
    state = None
    if request.method == 'POST':
        new_comic = Comic(
                name=request.POST.get('name', ''),
                author=request.POST.get('author', ''),
                category=request.POST.get('category', ''),
                type=request.POST.get('type', 0),
                publish_date=request.POST.get('publish_date', '')
        )
        new_comic.save()
        state = 'success'
    content = {
        'user': user,
        'active_menu': 'add_comic',
        'state': state,
    }
    return render(request, 'management/add_comic.html', content)


def view_comic_list(request):
    user = request.user if request.user.is_authenticated() else None
    category_list = Comic.objects.values_list('category', flat=True).distinct()
    query_category = request.GET.get('category', 'all')
    if (not query_category) or Comic.objects.filter(category=query_category).count() is 0:
        query_category = 'all'
        comic_list = Comic.objects.all()
    else:
        comic_list = Comic.objects.filter(category=query_category)

    if request.method == 'POST':
        keyword = request.POST.get('keyword', '')
        comic_list = Comic.objects.filter(name__contains=keyword)
        query_category = 'all'

    paginator = Paginator(comic_list, 10)
    page = request.GET.get('page')
    try:
        comic_list = paginator.page(page)
    except PageNotAnInteger:
        comic_list = paginator.page(1)
    except EmptyPage:
        comic_list = paginator.page(paginator.num_pages)
    content = {
        'user': user,
        'active_menu': 'view_comic',
        'category_list': category_list,
        'query_category': query_category,
        'comic_list': comic_list,
    }
    return render(request, 'management/view_comic_list.html', content)


def detail(request):
    user = request.user if request.user.is_authenticated() else None
    comic_id = request.GET.get('id', '')
    if comic_id == '':
        return HttpResponseRedirect(reverse('view_comic_list'))
    try:
        comic = Comic.objects.get(pk=comic_id)
    except Comic.DoesNotExist:
        return HttpResponseRedirect(reverse('view_comic_list'))
    content = {
        'user': user,
        'active_menu': 'view_comic',
        'comic': comic,
    }
    return render(request, 'management/detail.html', content)


@user_passes_test(permission_check)
def add_img(request):
    user = request.user
    state = None
    if request.method == 'POST':
        try:
            new_img = Img(
                    name=request.POST.get('name', ''),
                    description=request.POST.get('description', ''),
                    img=request.FILES.get('img', ''),
                    comic=Comic.objects.get(pk=request.POST.get('comic', ''))
            )
            new_img.save()
        except Comic.DoesNotExist as e:
            state = 'error'
            print(e)
        else:
            state = 'success'
    content = {
        'user': user,
        'state': state,
        'comic_list': Comic.objects.all(),
        'active_menu': 'add_img',
    }
    return render(request, 'management/add_img.html', content)
