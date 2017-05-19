from django import forms

from django.contrib.auth.models import User


class UserInfoForm(forms.ModelForm):
    avatar = forms.FileField(required=False)

    def save(self, commit=True):
        instance = super(UserInfoForm, self).save(commit=commit)
        # print (self.cleaned_data['avatar'])
        if self.cleaned_data['avatar']:
            instance.profile.avatar = self.cleaned_data['avatar']
            instance.profile.save()

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'avatar']
