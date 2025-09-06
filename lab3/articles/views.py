from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404, HttpResponseRedirect
from django.views.generic import TemplateView, RedirectView, View
from django.urls import reverse_lazy
from django.core.mail import send_mail
import datetime
import json

# Import forms
from .forms import NameForm, ContactForm, SearchForm, AdvancedForm, FeedbackForm

# Create your views here.

# ===== SIMPLE VIEW EXAMPLE =====
def home(request):
    """Home page with links to all examples"""
    html = '''
    <html lang="en">
    <head>
        <title>Django Views Lab</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            h1 { color: #0066cc; }
            h2 { color: #0088cc; }
            ul { list-style-type: none; }
            li { margin: 10px 0; }
            a { text-decoration: none; color: #0066cc; }
            a:hover { text-decoration: underline; }
        </style>
    </head>
    <body>
        <h1>Django Views Lab Examples</h1>
        <p>This lab demonstrates various Django view concepts from the official documentation.</p>
        
        <h2>🕒 Simple Views</h2>
        <ul>
            <li><a href="/datetime/">Current DateTime View (Template-based)</a></li>
            <li><a href="/async-datetime/">Async DateTime View</a></li>
            <li><a href="/json/">JSON Response Example</a></li>
        </ul>
        
        <h2>🔀 Redirects</h2>
        <ul>
            <li><a href="/redirect/">Redirect Example</a></li>
            <li><a href="/redirect/2024/">Redirect with Arguments</a></li>
        </ul>
        
        <h2>🏛️ Class-based Views</h2>
        <ul>
            <li><a href="/cbv/about/">TemplateView Example</a></li>
            <li><a href="/cbv/redirect/">RedirectView Example</a></li>
            <li><a href="/cbv/redirect/2025/">Dynamic RedirectView</a></li>
            <li><a href="/cbv/basic/">Basic View (GET/POST)</a></li>
            <li><a href="/cbv/async/">Async Class View</a></li>
            <li><a href="/cbv/api/">API View (supports GET/POST/PUT/DELETE)</a></li>
        </ul>
        
        <h2>⚠️ Error Handling</h2>
        <ul>
            <li><a href="/test-error/">Test Error View (normal response)</a></li>
            <li><a href="/test-error/?foo=1">Test Error View (404 error)</a></li>
            <li><a href="/created/">Created Status (201)</a></li>
            <li><a href="/poll/1/">Poll Detail (valid ID)</a></li>
            <li><a href="/poll/999/">Poll Detail (404 error)</a></li>
        </ul>
        
        <h2>📝 URL Patterns Examples</h2>
        <ul>
            <li><a href="/articles/2005/">Articles 2005</a></li>
            <li><a href="/articles/2005/03/">Articles 2005/03</a></li>
            <li><a href="/articles/2003/03/building-django/">Article Detail</a></li>
            <li><a href="/blog/">Blog (default page)</a></li>
            <li><a href="/blog/page5/">Blog Page 5</a></li>
        </ul>
    </body>
    </html>
    '''
    return HttpResponse(html)

def current_datetime(request):
    """A simple view that returns the current date and time as HTML"""
    now = datetime.datetime.now()
    # Original simple version
    # html = '<html lang="en"><body>It is now %s.</body></html>' % now
    # return HttpResponse(html)
    
    # Template version with context
    context = {
        'current_time': now,
        'view_type': 'Template-based view'
    }
    return render(request, 'articles/datetime.html', context)

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

# ===== ERROR HANDLING EXAMPLES =====
def my_view(request):
    """Example view showing different HTTP response codes"""
    foo = request.GET.get('foo', False)
    
    if foo:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    else:
        return HttpResponse("<h1>Page was found</h1>")

def created_view(request):
    """Example view returning HTTP 201 Created status"""
    return HttpResponse("<h1>Resource created successfully!</h1>", status=201)

