from django.urls import path, register_converter, re_path
from django.views.generic import TemplateView
from . import views, converters

# Register custom converter
register_converter(converters.FourDigitYearConverter, 'yyyy')

urlpatterns = [
    # Home page
    path("", views.home, name="home"),
    
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
    
    # ===== WRITING VIEWS EXAMPLES =====
    # Simple view example
    path("datetime/", views.current_datetime, name="current-datetime"),
    path("json/", views.json_response, name="json-response"),
    path("redirect/", views.redirect_example, name="redirect-example"),
    path("redirect/<int:year>/", views.redirect_with_args, name="redirect-with-args"),
    
    # Error handling examples
    path("test-error/", views.my_view, name="test-error"),  # Use ?foo=1 to get 404
    path("created/", views.created_view, name="created-view"),
    path("poll/<int:poll_id>/", views.detail, name="poll-detail"),
    path("test-500/", views.test_500_error, name="test-500"),  # Test 500 error handler
    path("test-403/", views.test_permission_denied, name="test-403"),  # Test 403 error handler
    
    # Async view example
    path("async-datetime/", views.async_current_datetime, name="async-datetime"),
    
    # ===== CLASS-BASED VIEWS EXAMPLES =====
    # Direct usage in URLconf
    path("cbv/template-direct/", TemplateView.as_view(template_name="articles/about.html"), name="template-direct"),
    
    # Subclassed views
    path("cbv/about/", views.AboutView.as_view(), name="about-view"),
    path("cbv/redirect/", views.SimpleRedirectView.as_view(), name="simple-redirect"),
    path("cbv/redirect/<int:year>/", views.DynamicRedirectView.as_view(), name="dynamic-redirect"),
    path("cbv/basic/", views.BasicView.as_view(), name="basic-view"),
    path("cbv/async/", views.AsyncClassView.as_view(), name="async-class-view"),
    path("cbv/api/", views.APIView.as_view(), name="api-view"),
]
