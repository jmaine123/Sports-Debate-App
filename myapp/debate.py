from django.forms import ModelForm


class DebateForm(ModelForm):
    class Meta:
        model = Debate
        fields = ['playerone', 'playertwo', 'p1_id', 'p2_id', 'vote', 'userid']
    # def __init__(self, player1, player2, p1_current, p2_current, p1_career, p2_career, userid):
    #     self.player1 = player1
    #     self.player2 = player2
    #     self.p1_current = p1_current
    #     self.p2_current = p2_current
    #     self.p1_career = p1_career
    #     self.p2_career = p2_career
    #     self.userid = userid

    def create_players(self):
        id1 = self.cleaned_data['p1_id']
        id2 = self.cleaned_data['p2_id']
        player1 = Playersinfo.ojects.get(pk=id1)
        player2 = Playersinfo.ojects.get(pk=id2)
