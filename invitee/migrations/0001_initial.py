# Generated by Django 3.2.16 on 2023-05-01 04:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inviter', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitee',
            fields=[
                ('invitee_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('message', models.CharField(blank=True, max_length=250, null=True)),
                ('schedule', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inviter.schedule')),
            ],
        ),
    ]