def detail(request, poll_id):
    """Example view demonstrating Http404 exception"""
    # Simulating a model lookup
    valid_ids = [1, 2, 3, 4, 5]
    
    try:
        if int(poll_id) not in valid_ids:
            raise Http404(f"Poll with ID {poll_id} does not exist")
        return HttpResponse(f"<h1>Poll details for ID: {poll_id}</h1>")
    except ValueError:
        raise Http404("Invalid poll ID format")

def test_500_error(request):
    """View that intentionally raises an exception to test 500 error handler"""
    raise Exception("This is a test exception to trigger 500 error handler")

def test_permission_denied(request):
    """View that raises PermissionDenied to test 403 error handler"""
    from django.core.exceptions import PermissionDenied
    raise PermissionDenied("You don't have permission to access this resource")

# ===== CUSTOM ERROR HANDLERS =====
def custom_404_view(request, exception):
    """Custom 404 error handler"""
    return HttpResponseNotFound(
        '<html><body><h1>Custom 404 - Page Not Found</h1>'
        '<p>Sorry, the page you are looking for does not exist.</p>'
        '<a href="/">Go back to home</a></body></html>'
    )

def custom_500_view(request):
    """Custom 500 error handler"""
    return HttpResponse(
        '<html><body><h1>Custom 500 - Server Error</h1>'
        '<p>Something went wrong on our end.</p>'
        '<a href="/">Go back to home</a></body></html>',
        status=500
    )

def custom_403_view(request, exception):
    """Custom 403 error handler"""
    return HttpResponse(
        '<html><body><h1>Custom 403 - Permission Denied</h1>'
        '<p>You do not have permission to access this resource.</p>'
        '<a href="/">Go back to home</a></body></html>',
        status=403
    )

def custom_400_view(request, exception):
    """Custom 400 error handler"""
    return HttpResponse(
        '<html><body><h1>Custom 400 - Bad Request</h1>'
        '<p>Your request could not be processed.</p>'
        '<a href="/">Go back to home</a></body></html>',
        status=400
    )

# ===== REDIRECT EXAMPLE =====
def redirect_example(request):
    """Example view that redirects to another page"""
    from django.shortcuts import redirect
    from django.urls import reverse
    
    # You can redirect using:
    # 1. Direct URL: redirect('/datetime/')
    # 2. Named URL: redirect('current-datetime')
    # 3. reverse() function: redirect(reverse('current-datetime'))
    
    return redirect('current-datetime')

def redirect_with_args(request, year):
    """Example view that redirects with arguments"""
    from django.shortcuts import redirect
    return redirect('year-archive', year=year)

# ===== JSON RESPONSE EXAMPLE =====
def json_response(request):
    """Example view returning JSON response"""
    import json
    
    data = {
        'message': 'Hello from Django!',
        'timestamp': datetime.datetime.now().isoformat(),
        'view_type': 'JSON API view',
        'request_method': request.method,
        'user_agent': request.META.get('HTTP_USER_AGENT', 'Unknown')
    }
    
    return HttpResponse(
        json.dumps(data, indent=2), 
        content_type='application/json'
    )

# ===== ASYNC VIEW EXAMPLE =====
async def async_current_datetime(request):
    """An async view that returns the current date and time"""
    import asyncio
    await asyncio.sleep(0.1)  # Simulate some async operation
    
    now = datetime.datetime.now()
    html = '<html lang="en"><body><h1>Async View</h1>It is now %s.<br><p>This was generated by an async view!</p></body></html>' % now
    return HttpResponse(html)

# View with extra options
def year_archive_with_extra(request, year, **kwargs):
    extra_info = ""
    if kwargs:
        extra_info = f", Extra options: {kwargs}"
    return HttpResponse(f"Archive for year: {year}{extra_info}")


# ===== CLASS-BASED VIEWS EXAMPLES =====

class AboutView(TemplateView):
    """Basic TemplateView example - displays a static template"""
    template_name = "articles/about.html"
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = 'About Us'
        context['description'] = 'This is an example of Django Class-based TemplateView'
        context['current_time'] = datetime.datetime.now()
        return context


