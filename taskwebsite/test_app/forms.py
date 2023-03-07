from django import forms
from django.contrib.auth.models import User

from .models import Customer,Branch,District

GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'))
class CustomerForm(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    gender = forms.ChoiceField( widget=forms.RadioSelect,choices=GENDER_CHOICES)
    district = forms.ModelChoiceField(queryset=District.objects.all())
    branch= forms.ModelChoiceField(queryset=Branch.objects.none())
    account_type = forms.ChoiceField(choices=[('savings', 'Savings'),
                                              ('current', 'Current')])
    materials_provide = forms.MultipleChoiceField(choices=[('debit', 'Debit Card'),
                                                           ('credit', 'Credit Card'),
                                                           ('cheque', 'Cheque Book')],
                                                 widget=forms.CheckboxSelectMultiple)


    class Meta:
        model = Customer
        fields = ('name', 'dob','age', 'gender', 'phone_number', 'email', 'address','district','branch', 'account_type', 'materials_provide')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['branch'].queryset = Branch.objects.none()
        if 'district' in self.data:
            try:
                district_id = int(self.data.get('district'))
                self.fields['branch'].queryset = Branch.objects.filter(district_id=district_id).order_by('name')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['branch'].queryset = self.instance.district.branch_set.order_by('name')