# from urllib import request
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment
from .forms import ContactForm, PostForm, TagForm, CommentForm
from django.http import JsonResponse
from .utils.text_tools import make_title
from django.views.generic import DetailView, ListView
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from .serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, AllowAny, IsAuthenticated
from .permissions import IsOwnerOrAdmin
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import ListAPIView
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.views.decorators.csrf import csrf_exempt


def home(request):
    posts = Post.objects.order_by('-published_date')
    query = request.GET.get("q")

    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query) |
            Q(author__name__icontains=query) |
            Q(tags__name__icontains=query) 

        ).distinct()

    context = {
        'posts': posts,
        'query' : query,
                }
    return render(request, 'home.html', context)


def about(request):
    return render(request, 'about.html')

def contact(request):
    form = ContactForm()

    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            print(f"Message from {name} ({email}): {message}")
            success = True
        else:
            success = False
    else:
        success = None

    return render(request, 'contact.html', {'form': form, 'success': success})


def add_post(request):
    saved_data = request.session.get('unsaved_post_data')
    if request.method == 'POST':
        form = PostForm(request.POST)

        if 'add_tag' in request.POST:
            request.session['unsaved_post_data'] = request.POST
            next_url = request.POST.get('next', 'add_post')
            return redirect(f'/add_tag/?next={next_url}')

        if 'add_author' in request.POST:
            request.session['unsaved_post_data'] = request.POST
            next_url = request.POST.get('next', 'add_post')
            return redirect(f'/add_author/?next={next_url}')

        if form.is_valid():
            post = form.save(commit=False)
            post.title = make_title(post.title)
            post.save()
            request.session.pop('unsaved_post_data', None)
            return render(request, 'success.html', {'message': 'Post created successfully!'})
        else:
            request.session['unsaved_post_data'] = request.POST
    else:
        form = PostForm(saved_data) if saved_data else PostForm()
        request.session.pop('unsaved_post_data', None)
    return render(request, 'add_post.html', {'form': form})


#edit operation
def edit_post(request, slug):
    post = get_object_or_404(Post, slug=slug)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            form = PostForm(instance=post)
    return render(request, 'edit_post.html', {'form': form, 'post': post})

#delete operation
def delete_post(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.method == 'POST':
        post.delete()
        return redirect('home')
    
    return render(request, 'confirm_delete.html', {'post': post})

#adding tag option
def add_tag(request):
    print(request.headers)
    next_url = request.GET.get('next', 'add_post')
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save()

            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'id': tag.id, 'name': tag.name})
            
            
            return redirect(next_url)
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'errors': form.errors}, status=400)
        
        
    else:
        form = TagForm()
    return render(request, 'add_tag.html', {'form': form})

#add author manually
# def add_author(request):
#     next_url = request.GET.get('next', 'add_post')
#     if request.method == 'POST':
#         form = AuthorForm(request.POST)
#         next_url = request.GET.get('next', 'add_post')
#         if form.is_valid():
#             form.save()
#             return redirect(next_url)
#     else:
#         form = AuthorForm()        
#     return render(request, 'add_author.html', {'form': form})

#find author's post
# def posts_by_author(request, author_id):
#     author = get_object_or_404(user, id=author_id)
#     posts = Post.objects.filter(author=author).order_by('-published_date')
#     return render(request, 'posts_by_author.html', {
#         'author': author,
#         'posts': posts
#         })


#to show post in a page
class PostDetailView(DetailView):
    model = Post
    slug_field = "slug"
    slug_url_kwarg = "slug"
    template_name = "post_detail.html"


    #to filter approved for reply
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = self.object.comments.filter(
            parent__isnull=True,
            is_approved=True
        )
        return context

    # def post_detail(request, slug):
    #     post = get_object_or_404(Post, slug=slug)

    #     #handle form submit for comment
    #     if request.method == "POST":
    #         form = CommentForm(request.POST)
    #         if form.is_valid():
    #             comment = form.save(commit=False)
    #             comment.post = post
    #             comment.save()
    #             return redirect("post_detail", slug=post.slug)
    #         else:
    #             form = CommentForm()

    #         return render(request, "post_detail.html", {"post": post, "form":form})


#to show posts in homepage as list
class HomeView(ListView):
    model = Post
    template_name = "home.html"
    context_object_name = "posts"
    ordering = ["-published_date"]
    paginate_by = 3


    def get_queryset(self):
        posts = Post.objects.order_by('-published_date')
        query = self.request.GET.get("q")

        if query:
            posts = posts.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(author__name__icontains=query) |
                Q(author__place__icontains=query) |
                Q(tags__name__icontains=query) 

            ).distinct()
        
    
        return posts
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "")
        return context

