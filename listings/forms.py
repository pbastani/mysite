from django import forms
from listings.models import Post


GENERAL = 'general'
FORSALE = 'forsale'
SERVICES = 'services'
HOUSING = 'housing'
CATEGORIES = (
    (GENERAL, 'General'),
    (FORSALE, 'For Sale'),
    (SERVICES, 'Services'),
    (HOUSING, 'Housing'))


class SearchForm(forms.Form):
    search_string = forms.CharField(label="Search", required=False)
    category = forms.ChoiceField(label="Category", choices=CATEGORIES)


class PublishPostForm(forms.Form):
    id = forms.IntegerField(required=False)
    create_date = forms.DateField(required=False)
    expiry_date = forms.DateField(required=False)


class UploadPhotosForm(forms.Form):
    id = forms.IntegerField(required=False)
    photos = forms.FileField(label="Upload Photos", required=False)


class EditPostForm(forms.Form):
    id = forms.IntegerField(required=True)
    title = forms.CharField(label="Title", required=False)
    content = forms.CharField(label="Content", widget=forms.Textarea, required=True)
    tags = forms.CharField(label="Tags", required=False)
    location = forms.CharField(label="Location", required=False)
    price = forms.IntegerField(label="Price", required=False)
    category = forms.ChoiceField(label="Category", choices=CATEGORIES)


class SignupForm(forms.Form):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        required=True,
        )
    display_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)


class SigninForm(forms.Form):
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(),
        required=True,
        )
    email = forms.EmailField()