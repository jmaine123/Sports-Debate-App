from django import forms

class PlayerForm(forms.Form):
    # player = forms.IntegerField(label='player ID')
    # player_two = forms.IntegerField(label='player2 ID')
    player = forms.CharField(label='PLAYER 1')
    player_two = forms.CharField(label='PLAYER 2')