class SimpleRedirectView(RedirectView):
    """Basic RedirectView example - redirects to another URL"""
    url = '/datetime/'  # Static redirect
    permanent = False   # Use 302 redirect instead of 301


class DynamicRedirectView(RedirectView):
    """Dynamic RedirectView - constructs URL based on arguments"""
    permanent = False
    
    def get_redirect_url(self, *args, **kwargs):
        year = kwargs.get('year')
        return f'/articles/{year}/'


class BasicView(View):
    """Basic View class example - handles different HTTP methods"""
    
    def get(self, request, *args, **kwargs):
        return HttpResponse(
            '<h1>Basic Class-based View</h1>'
            '<p>This is a GET request</p>'
            '<form method="post"><button type="submit">Send POST</button></form>'
        )
    
    def post(self, request, *args, **kwargs):
        return HttpResponse(
            '<h1>Basic Class-based View</h1>'
            '<p>This is a POST request</p>'
            '<a href="/cbv/basic/">Back to GET</a>'
        )


class AsyncClassView(View):
    """Asynchronous class-based view example"""
    
    async def get(self, request, *args, **kwargs):
        import asyncio
        # Simulate some async operation
        await asyncio.sleep(0.5)
        
        html = f'''
        <h1>Async Class-based View</h1>
        <p>This response was generated asynchronously!</p>
        <p>Current time: {datetime.datetime.now()}</p>
        <a href="/">← Back to Home</a>
        '''
        return HttpResponse(html)


class APIView(View):
    """API-style class-based view with different HTTP methods"""
    
    def get(self, request, *args, **kwargs):
        data = {
            'message': 'GET request to API view',
            'timestamp': datetime.datetime.now().isoformat(),
            'method': 'GET',
            'available_methods': ['GET', 'POST', 'PUT', 'DELETE']
        }
        return HttpResponse(
            json.dumps(data, indent=2),
            content_type='application/json'
        )
    
    def post(self, request, *args, **kwargs):
        data = {
            'message': 'POST request to API view',
            'timestamp': datetime.datetime.now().isoformat(),
            'method': 'POST',
            'data_received': 'Success'
        }
        return HttpResponse(
            json.dumps(data, indent=2),
            content_type='application/json'
        )
    
    def put(self, request, *args, **kwargs):
        data = {
            'message': 'PUT request to API view',
            'timestamp': datetime.datetime.now().isoformat(),
            'method': 'PUT',
            'data_updated': 'Success'
        }
        return HttpResponse(
            json.dumps(data, indent=2),
            content_type='application/json'
        )
    
    def delete(self, request, *args, **kwargs):
        data = {
            'message': 'DELETE request to API view',
            'timestamp': datetime.datetime.now().isoformat(),
            'method': 'DELETE',
            'data_deleted': 'Success'
        }
        return HttpResponse(
            json.dumps(data, indent=2),
            content_type='application/json'
        )


# ===== DJANGO FORMS EXAMPLES =====

def get_name(request):
    """Basic form example from Django documentation"""
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request
        form = NameForm(request.POST)
        # Check whether it's valid
        if form.is_valid():
            # Process the data in form.cleaned_data as required
            name = form.cleaned_data['your_name']
            # Redirect to a new URL
            return HttpResponseRedirect(f'/forms/thanks/?name={name}')
    else:
        # If a GET (or any other method) we'll create a blank form
        form = NameForm()

    return render(request, 'articles/name_form.html', {'form': form})


