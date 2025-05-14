from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import RegisterForm,PostForm





from django.contrib.auth.decorators import login_required

from .models import Post, Like, Comment



def register_view(request):
    form=RegisterForm()
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
   
    return render(request, 'core/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
    return render(request, 'core/login.html')


@login_required
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    return render(request, 'core/home.html', {'posts': posts})


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'core/create_post.html', {'form': form})





@login_required
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    like,created=Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('home')

@login_required
def comment_post(request, post_id):
    post=get_object_or_404(Post,id=post_id)
    if request.method == 'POST':
        
        content=request.POST.get('content')  

        
        Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )
    return redirect('home')



