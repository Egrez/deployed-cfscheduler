from django import forms

class LoginForm(forms.Form):
    email = forms.CharField(
        label='Username:',
        validators=[],
        widget = forms.TextInput(attrs = {
            "class" : "text",
            "style" : "margin-top: 7%; font-weight: bolder;",
            "name" : "fname",
            "value" : "Email: ",
            "placeholder" : "cf/scheduler@gmail.com",
        }),

    )

    name = forms.CharField(
        label='Username:',
        validators=[],
        widget = forms.TextInput(attrs = {
            "class" : "text",
            "style" : "margin-top: 2%; font-weight: bolder;",
            "name" : "fname",
            "value" : "Name: ",
            "placeholder" : "Fort was here",
        }),

    )
    
    password = forms.CharField(
        label='Password:',
        validators=[],
        widget = forms.PasswordInput(attrs = {
            "class" : "password",
            "style" : "margin-top: 2%; font-weight: bolder;",
            "name" : "fname",
            "value" : "Password: ",
            "placeholder" : "*******",
        }),
    )

