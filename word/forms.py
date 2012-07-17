from django import forms

class UploadForm(forms.Form): #todo: add functions for cleaning file uploads: ensure they are unicode, strip metadata and encode as yaml
    file = forms.FileField(
        label  = u'Plain Text or CSV file',
        required = True,
        widget = forms.ClearableFileInput()
    )
