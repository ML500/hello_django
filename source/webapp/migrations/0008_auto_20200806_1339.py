# Generated by Django 2.2 on 2020-08-06 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20200806_1337'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='articles', through='webapp.ArticleTag', to='webapp.Tag', verbose_name='Теги'),
        ),
    ]
