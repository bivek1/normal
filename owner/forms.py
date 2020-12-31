from django import forms
from .models import Customer, Category, Sub_Category, Product, Order
from owner.models import CustomUser
from django.core.exceptions import ValidationError


class UserRegistration(forms.ModelForm):
    re_password = forms.CharField(label = 'Repeat Password', widget = forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Repeat Password'}))
    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password', 're_password')
        
        labels = {
            'first_name': 'Phone Number',
            'last_name' :'Last Name',
            'email':'Email Address',
            'password':'Password'
        }
        
        widgets = {
            'first_name': forms.TextInput(attrs= {'class':'form-control', 'placeholder':'First Name'}),
            'last_name' : forms.TextInput(attrs = {'class':'form-control', 'placeholder':'Last Name'}),
            'email': forms.TextInput(attrs={'class':'form-control', 'placeholder' : 'Email'}),
            'password':forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Password'})
        }
    def clean_email(self):
        email = self.cleaned_data['email']
        try:
            match = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            # Unable to find a user, this is fine
            return email

        # A user was found with this as a username, raise an error.
        raise forms.ValidationError('This email address is already in use.')
   
    def clean_password(self):
        data = self.cleaned_data['password']
        d = str(data)
        if len(d) < 6:
            raise ValidationError("Password must be greater than 6 digits")
        return data
    def clean_re_password(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('re_password')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('Password Did not Match')
        return password2
    
class AddCat(forms.ModelForm):
    class Meta:
        model = Category
        fields = ('name',)
        labels = {
            'name' : 'Category Name',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Category Name'}),
        }
    def clean_name(self):
        data = self.cleaned_data['name']
        try:
            check = data.lower()
            same = Category.objects.get(name = check)
        except:
            return data
        raise ValidationError('This Category is added already')
        
class AddSubCat(forms.ModelForm):
    class Meta:
        model = Sub_Category
        fields = ('sub_name', 'category')
        widgets = {
            'sub_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Sub Category Name'}),
            'category': forms.Select(attrs={'class':'form-control', 'placeholder':'Category Name'}),
        }
    
    def clean_name(self):
        data = self.cleaned_data['name']
        try:
            check = data.lower()
            same = Sub_Category.objects.get(sub_name = check)
        except:
            return data
        raise ValidationError('This Sub-Category is added already') 
    
class AddProduct(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('category', 'sub_category', 'name', 'description', 'price', 'available','image')
        
        widgets = {
            'category': forms.Select(attrs= {'class':'form-control'}),
            'sub_category': forms.Select(attrs= {'class':'form-control'}),
            'name' : forms.TextInput(attrs= {'class':'form-control','placeholder':'Product Name'}),
            'description': forms.Textarea(attrs= {'class':'form-control','placeholder':'Description'}),
            'price':forms.TextInput(attrs= {'class':'form-control','placeholder':'Product Price'}),
            'available':forms.CheckboxInput(attrs= {'class':'form-check-input'}),
            'image':forms.FileInput(attrs= {'class':'form-control','placeholder':'Image'}),
        }
        
        labels = {
            'category': 'Choose Category',
            'sub_category': 'Choose Sub Category',
            'name' : 'Product Name',
            'description': 'Product Description',
            'price':'Price',
            'available':'Available',
            'image':'Product Image',
        }
        
class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'number', 'address', 'city']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}),
            'number': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone Number'}),
            'address': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address'}),
            'city': forms.TextInput(attrs={'class':'form-control', 'placeholder':'City'}),
        }
        labels= {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'number': 'Phone Number',
            'address': 'Address',
            'city': 'City',
        }
        
    def clean_number(self):
        data = self.cleaned_data['number']
        d = str(data)
        if len(d) > 10 or len(d) < 10 :
            raise ValidationError("Number can not be less or more than 10 digits")
        if not d.startswith('98'):
            raise ValidationError("Nepali number should start with 98")
        return data