def contact(request):
    """Contact form example with email sending"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            # In a real application, you would send the email here
            # send_mail(subject, message, sender, ['admin@example.com'])
            
            return render(request, 'articles/contact_success.html', {
                'subject': subject,
                'sender': sender,
                'cc_myself': cc_myself
            })
    else:
        form = ContactForm()

    return render(request, 'articles/contact_form.html', {'form': form})


def search(request):
    """Search form using GET method"""
    results = []
    form = SearchForm(request.GET or None)
    
    if form.is_valid():
        query = form.cleaned_data['query']
        category = form.cleaned_data.get('category', 'all')
        
        # Mock search results
        mock_data = [
            {'title': 'Django Tutorial', 'category': 'tutorials', 'content': 'Learn Django from scratch'},
            {'title': 'Python Guide', 'category': 'guides', 'content': 'Complete Python programming guide'},
            {'title': 'Web Development Article', 'category': 'articles', 'content': 'Modern web development practices'},
            {'title': 'Database Design Guide', 'category': 'guides', 'content': 'How to design efficient databases'},
            {'title': 'API Development Tutorial', 'category': 'tutorials', 'content': 'Building REST APIs with Django'},
        ]
        
        # Filter results based on query and category
        for item in mock_data:
            if query.lower() in item['title'].lower() or query.lower() in item['content'].lower():
                if category == 'all' or item['category'] == category:
                    results.append(item)
    
    return render(request, 'articles/search.html', {
        'form': form,
        'results': results,
        'query': form.cleaned_data.get('query', '') if form.is_valid() else ''
    })


def advanced_form_view(request):
    """Advanced form with various field types"""
    if request.method == 'POST':
        form = AdvancedForm(request.POST, request.FILES)
        if form.is_valid():
            return render(request, 'articles/advanced_form_success.html', {
                'data': form.cleaned_data
            })
    else:
        form = AdvancedForm()

    return render(request, 'articles/advanced_form.html', {'form': form})


def feedback_view(request):
    """Feedback form with custom validation"""
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            return render(request, 'articles/feedback_success.html', {
                'data': form.cleaned_data
            })
    else:
        form = FeedbackForm()

    return render(request, 'articles/feedback_form.html', {'form': form})


def thanks_view(request):
    """Thank you page for forms"""
    name = request.GET.get('name', 'Anonymous')
    return HttpResponse(
        f'<h1>Thank you, {name}!</h1>'
        f'<p>Your form has been submitted successfully.</p>'
        f'<a href="/forms/">← Back to Forms</a>'
    )


def forms_home(request):
    """Home page for forms examples"""
    html = '''
    <html lang="en">
    <head>
        <title>Django Forms Lab</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; background-color: #f8f9fa; }
            .container { background: white; border-radius: 10px; padding: 30px; max-width: 800px; margin: 0 auto; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }
            h1 { color: #0066cc; }
            h2 { color: #0088cc; margin-top: 30px; }
            ul { list-style-type: none; }
            li { margin: 10px 0; }
            a { text-decoration: none; color: #0066cc; }
            a:hover { text-decoration: underline; }
            .description { background: #e9ecef; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Django Forms Lab Examples</h1>
            <div class="description">
                <p>This section demonstrates Django Forms concepts from the official documentation.</p>
                <p>Forms are essential for handling user input in web applications.</p>
            </div>
            
            <h2>📝 Basic Forms</h2>
            <ul>
                <li><a href="/forms/name/">Name Form (Basic Example)</a></li>
                <li><a href="/forms/contact/">Contact Form (Multiple Fields)</a></li>
            </ul>
            
            <h2>🔍 GET Method Forms</h2>
            <ul>
                <li><a href="/forms/search/">Search Form (GET method)</a></li>
            </ul>
            
            <h2>🎛️ Advanced Forms</h2>
            <ul>
                <li><a href="/forms/advanced/">Advanced Form (All Field Types)</a></li>
                <li><a href="/forms/feedback/">Feedback Form (Custom Validation)</a></li>
            </ul>
            
            <h2>🏠 Other Sections</h2>
            <ul>
                <li><a href="/">← Back to Main Lab Home</a></li>
            </ul>
        </div>
    </body>
    </html>
    '''
    return HttpResponse(html)
