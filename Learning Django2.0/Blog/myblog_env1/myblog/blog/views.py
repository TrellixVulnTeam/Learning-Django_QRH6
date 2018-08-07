from django.shortcuts import render_to_response,get_object_or_404 # modify from render
from django.core.paginator import Paginator
from django.conf import settings
from django.db.models import Count
from .models import Blog,BlogType

def get_blog_list_common_data(request,blogs_all_list):
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
    # Count by date  
    blog_dates  = Blog.objects.dates('create_time','month',order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(create_time__year = blog_date.year,create_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count

    
    context={}
    context['blogs'] = page_of_blogs.object_list
    context['page_of_blogs'] = page_of_blogs
    context['page_range']=page_range
    context['blog_types']=BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates']=blog_dates_dict
    return context

def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context=get_blog_list_common_data(request,blogs_all_list)
    return render_to_response('blog/blog_list.html',context)

def blog_detail(request,blog_pk):
    context = {}
    blog=get_object_or_404(Blog,pk=blog_pk)
    if not request.COOKIES.get('blog_%s_readed' %blog_pk):
        blog.readed_num+=1
        blog.save()
    context['previous_blog'] =Blog.objects.filter(create_time__gt=blog.create_time).last()
    context['next_blog'] = Blog.objects.filter(create_time__lt=blog.create_time).first()
    context['blog']=blog
    response=render_to_response('blog/blog_detail.html',context)
    response.set_cookie('blog_%s_readed' %blog_pk,'true')
    return response


def blogs_with_type(request,blog_type_pk):
    blog_type = get_object_or_404(BlogType,pk=blog_type_pk)  # 2nd
    blogs_all_list = Blog.objects.filter(blog_type=blog_type)
    context=get_blog_list_common_data(request,blogs_all_list)
    context['blog_type']=blog_type   # 3rd
    return render_to_response('blog/blog_with_type.html',context)
# Create your views here.

def blogs_with_date(request,year,month):
    blogs_all_list = Blog.objects.filter(create_time__year=year,create_time__month=month)
    context=get_blog_list_common_data(request,blogs_all_list)
    context['blogs_with_date']='%s/%s'%(month,year)
    return render_to_response('blog/blog_with_date.html',context)
