from django.shortcuts import render, get_object_or_404, redirect ,reverse
from django.core.paginator import Paginator , PageNotAnInteger, EmptyPage
from django.db.models import Count , Q

from .forms import CommentForm, PostForm

from .models import Post ,Author ,PostView
from marketing.models import Signup


def get_author(user):
	qs = Author.objects.filter(user=user)
	if qs.exists():
		return qs[0]
	return None

def search(requset):
	queryset  = Post.objects.all()
	query = requset.GET.get('q')
	if query:
		queryset = queryset.filter(
		Q(title__icontains=query) | 
		Q(overview__icontains=query)).distinct()
	context = {
	'queryset': queryset,
	}
	return render(requset, 'search_results.html', context)


def get_category_count():
	queryset = Post\
	.objects\
	.values('categories__title')\
	.annotate(Count('categories__title'))
	return queryset

def index(requset):
	featured = Post.objects.filter(featured=True)
	latest = Post.objects.order_by('-timestamp')[:3]

	if requset.method =='POST':
		email = requset.POST['email']
		new_signup = Signup()
		new_signup.email = email
		new_signup.save()

	context = {
	'objects_list': featured,
	'latest': latest,
	} 

	return render(requset, 'index.html', context)


def blog(requset):
	category_count = get_category_count()
	most_recent = Post.objects.order_by('-timestamp')[:3]
	post_list = Post.objects.all()
	paginator = Paginator(post_list, 4)
	page_request_var = 'page'
	page = requset.GET.get(page_request_var)
	try:
		paginated_queryset = paginator.page(page)
	except PageNotAnInteger:
		paginated_queryset = paginator.page(1)

	except EmptyPage:
		paginated_queryset = paginator.page(paginator.num_page)

	context ={
	'queryset': paginated_queryset,
	'page_request_var': page_request_var,
	'most_recent': most_recent,
	'category_count': category_count
	}
	return render(requset, 'blog.html', context)


def post(requset, id):
	category_count = get_category_count()
	most_recent = Post.objects.order_by('-timestamp')[:3]
	post = get_object_or_404(Post, pk=id)

	if requset.user.is_authenticated:
		PostView.objects.get_or_create(user=requset.user, post=post)

	form = CommentForm(requset.POST or None)
	if requset.method == 'POST':
		if form.is_valid():
			form.instance.user = requset.user
			form.instance.post = post
			form.save()

	context = {
	'form': form,
	'post': post,
	'most_recent': most_recent,
	'category_count': category_count
	}
	return render(requset, 'post.html', context)

	

def post_create(requset):
	title = 'Create'
	form = PostForm(requset.POST or None, requset.FILES or None)
	author = get_author(requset.user)
	if requset.method == 'POST':
		if form.is_valid():
			# form.instance.author = author
			form.save()
			return redirect(reverse('post-detail', kwargs={
				'id': form.instance.id
				}))
	context = {
	'form': form,
	'title': title
	}
	return render(requset, 'post_create.html', context)

def post_update(requset, id):
	title = 'Update'
	post = get_object_or_404(Post, id=id)
	form = PostForm(
		requset.POST or None,
	 	requset.FILES or None,
	 	instance=post)
	author = get_author(requset.user)
	if requset.method == 'POST':
		if form.is_valid():
			# form.instance.author = author
			form.save()
			return redirect(reverse('post-detail', kwargs={
				'id': form.instance.id
				}))
	context = {
	'form': form,
	'title': title
	}
	return render(requset, 'post_update.html', context)

def post_delete(requset, id):
	post =  get_object_or_404(Post, id=id)
	post.delete()
	return redirect('post-list')