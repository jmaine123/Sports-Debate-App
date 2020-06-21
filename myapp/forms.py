from django import forms

class PlayerForm(forms.Form):
    player = forms.CharField(label='PLAYER 1')
    player_two = forms.CharField(label='PLAYER 2')

class DebateStatusBar(forms.Form):
    status = forms.CharField(label='Write your debate', max_length=100)
    open_debate = forms.BooleanField()
    user_id = forms.IntegerField(widget=forms.HiddenInput())