#ajax searching
def ajax_search(request):
    q = request.GET.get("q", "").strip()
    results = []

    if q:
        posts = Post.objects.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        ).distinct()[:5]

        results = [
            {
                "title": p.title,
                "slug": p.slug,
            }
            for p in posts
        ]
    return JsonResponse({"results": results})


#ajax_comment
@login_required
@require_POST
def ajax_comment(request):
    
        post_id = request.POST.get("post_id")
        content = request.POST.get("content")

        if not content.strip():
            return JsonResponse({"error": "Comment cannot be empty"}, status=400)




        post = get_object_or_404(Post, id=post_id)

        comment = Comment.objects.create(
            post = post,
            user = request.user,
            content = content,
            is_approved = True, 
            parent = None
        )

        #return json to browser
        return JsonResponse({
            "username" : comment.user.username,
            "content": comment.content,
            "created_at" : comment.created_at.strftime("%Y-%m-%d %H:%M")
        })
@login_required
def add_comment(request):
    if request.method == "POST":
        post_id = request.POST.get("post_id")
        parent_id = request.POST.get("parent_id")
        content = request.POST.get("content")

        if not parent_id:
            return redirect("post_detail", slug=request.POST.get("slug", ""))

        post = get_object_or_404(Post, id=post_id)
        parent = get_object_or_404(Comment, id=parent_id)

        

        Comment.objects.create(
            post=post,
            parent=parent,
            user=request.user,
            content=content,
            is_approved=True
                    
        )
                
    return redirect("post_detail", slug=post.slug)            
                


def approve_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    comment.is_approved = True
    comment.save()
    return redirect(comment.post.get_absolute_url())

#get all objects using DRF
# @api_view(['GET'])
# def post_list_api(request):
#     posts = Post.objects.all()
#     serializer = PostSerializer(posts, many=True)
#     return Response(serializer.data)

# #create a post using DRF
# @api_view(['POST'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def post_create_api(request):
#     serializer = PostSerializer(data=request.data)
#     if serializer.is_valid():
#         serializer.save(user=request.user)
#         return Response(serializer.data, status=201)
    
#     return Response(serializer.errors, status=400)


#get only one object using DRF
# @api_view(['GET'])
# def post_detail_api(request, pk):
#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return Response({"error":"Post not found"}, status=404)
    
#     serializer = PostSerializer(post)
#     return Response(serializer.data)


# #GET AND update one object COMBINED using DRF
# @api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
# @permission_classes([IsAuthenticatedOrReadOnly])
# def post_detail_update_delete_api(request, pk):
#     print("AUTH HEADER:", request.headers.get("Authorization"))
#     print("USER:", request.user)
#     print("IS AUTH:", request.user.is_authenticated)

#     try:
#         post = Post.objects.get(pk=pk)
#     except Post.DoesNotExist:
#         return Response({"error": "Post not found"}, status=404)

#     # ✅ READ — public
#     if request.method == 'GET':
#         serializer = PostSerializer(post)
#         return Response(serializer.data)

#     # 🔐 WRITE — owner OR admin only
#     if not (request.user.is_staff or post.user == request.user):
#         return Response(
#             {"detail": "You do not have permission"},
#             status=status.HTTP_403_FORBIDDEN
#         )

#     # ✏️ UPDATE
#     if request.method in ['PUT', 'PATCH']:
#         serializer = PostSerializer(
#             post,
#             data=request.data,
#             partial=(request.method == 'PATCH')
#         )
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=400)

#     # 🗑 DELETE
#     if request.method == 'DELETE':
#         post.delete()
#         return Response({"message": "Post deleted"}, status=204)



class PostViewSet(ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdmin]
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['user']
    search_fields = ['title', 'content']
    ordering_fields = ['published_date', 'reading_time']


    def get_queryset(self):
        return Post.objects.all().distinct()


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


# class PostListAPI(ListAPIView):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = ['author', 'user']
#     search_fields = ['title', 'content']
#     ordering_fields = ['published_date', 'reading_time']



@api_view(['POST'])
@permission_classes([AllowAny])
@authentication_classes([])
def login_api(request):
    username = request.data.get('username')
    password = request.data.get('password')


    user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {'error': 'Invalid credentials'},
            status=400
            )
    token, created = Token.objects.get_or_create(user=user)

    return Response({
        "token": token.key,
        "user_id": user.id,
        "username": user.username
    })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile_api(request):
    user = request.user
    return Response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
    }) 