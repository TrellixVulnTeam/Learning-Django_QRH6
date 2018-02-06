from django.shortcuts import render_to_response,get_object_or_404 # modify from render
from django.core.paginator import Paginator
from .models import Blog,BlogType

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list,10)
    page_num =request.GET.get('page',1) # get the url's argc (GET requeset)
    page_of_blogs = paginator.get_page(page_num)
    
    context={}
    context['blogs'] = blogs_all_list
    context['page_of_blogs'] = page_of_blogs
    context['blog_types']=BlogType.objects.all()
    return render_to_response('blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    context = {}
    context['blog']=get_object_or_404(Blog,pk=blog_pk)
    return render_to_response('blog/blog_detail.html',context)


def blogs_with_type(request,blog_type_pk):
    context={}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)  # 2nd
    context['blogs']=Blog.objects.filter(blog_type=blog_type)     # 1st
    context['blog_type']=blog_type   # 3rd
    context['blog_types']=BlogType.objects.all()
    return render_to_response('blog/blog_with_type.html',context)
# Create your views here.

