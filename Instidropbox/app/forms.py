"""
Definition of forms.
"""

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import ReqDetails
class BootstrapAuthenticationForm(AuthenticationForm):
    """Authentication form which uses boostrap CSS."""
    username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))

class SignUpForm(UserCreationForm):
    #is_student=forms.BooleanField()
    '''username = forms.CharField(max_length=254,
                               widget=forms.TextInput({
                                   'class': 'form-control',
                                   'placeholder': 'User name'}))
    password1 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                   'placeholder':'Password'}))
    password2 = forms.CharField(label=_("Password"),
                               widget=forms.PasswordInput({
                                   'class': 'form-control',
                                  'placeholder':'Password'}))
    '''
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']     #, 'is_student']
      

class RequestDetailsForm(forms.ModelForm):
    class Meta:
        model=ReqDetails
        fields=["Req_Type","Req_details","sender_id","receiver_id","Req_Status","dateof_request","visibilty_sender_id","visible_to_Hod","visible_to_Principal"]
        widgets={
            "Req_Type":forms.TextInput({
                                   'class': 'form-control',
                                   'name':'Req_Type',
                                   'placeholder': 'Request Type'}), 
            "Req_details":forms.Textarea({
                                   'class': 'form-control',
                                   'name':'Req_details',
                                   'placeholder': 'Request/suggestion Details enter here'}),
             "sender_id":forms.TextInput({
                                   'class': 'form-control',
                                   'name':'sender_id',                                    
                                   'placeholder': 'Sender id'}),
              "receiver_id":forms.TextInput({
                                   'class': 'form-control',
                                   'name':'receiver_id',
                                   'placeholder': 'Faculty name'}),
               "Req_Status":forms.TextInput({
                                   'class': 'form-control',
                                   'name':'Req_Status',
                                   }),
                "dateof_request":forms.TextInput({
                                   'class': 'form-control'
                                   }),
                 "visibilty_sender_id":forms.CheckboxInput({
                                   'class': 'form-check-input',
                                   'name':'visibilty_sender_id',
                                  }),
                  "visible_to_Hod":forms.CheckboxInput({
                                   'class': 'form-check-input',
                                   'name':'visible_to_Hod',
                                   }),
                   "visible_to_Principal":forms.CheckboxInput({
                                   'class': 'fform-check-input',
                                   'name':'visible_to_Principal',
                                   }),
         }