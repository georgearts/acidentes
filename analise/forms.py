from django import forms

class AcidenteForm(forms.Form):
    Numero_Ocorrencia = forms.CharField(max_length=100, required=False)
    Data = forms.DateField(required=False)
    Localidade = forms.CharField(max_length=100)
    UF = forms.CharField(max_length=2)
    Aerodromo = forms.CharField(max_length=100)
    Operacao = forms.CharField(max_length=100)
