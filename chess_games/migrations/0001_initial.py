
import chess_games.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('date', models.DateTimeField()),
                ('number_of_players', models.IntegerField(help_text='Maximal number of players', validators=[chess_games.models.more_than_2_validator])),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Player',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chess_games.Tournament')),
            ],
            options={
                'unique_together': {('name', 'tournament')},
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(choices=[('1-0', '1-0'), ('1-1', '0-0'), ('0-1', '0-1')], max_length=3, null=True)),
                ('black', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='black', to='chess_games.Player')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chess_games.Tournament')),
                ('white', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='white', to='chess_games.Player')),
            ],
        ),
    ]
