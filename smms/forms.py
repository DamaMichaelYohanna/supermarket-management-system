from django.contrib.auth.models import User
from django import forms

from . import models


class UserUpdateForm(forms.ModelForm):
    """form for update user info"""

    class Meta:
        model = models.Profile
        exclude = ('user',)


class UserForm(forms.ModelForm):
    """form for base user"""

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email',)


class ProfileForm(forms.ModelForm):
    """ form for creating new user"""

    # first_name = forms.CharField(max_length=20)
    # last_name = forms.CharField(max_length=20)
    # gender = forms.CharField(max_length=10)
    # email = forms.EmailField()
    # phone = forms.IntegerField()
    # state = forms.CharField(max_length=10)
    # rank = forms.CharField(max_length=20)
    # image = forms.ImageField()
    # address = forms.CharField(max_length=40,widget=forms.Textarea())
    class Meta:
        model = models.Profile
        fields = "__all__"

    # def save(self, commit=True):
    #     user = User.objects.create(username=self.form.get('first_name'),
    #                                password=self.form.get('first_name') + self.form.get('last_name'),
    #                                email=self.form.get('email'),
    #                                first_name=self.form.get('first_name'),
    #                                last_name=self.form.get('last_name'))
    #     profile = models.Profile.objects.create(user=user, phone=self.form.get('phone'),
    #                                             address=self.form.get('address'),
    #                                             rank=self.form.get('rank'),
    #                                             gender=self.form.get('gender'),
    #                                             )
    #     if "FILES" in self.form:
    #         profile.image = forms.FILES
    #     else:
    #         print('no image in files')
    #         pass


class AddSaleForm(forms.ModelForm):
    class Meta:
        model = models.Sale
        fields = "__all__"


class AddProductForm(forms.ModelForm):
    class Meta:
        model = models.Product
        fields = "__all__"
