import datetime
from django import forms
from .models import Tournament, Player


class TournamentForm(forms.ModelForm):
    date = forms.DateTimeField(initial=f"{datetime.datetime.now():%Y-%m-%d %H:%M}",
                               help_text="Format YYYY-mm-dd HH:MM")

    class Meta:
        model = Tournament
        fields = ('name', 'date', 'number_of_players')


class AddPlayerForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    tournament = forms.ChoiceField()

    class Meta:
        model = Player
        fields = ('name',)

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(AddPlayerForm, self).__init__(*args, **kwargs)
        if self.user is not None:
            if self.user.is_superuser:
                self.fields['tournament'].choices = [tuple([p.name, p.name])
                                                     for p in Tournament.objects.all()]
            else:
                self.fields['tournament'].choices = [tuple([p.name, p.name])
                                                     for p in Tournament.objects.filter(user=self.user)]


class FilterByDate(forms.Form):
    date_from = forms.DateTimeField(initial=f"{datetime.date.today() - datetime.timedelta(days=1):%Y-%m-%d %H:%M}", input_formats=["%Y-%m-%d %H:%M"])
    date_to = forms.DateTimeField(initial=f"{datetime.date.today():%Y-%m-%d %H:%M}", input_formats=["%Y-%m-%d %H:%M"])


class GameForm(forms.Form):
    RESULT = [("1-0", "1-0"), ("0-0", "0-0"), ("0-1", "0-1")]
    result = forms.ChoiceField()

    def __init__(self, *args, **kwargs):
        super(GameForm, self).__init__(*args, **kwargs)
        self.fields['result'].choices = self.RESULT
