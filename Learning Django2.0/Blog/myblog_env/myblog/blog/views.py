from django.shortcuts import render_to_response,get_object_or_404 # modify from render
from django.core.paginator import Paginator
from django.conf import settings
from .models import Blog,BlogType

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)
    page_num =request.GET.get('page',1) # get the url's argc (GET requeset)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num =page_of_blogs.number # get the current page
    page_range=list(range(max(current_page_num-2,1),current_page_num))+\
               list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
    # add omit mark
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages-page_range[-1]>=2:
        page_range.append('...')
    # add first page and last page
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)

    context={}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range']=page_range
    context['blog_types']=BlogType.objects.all()
    return render_to_response('blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    context = {}
    context['blog']=get_object_or_404(Blog,pk=blog_pk)
    return render_to_response('blog/blog_detail.html',context)


def blogs_with_type(request,blog_type_pk):
    context={}
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)  # 2nd
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    paginator = Paginator(blogs_all_list,settings.EACH_PAGE_BLOGS_NUMBER)
    page_num =request.GET.get('page',1) # get the url's argc (GET requeset)
    page_of_blogs = paginator.get_page(page_num)
    current_page_num =page_of_blogs.number # get the current page
    page_range=list(range(max(current_page_num-2,1),current_page_num))+\
               list(range(current_page_num,min(current_page_num+2,paginator.num_pages)+1))
    # add omit mark
    if page_range[0]-1>=2:
        page_range.insert(0,'...')
    if paginator.num_pages-page_range[-1]>=2:
        page_range.append('...')
    # add first page and last page
    if page_range[0]!=1:
        page_range.insert(0,1)
    if page_range[-1]!=paginator.num_pages:
        page_range.append(paginator.num_pages)

    context={}
    context['blog_type']=blog_type   # 3rd
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range']=page_range
    context['blog_types']=BlogType.objects.all()
    return render_to_response('blog/blog_with_type.html',context)
# Create your views here.

