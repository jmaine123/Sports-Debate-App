from django.forms import ModelForm
from .models import Debate
from django import forms


class DebateForm(ModelForm):
    class Meta:
        model = Debate
        fields = ['p1_id', 'p2_id','user','user_pick']
        widgets = {'p1_id': forms.HiddenInput()}
        widgets = {'p2_id': forms.HiddenInput()}
        widgets = {'user': forms.HiddenInput()}
        widgets = {'user_pick': forms.RadioSelect()}

    # def create_players(self):
    #     id1 = self.cleaned_data['p1_id']
    #     id2 = self.cleaned_data['p2_id']
    #     player1 = Playersinfo.ojects.get(pk=id1)
    #     player2 = Playersinfo.ojects.get(pk=id2)
