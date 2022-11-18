from django import forms


class DateInputCustom(forms.DateInput):
    input_type = 'date'
