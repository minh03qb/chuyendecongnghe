from django.urls import path, register_converter, re_path
from . import views, converters

# Register custom converter
register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    # Basic examples from the documentation (with names for URL reversal)
    path("articles/2003/", views.special_case_2003, name="special-2003"),
    path("articles/<int:year>/", views.year_archive, name="year-archive"),
    path("articles/<int:year>/<int:month>/", views.month_archive, name="month-archive"),
    path("articles/<int:year>/<int:month>/<slug:slug>/", views.article_detail, name="article-detail"),
    
    # Custom converter example
    path("archive/<yyyy:year>/", views.year_archive, name="custom-year-archive"),
    
    # Regular expressions examples
    re_path(r'^regex-articles/(?P<year>[0-9]{4})/$', views.year_archive, name="regex-year-archive"),
    re_path(r'^regex-articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/$', views.month_archive, name="regex-month-archive"),
    re_path(r'^regex-articles/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<slug>[\w-]+)/$', views.article_detail, name="regex-article-detail"),
    
    # Default parameters example
    path("blog/", views.page, name="blog-index"),  # Will use num=1 (default)
    path("blog/page<int:num>/", views.page, name="blog-page"),  # Will use the provided num
    
    # Extra options example
    path("extra/<int:year>/", views.year_archive_with_extra, {"foo": "bar", "category": "special"}, name="extra-year"),
    
    # Path converter examples
    path("string/<str:name>/", views.string_example, name="string-example"),  # str is default, can be omitted
    path("string/<name>/", views.string_example, name="string-example-2"),  # Same as above, str is implicit
    path("uuid/<uuid:id>/", views.uuid_example, name="uuid-example"),
    path("path/<path:path>/", views.path_example, name="path-example"),
]
