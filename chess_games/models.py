from django.contrib.auth.models import User
from django.db import models
from django.core.exceptions import ValidationError


def more_than_2_validator(value):
    if 2 > value:
        raise ValidationError('There need to be more than 2 players')


class Tournament(models.Model):
    name = models.CharField(max_length=50, unique=True)
    date = models.DateTimeField()
    number_of_players = models.IntegerField(help_text="Maximal number of players", validators=[more_than_2_validator])
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Player(models.Model):
    name = models.CharField(max_length=50)
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('name', 'tournament',)

    def __str__(self):
        return self.name


class Game(models.Model):
    RESULT = [("1-0", "1-0"), ("0-0", "0-0"), ("0-1", "0-1")]
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE)
    result = models.CharField(
        max_length=3,
        choices=RESULT,
        null=True)
    white = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name="white")
    black = models.ForeignKey(Player, null=True, on_delete=models.SET_NULL, related_name="black")

    def save(self, *args, **kwargs):
        if self.white is None or self.black is None:
            super(Game, self).save(*args, **kwargs)
        elif self.white.name == self.black.name and self.white.tournament == self.black.tournament:
            raise ValidationError('Both players cant be the same')
        else:
            super(Game, self).save(*args, **kwargs)

    def __str__(self):
        try:
            return "Game: " + self.white.name + " vs " + self.black.name
        except:
            return "Empty game"
