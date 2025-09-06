from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def special_case_2003(request):
    return HttpResponse("This is a special case for 2003!")

def year_archive(request, year):
    return HttpResponse(f"Archive for year: {year} (type: {type(year).__name__})")

def month_archive(request, year, month):
    return HttpResponse(f"Archive for year: {year} (type: {type(year).__name__}), month: {month} (type: {type(month).__name__})")

def article_detail(request, year, month, slug):
    return HttpResponse(f"Article detail - Year: {year}, Month: {month}, Slug: {slug} (type: {type(slug).__name__})")

# Views to demonstrate different path converters
def string_example(request, name):
    return HttpResponse(f"String parameter: {name} (type: {type(name).__name__})")

def uuid_example(request, id):
    return HttpResponse(f"UUID parameter: {id} (type: {type(id).__name__})")

def path_example(request, path):
    return HttpResponse(f"Path parameter: {path} (type: {type(path).__name__})")

# View with default parameters
def page(request, num=1):
    return HttpResponse(f"Blog page number: {num} (default parameter example)")

# View with extra options
def year_archive_with_extra(request, year, **kwargs):
    extra_info = ""
    if kwargs:
        extra_info = f", Extra options: {kwargs}"
    return HttpResponse(f"Archive for year: {year}{extra_info}")
