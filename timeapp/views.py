from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from django.contrib.auth.models import User
from .models import Post
from .filters import PostFilter

# REST FRAMEWORK
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializer import PostSerializer
from rest_framework import status
# END OF REST IMPORTS

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'timeapp/home.html', context)

# List Views for Post

class PostListView(ListView):
    model = Post
    template_name = 'timeapp/home.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    ordering = ['-date_posted']


# Detail Views for Post
class PostDetailView(DetailView):
    model = Post

# Create Views for Post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'content', 'post_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
        data = {'success': 'You have been successfully Posted to Time APP'}
        return JsonResponse(data)

# Update Class Views for Post

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'content', 'post_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


# Delete Class Views for Post
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

def about(request):
    return render(request, 'timeapp/about.html', {'title': 'About'})


# Searching Models


def postsearch(request):
    post_list = Post.objects.all()
    post_filter = PostFilter(request.GET, queryset=post_list)
    return render(request, 'timeapp/post-search.html', {'filter': post_filter})

# REST API VIEW
class PostList(APIView):
    def get(self, request, format=None):
        all_merch = Post.objects.all()
        serializers = PostSerializer(all_merch, many=True)
        return Response(serializers.data)
    def post(self, request, format=None):
        serializers = PostSerializer(data=request.data)
        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


        