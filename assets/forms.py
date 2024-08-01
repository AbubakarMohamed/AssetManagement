from django import forms
from .models import Lend, Maintenance, Asset


class LendForm(forms.ModelForm):
    id = forms.ModelChoiceField(queryset=Asset.objects.none(), required=False, widget=forms.Select(attrs={'class': 'form-control'}))
   
    class Meta:
        model = Lend
        fields = ['asset', 'quantity', 'id', 'person_picking',  'organisation', 'phone_number', 'picking', 'returning']
        widgets = {
            'asset': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'picking': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'returning': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'person_picking': forms.TextInput(attrs={'class': 'form-control'}),
            'organisation': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            
        }

    def __init__(self, *args, **kwargs):
        super(LendForm, self).__init__(*args, **kwargs)
        self.fields['asset'].queryset = Asset.objects.all()
        
        if 'asset' in self.data:
            try:
                asset_id = int(self.data.get('asset'))
                self.fields['id'].queryset = Asset.objects.filter(id=asset_id)
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty queryset
        elif self.instance.pk:
            self.fields['id'].queryset = self.instance.asset.id_set.all()

    def clean(self):
        cleaned_data = super().clean()
        picking_date = cleaned_data.get('picking')
        returning_date = cleaned_data.get('returning')

        if picking_date and returning_date:
            if returning_date < picking_date:
                self.add_error('returning', 'Returning date should be greater than or equal to picking date.')

        return cleaned_data


class MaintenanceForm(forms.ModelForm):
    class Meta:
        model = Maintenance
        fields = ['asset', 'quantity', 'is_fixed']
        widgets = {
            'asset': forms.Select(attrs={ 'readonly': 'readonly'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'is_fixed': forms.CheckboxInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make asset and quantity fields readonly
        self.fields['asset'].widget.attrs['readonly'] = 'readonly'
        self.fields['quantity'].widget.attrs['readonly'] = 'readonly'

    def clean_quantity(self):
        quantity = self.cleaned_data.get('quantity')
        if quantity is not None and quantity < 0:
            raise forms.ValidationError("Quantity cannot be negative.")
        return quantity

class AddAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = ['name', 'total_quantity']  # Exclude 'available_quantity' and 'unique_id'
        widgets = {
            'name': forms.Select(choices=Asset.ASSET_CHOICES, attrs={'class': 'form-control'}),
            'total_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }

    def clean_total_quantity(self):
        total_quantity = self.cleaned_data.get('total_quantity')
        if total_quantity is not None and total_quantity < 0:
            raise forms.ValidationError("Total quantity cannot be negative.")
        return total_quantity

class ReturnAssetForm(forms.ModelForm):
    quantity_good = forms.IntegerField(min_value=0, label='Quantity in Good Condition', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    quantity_bad = forms.IntegerField(min_value=0, label='Quantity in Bad Condition', widget=forms.NumberInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Lend
        fields = ['returned_date', 'condition']
        widgets = {
            'returned_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'condition': forms.Select(choices=[('Good', 'Good'), ('Bad', 'Bad')], attrs={'class': 'form-control'}),
        }
