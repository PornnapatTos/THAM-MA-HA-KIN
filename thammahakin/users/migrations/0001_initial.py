# Generated by Django 3.1.1 on 2020-10-17 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Thammart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('t_user', models.CharField(max_length=10)),
                ('t_name', models.CharField(max_length=50)),
                ('t_detail', models.CharField(max_length=200)),
                ('t_cat', models.CharField(choices=[('food', 'Food'), ('closet', 'Closet'), ('accessary', 'Accessary'), ('beauty', 'Beauty'), ('electronic', 'Electronic'), ('others', 'Others')], max_length=20)),
                ('t_count', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('p_user', models.CharField(max_length=10)),
                ('p_name', models.CharField(max_length=50)),
                ('p_sname', models.CharField(max_length=50)),
                ('p_mail', models.CharField(max_length=40)),
                ('p_phone', models.CharField(max_length=40)),
                ('p_facebook', models.CharField(max_length=40)),
                ('p_instragram', models.CharField(max_length=40)),
                ('p_line', models.CharField(max_length=40)),
                ('p_fav', models.ManyToManyField(blank=True, related_name='favorites', to='users.Thammart')),
                ('p_mymart', models.ManyToManyField(blank=True, related_name='mymart', to='users.Thammart')),
            ],
        ),
    ]