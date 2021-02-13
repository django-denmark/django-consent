# Generated by Django 3.0.11 on 2021-02-13 21:05

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
            name='EmailConsent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email_hash', models.UUIDField()),
            ],
        ),
        migrations.CreateModel(
            name='EmailConsentSources',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source_name', models.CharField(max_length=255)),
                ('definition', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='EmailOptOut',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_everything', models.BooleanField(default=False, editable=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('email_hash', models.UUIDField()),
                ('consent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='optouts', to='django_consent.EmailConsent')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='optouts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='emailconsent',
            name='source',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='django_consent.EmailConsentSources'),
        ),
        migrations.AddField(
            model_name='emailconsent',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='EmailCampaign',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('consent', models.ManyToManyField(to='django_consent.EmailConsentSources')),
            ],
        ),
    ]
