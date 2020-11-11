from django import forms

class EntryCreationForm(forms.Form):

	title=forms.CharField(max_length=200)
	entry=forms.CharField(widget=forms.Textarea())

class EditEntryForm(forms.Form):

	title=forms.CharField(max_length=200)
	entry=forms.CharField(widget=forms.Textarea())