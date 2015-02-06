from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import datetime
from itertools import chain

from .forms import \
    SignupForm, \
    SigninForm, \
    EditPostForm, \
    SearchForm, \
    UploadPhotosForm, \
    PublishPostForm

from listings.models import Profile, Post, Tag, Picture

import pdb


@login_required()
def favorites_add(request, post_id=0):
    return HttpResponseRedirect('/listings/')


def view_post(request, post_id=0):
    form = SearchForm({'search_string': ''})
    post = None
    if int(post_id) > 0:
        post = Post.objects.get(id=int(post_id))

    post.tags_text = []
    for tag in post.tags.all():
        post.tags_text.append(tag.description)

    context = {'post': post,
               'form': form,
               'page_title': "Rosetti Listings"}
    return render(request, 'listings/post.html', context)


def view_category(request, category=""):
    form = SearchForm({'search_string': ''})
    posts = Post.objects.filter(category=category)

    context = {'posts': posts,
               'form': form,
               'request_method': request.method,
               'page_title': "Rosetti Listings"}

    return render(request, 'listings/index.html', context)


def view_tag(request, tag=""):
    tag = tag.replace('-', ' ')
    posts = []
    form = SearchForm({'search_string': ''})
    tags = Tag.objects.filter(description=tag)

    if len(tags) == 1:
        posts = tags[0].posts.all()

    context = {'tag': tag,
               'form': form,
               'posts': posts,
               'page_title': 'Rosetti Listings'}
    return render(request, 'listings/tag.html', context)


def search(request, search_string=""):
    posts = []
    search_string = search_string.replace('-', ' ')
    form = SearchForm({'search_string': search_string})

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            search_string = form.cleaned_data['search_string']
            category = form.cleaned_data['category']

    tag = Tag.objects.filter(description=search_string)
    posts_by_tag = tag[0].posts.filter(category=category) if tag else []
    posts_by_title = Post.objects.filter(title__contains=search_string)
    posts = sorted(set(chain(posts_by_tag, posts_by_title)), key=lambda x: x.title)

    context = {'posts': posts,
               'form': form,
               'search_string': search_string,
               'page_title': "Rosetti Listings"}

    return render(request, 'listings/search.html', context)


@login_required()
def my_posts(request):
    me = request.user
    posts = Post.objects.filter(user=me).order_by('create_date')

    for post in posts:
        if post.expiry_date < datetime.datetime.now():
            post.is_active = False
        else:
            post.is_active = True

    active_posts = Post.objects.filter(expiry_date__gt=datetime.datetime.today(), user=me)
    context = {'posts': posts,
               'num_of_posts': active_posts.count(),
               'today': datetime.datetime.today(),
               'me': me,
               'page_title': "View Post"}

    return render(request, 'listings/admin/my_posts.html', context)


@login_required()
def delete_post(request, post_id=0):
    if int(post_id) > 0:
        post = Post.objects.get(id=int(post_id))
        post.delete()
    return HttpResponseRedirect('/listings/myposts/view/')


@login_required()
def edit_post(request, post_id=0):
    me = request.user
    errors = []
    post = Post()

    if request.method == 'POST':
        form = EditPostForm(request.POST)

        if form.is_valid():
            data = form.cleaned_data
            post_id = data['id']
            title = data['title']
            content = data['content']
            price = data['price']
            location = data['location']
            category = data['category']
            # create_date = datetime.date(2014, 11, 5)
            create_date = datetime.datetime.today()
            tag_descriptions = data['tags'].split(',')

            if int(post_id) > 0:
                post = Post.objects.get(id=int(post_id))

            # for tag in post.tags.all():
            #    tag.delete()

            post.user = me
            post.title = title
            post.content = content
            post.price = price
            post.category = category
            post.location = location
            if post_id == 0:
                post.create_date = create_date
                post.expiry_date = create_date + datetime.timedelta(days=7)
            post.save()

            for tag_description in tag_descriptions:
                description = tag_description.lower().strip()
                tags = Tag.objects.filter(description=description)

                if description == '':
                    tags.delete()
                    continue

                # if multiple tags with the same description exist delete all but the first
                for i in range(1, len(tags)):
                    tags[i].delete()

                tag = Tag(description=description.lower().strip())
                if len(tags) > 0:
                    tag = tags[0]

                tag.save()
                tag.posts.add(post)

            return HttpResponseRedirect('/listings/myposts/upload/'+str(post.id)+'/')
        else:
            return HttpResponseRedirect('/listings/myposts/view/')
    else:

        data = {}
        post_tags = []
        if int(post_id) > 0:
            post = Post.objects.get(id=int(post_id))
            data['title'] = post.title
            data['content'] = post.content
            data['tags'] = ', '.join(str(item) for item in post.tags.all())
            data['location'] = post.location
            data['price'] = post.price
            data['category'] = post.category
        else:
            post.id = 0

        form = EditPostForm(data)
        context = {'form': form,
                   'post': post,
                   'num_of_posts': Post.objects.filter(user=me).count(),
                   'post_tags': post_tags,
                   'errors': errors,
                   'me': me,
                   'page_title': 'Add Post'}
        return render(request, 'listings/admin/edit_post.html', context)


