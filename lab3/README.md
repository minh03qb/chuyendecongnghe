# Django Views Lab

This lab demonstrates Django Views concepts following the official Django documentation: [Writing views](https://docs.djangoproject.com/en/5.2/topics/http/views/)

## Lab Structure

```
lab3/
├── manage.py
├── db.sqlite3
├── mysite/                 # Main project directory
│   ├── __init__.py
│   ├── settings.py        # Project settings
│   ├── urls.py           # Main URL configuration with custom error handlers
│   └── wsgi.py
└── articles/              # Django app
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── converters.py     # Custom path converters
    ├── models.py
    ├── tests.py
    ├── urls.py           # App URL patterns
    ├── views.py          # All view examples
    ├── templates/
    │   └── articles/
    │       ├── datetime.html  # Template for datetime view
    │       └── 404.html       # Custom 404 template
    └── migrations/
```

## Views Implemented

### 🕒 Simple Views
- **current_datetime**: Demonstrates both simple HttpResponse and template rendering
- **async_current_datetime**: Asynchronous view example
- **json_response**: JSON API response example
- **home**: Landing page with navigation to all examples

### ⚠️ Error Handling
- **my_view**: Conditional error responses (200 vs 404)
- **created_view**: HTTP 201 Created status example
- **detail**: Http404 exception demonstration
- **test_500_error**: Intentional server error for testing
- **test_permission_denied**: PermissionDenied exception (403)

### 🔀 Redirects
- **redirect_example**: Simple redirect to another view
- **redirect_with_args**: Redirect with URL arguments

### 🎨 Custom Error Handlers
- **custom_404_view**: Custom 404 page not found handler
- **custom_500_view**: Custom 500 server error handler
- **custom_403_view**: Custom 403 permission denied handler
- **custom_400_view**: Custom 400 bad request handler

### 📝 URL Pattern Examples (from previous URL lab)
- Path converters: `<int:year>`, `<slug:slug>`, `<str:name>`
- Custom converters: `<yyyy:year>` (four-digit year)
- Regular expressions with `re_path()`
- Default parameters and extra options

## Key Django Concepts Demonstrated

1. **HttpResponse vs HttpResponseNotFound**: Different ways to return responses
2. **Http404 Exception**: Raising 404 errors programmatically  
3. **Status Codes**: Returning different HTTP status codes (200, 201, 404, 500)
4. **Template Rendering**: Using `render()` shortcut with context
5. **JSON Responses**: Returning API-style JSON data
6. **Redirects**: Using `redirect()` for view redirection
7. **Async Views**: Asynchronous view functions
8. **Error Handlers**: Custom error pages for different HTTP errors
9. **View Arguments**: Handling URL parameters and request data

## Running the Lab

1. Start the development server:
   ```bash
   python manage.py runserver
   ```

2. Visit `http://127.0.0.1:8000/` to see the home page with links to all examples

3. Test different views:
   - `/datetime/` - Template-based datetime view
   - `/async-datetime/` - Async version
   - `/json/` - JSON API response
   - `/test-error/?foo=1` - Trigger 404 error
   - `/poll/999/` - Http404 exception
   - `/redirect/` - Redirect example

## Error Testing

Custom error handlers can be tested by:
- Visiting non-existent URLs (404)
- Adding `DEBUG = False` in settings.py to see custom error pages
- Accessing `/test-500/` for server errors
- Accessing `/test-403/` for permission denied

## Documentation Reference

This lab covers the following sections from Django documentation:
- ✅ A simple view
- ✅ Mapping URLs to views (from URL dispatcher lab)
- ✅ Returning errors
- ✅ The Http404 exception  
- ✅ Customizing error views
- ✅ Async views
- ✅ Template rendering
- ✅ JSON responses
- ✅ Redirects

## Next Steps

This lab provides a foundation for understanding Django views. Next topics could include:
- Class-based views
- View decorators
- Form handling
- Authentication and permissions
- Middleware
