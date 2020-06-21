# Generated by Django 3.0.7 on 2020-06-21 20:32

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
            name='Boxscore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('loser', models.TextField(blank=True, db_column='Loser', null=True)),
                ('loserscore', models.IntegerField(blank=True, db_column='LoserScore', null=True)),
                ('winner', models.TextField(blank=True, db_column='Winner', null=True)),
                ('winnerscore', models.IntegerField(blank=True, db_column='WinnerScore', null=True)),
                ('topscorer', models.TextField(blank=True, db_column='TopScorer', null=True)),
                ('topscorerpoints', models.IntegerField(blank=True, db_column='TopScorerPoints', null=True)),
            ],
            options={
                'db_table': 'boxScore',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='Playersinfo',
            fields=[
                ('id', models.AutoField(db_column='ID', primary_key=True, serialize=False)),
                ('player_id', models.TextField(blank=True, db_column='Player_id', null=True)),
                ('name', models.TextField(blank=True, db_column='Name', null=True)),
                ('position', models.TextField(blank=True, db_column='Position', null=True)),
                ('height', models.FloatField(blank=True, db_column='Height', null=True)),
                ('birthdate', models.TextField(blank=True, db_column='Birthdate', null=True)),
                ('college', models.TextField(blank=True, db_column='College', null=True)),
                ('url', models.TextField(blank=True, db_column='Url', null=True)),
            ],
            options={
                'db_table': 'playersInfo',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='DebateStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=20)),
                ('status', models.CharField(max_length=100)),
                ('open_debate', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('agree', models.IntegerField(default=0)),
                ('disagree', models.IntegerField(default=0)),
                ('opinion_total', models.IntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'debateStatus',
            },
        ),
        migrations.CreateModel(
            name='Debate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p1_id', models.IntegerField(default=0)),
                ('p2_id', models.IntegerField(default=0)),
                ('p1_name', models.TextField(blank=True, null=True)),
                ('p2_name', models.TextField(blank=True, null=True)),
                ('p1_user_id', models.TextField(blank=True, null=True)),
                ('p2_user_id', models.TextField(blank=True, null=True)),
                ('p1_vote', models.IntegerField(default=0)),
                ('p2_vote', models.IntegerField(default=0)),
                ('user_pick', models.TextField(default='1')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'debate',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL)),
                ('following', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'follower',
                'unique_together': {('follower', 'following')},
            },
        ),
    ]
