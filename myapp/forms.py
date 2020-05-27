from django import forms

class PlayerForm(forms.Form):
    player = forms.CharField(label='PLAYER 1')
    player_two = forms.CharField(label='PLAYER 2')
