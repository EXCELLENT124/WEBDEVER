from django import forms
from django.core.validators import RegexValidator, EmailValidator
from .models import WebsiteApplication, ApplicationMessage
from services.models import WebsiteType, AdditionalService


class WebsiteApplicationForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your first name',
            'required': 'required'
        }),
        label='First Name'
    )
    
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your last name',
            'required': 'required'
        }),
        label='Last Name'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'required': 'required'
        }),
        label='Email Address',
        validators=[EmailValidator()]
    )
    
    phone = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 0831234567 or +27831234567',
            'required': 'required'
        }),
        label='Phone Number',
        validators=[
            RegexValidator(
                regex=r'^(\+27|0)[6-8][0-9]{8}$',
                message='Enter a valid South African phone number (e.g., 0831234567)'
            )
        ]
    )
    
    company_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Company name (optional)'
        }),
        label='Company Name'
    )
    
    website_type = forms.ModelChoiceField(
        queryset=WebsiteType.objects.filter(is_active=True),
        widget=forms.Select(attrs={
            'class': 'form-control form-select',
            'required': 'required'
        }),
        label='Website Type',
        empty_label='Select a website type...'
    )
    
    project_title = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., My Business Website',
            'required': 'required'
        }),
        label='Project Title'
    )
    
    project_description = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Describe your website project in detail. What do you want to achieve? Who is your target audience?',
            'required': 'required'
        }),
        label='Project Description'
    )
    
    budget_range = forms.ChoiceField(
        choices=WebsiteApplication.BUDGET_RANGES,
        widget=forms.Select(attrs={
            'class': 'form-control form-select',
            'required': 'required'
        }),
        label='Budget Range'
    )
    
    preferred_timeline = forms.IntegerField(
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 30 (for 30 days)',
            'min': '7',
            'max': '365'
        }),
        label='Preferred Timeline (days)',
        help_text='Optional - let us know if you have a deadline'
    )
    
    additional_services = forms.ModelMultipleChoiceField(
        queryset=AdditionalService.objects.filter(is_active=True),
        required=False,
        widget=forms.CheckboxSelectMultiple(),
        label='Additional Services (Optional)'
    )
    
    design_preferences = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Any specific design preferences? Colors, style, examples of websites you like...'
        }),
        label='Design Preferences'
    )
    
    has_logo = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='I have a logo'
    )
    
    has_content = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='I have content ready (text, images)'
    )
    
    has_domain = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='I have a domain registered'
    )
    
    features_needed = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'List specific features needed: e.g., contact form, photo gallery, booking system, payment integration, etc.'
        }),
        label='Specific Features Needed'
    )
    
    # Price estimate display (not a field, just for display)
    price_estimate = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control price-estimate-display',
            'readonly': 'readonly'
        }),
        label='Estimated Price Range'
    )
    
    class Meta:
        model = WebsiteApplication
        fields = [
            'first_name', 'last_name', 'email', 'phone', 'company_name',
            'website_type', 'project_title', 'project_description',
            'budget_range', 'preferred_timeline', 'additional_services',
            'design_preferences', 'has_logo', 'has_content', 'has_domain',
            'features_needed'
        ]
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make price_estimate not required
        self.fields['price_estimate'].required = False
        self.fields['price_estimate'].initial = 'Select a website type to see price estimate'


class ApplicationMessageForm(forms.ModelForm):
    sender_name = forms.CharField(
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your name'
        }),
        label='Your Name'
    )
    
    sender_email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com'
        }),
        label='Your Email'
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Type your message here...'
        }),
        label='Message'
    )
    
    class Meta:
        model = ApplicationMessage
        fields = ['sender_name', 'sender_email', 'message']


class ContactForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Your full name',
            'required': 'required'
        }),
        label='Full Name'
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'your.email@example.com',
            'required': 'required'
        }),
        label='Email Address'
    )
    
    phone = forms.CharField(
        required=False,
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Phone number (optional)'
        }),
        label='Phone Number'
    )
    
    subject = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Subject of your message',
            'required': 'required'
        }),
        label='Subject'
    )
    
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 5,
            'placeholder': 'Your message...',
            'required': 'required'
        }),
        label='Message'
    )