# Generated by Django 4.1.1 on 2022-10-04 12:56

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shortener', '0002_shortlink_is_active'),
    ]

    operations = [
        migrations.CreateModel(
            name='ShortLinkStatistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField(default=django.utils.timezone.now)),
                ('ip', models.CharField(max_length=255)),
                ('referrer_url', models.CharField(blank=True, max_length=255, null=True)),
                ('short_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shortener.shortlink')),
            ],
        ),
    ]
