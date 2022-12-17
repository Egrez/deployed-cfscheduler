from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        label='Username:',
        validators=[],
        widget = forms.TextInput(attrs = {
            'class' : 'form-control w-100',
        }),

    )
    
    password = forms.CharField(
        label='Password:',
        validators=[],
        widget = forms.PasswordInput(attrs = {
            'class' : 'form-control w-100',
        }),
    )

