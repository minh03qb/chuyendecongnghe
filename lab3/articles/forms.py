from django import forms


class NameForm(forms.Form):
    """Basic form example from Django documentation"""
    your_name = forms.CharField(label="Your name", max_length=100)


class ContactForm(forms.Form):
    """More complex form with different field types"""
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)


class SearchForm(forms.Form):
    """Simple search form using GET method"""
    query = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter your search term...',
            'class': 'form-control'
        })
    )
    category = forms.ChoiceField(
        choices=[
            ('all', 'All Categories'),
            ('articles', 'Articles'),
            ('tutorials', 'Tutorials'),
            ('guides', 'Guides'),
        ],
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )


class AdvancedForm(forms.Form):
    """Form demonstrating various field types and widgets"""
    # Text fields
    username = forms.CharField(
        max_length=50,
        help_text="Enter a unique username",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        min_length=8
    )
    
    # Email and URL
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    
    website = forms.URLField(
        required=False,
        widget=forms.URLInput(attrs={'class': 'form-control'})
    )
    
    # Numbers
    age = forms.IntegerField(
        min_value=1,
        max_value=120,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    salary = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    
    # Date and time
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    
    appointment_time = forms.DateTimeField(
        required=False,
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'})
    )
    
    # Choices
    gender = forms.ChoiceField(
        choices=[
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Other'),
        ],
        widget=forms.RadioSelect
    )
    
    interests = forms.MultipleChoiceField(
        choices=[
            ('tech', 'Technology'),
            ('sports', 'Sports'),
            ('music', 'Music'),
            ('books', 'Books'),
            ('movies', 'Movies'),
        ],
        widget=forms.CheckboxSelectMultiple,
        required=False
    )
    
    # File upload
    avatar = forms.ImageField(required=False)
    resume = forms.FileField(required=False)
    
    # Boolean
    newsletter = forms.BooleanField(
        required=False,
        help_text="Subscribe to our newsletter"
    )
    
    terms_accepted = forms.BooleanField(
        label="I accept the terms and conditions",
        error_messages={'required': 'You must accept the terms to proceed.'}
    )


class FeedbackForm(forms.Form):
    """Form with custom validation"""
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    rating = forms.ChoiceField(
        choices=[(1, '1 - Poor'), (2, '2 - Fair'), (3, '3 - Good'), (4, '4 - Very Good'), (5, '5 - Excellent')],
        widget=forms.RadioSelect
    )
    comments = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        help_text="Tell us about your experience"
    )
    
    def clean_name(self):
        """Custom validation for name field"""
        name = self.cleaned_data['name']
        if len(name.split()) < 2:
            raise forms.ValidationError("Please enter your full name (first and last name)")
        return name
    
    def clean(self):
        """Form-wide validation"""
        cleaned_data = super().clean()
        rating = int(cleaned_data.get('rating', 5))
        comments = cleaned_data.get('comments', '')
        
        if rating <= 2 and len(comments) < 20:
            raise forms.ValidationError(
                "For ratings of 2 or below, please provide detailed comments (at least 20 characters)."
            )
        
        return cleaned_data