@login_required()
def view_my_post(request, post_id=0):
    me = request.user
    post_id = int(post_id)
    post = Post.objects.get(id=post_id)
    post.tags_text = []
    for tag in post.tags.all():
        post.tags_text.append(tag.description)

    context = {'post': post,
               'num_of_posts': Post.objects.filter(user=me).count()}
    return render(request, 'listings/admin/view_my_post.html', context)


@login_required()
def publish_post(request, post_id=0):
    me = request.user
    if request.method == 'POST':
        form = PublishPostForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            post_id = data['id']
            post = Post.objects.get(id=post_id)
            post.create_date = data['create_date']
            post.expiry_date = data['expiry_date']
            post.save()
            return HttpResponseRedirect('/listings/myposts/view/')
    else:
        post_id = int(post_id)
        post = Post.objects.get(id=post_id)
        post.tags_text = []
        for tag in post.tags.all():
            post.tags_text.append(tag.description)

        form = PublishPostForm()
        context = {
            'post': post,
            'form': form,
            'num_of_posts': Post.objects.filter(user=me).count()}
        return render(request, 'listings/admin/publish_post.html', context)


@login_required()
def upload_photos(request, post_id=0):
    me = request.user
    post_id = int(post_id)
    post = Post.objects.get(id=post_id) if post_id > 0 else []
    pictures = post.pictures if post else []

    if request.method == 'POST':
        position = len(pictures.all())
        for file in request.FILES.getlist('pictures'):
            print("###### Adding photo #"+repr(position))
            photo = Picture(post=post,
                            file=file,
                            title="Untitled",
                            upload_date=datetime.datetime.now(),
                            position=position)
            pictures.add(photo)
            position += 1

        for id_str in request.POST.getlist('old_pic_delete'):
            picture_id = int(id_str)
            pic_to_delete = Picture.objects.get(id=picture_id)
            pic_to_delete.delete()

    form = UploadPhotosForm()
    context = {'post_id': post_id,
               'pictures': pictures.all(),
               'form': form,
               'page_title': 'Upload Photos',
               'num_of_posts': Post.objects.filter(user=me).count()}
    return render(request, 'listings/admin/upload_photos.html', context)


def home(request):
    search_string = ''
    form = SearchForm({'search_string': search_string})
    context = {'form': form,
               'page_title': 'Rosetti Listings'}
    return render(request, 'listings/index.html', context)


@login_required()
def dashboard(request):
    me = request.user
    context = {'me': me,
               'num_of_posts': Post.objects.filter(user=me).count()}
    return render(request, 'listings/admin/index.html', context)


def signup(request):
    errors = []
    if request.method == 'POST':
        form = SignupForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data
            display_name = data['display_name']
            email = data['email']
            password = data['password']
            username = email.split("@")

            if len(username) != 2:
                errors.append('Invalid email address.')
            else:
                username = username[0]
                if len(User.objects.filter(email=email)) > 0:
                    errors.append('Email address already in use.')
                if len(User.objects.filter(username=username)) > 0:
                    errors.append('Username already taken.')

            if not errors:
                me = User.objects.create_user(username, email, password)
                me.first_name = display_name
                me.save()
                Profile(user=me).save()
                return HttpResponseRedirect('/listings/signin/')
        else:
            errors.append('Invalid form data submitted.')
    else:
        form = SignupForm(initial={'username': '', 'email': '', 'password': ''})
        user = request.user
        if user.is_authenticated():
            return redirect('/listings/')

    context = {'form': form,
               'errors': errors,
               'page_title': "Sign Up"}
    return render(request, 'listings/signup.html', context)


def signin(request):
    errors = []
    me = request.user
    if me.is_authenticated():
        return HttpResponseRedirect('/listings/')
    if request.method == 'POST':
        form = SigninForm(data=request.POST)
        if form.is_valid():
            data = form.cleaned_data

            email = data['email']
            user_by_email = User.objects.filter(email=email)

            if user_by_email.count() == 0:
                errors.append('Email address not registered.')
            else:
                username = user_by_email[0].username
                password = request.POST['password']
                me = authenticate(username=username, password=password)
                if me:
                    if me.is_active:
                        login(request, me)
                        me.profile.last_online = datetime.datetime.today()
                        me.save()
                        return HttpResponseRedirect('/listings/dashboard/')
                    else:
                        errors.append('Your account is disabled.')
                else:
                    errors.append('Invalid login details.')
        else:
            errors.append('Invalid form data submitted.')
    else:
        logged_in = False
        form = SigninForm()
        context = {'form': form,
                   'logged_in': logged_in,
                   'page_title': "Sign In"}
        return render(request, 'listings/signin.html', context)


def signout(request):
    logout(request)
    return HttpResponseRedirect('/listings/')