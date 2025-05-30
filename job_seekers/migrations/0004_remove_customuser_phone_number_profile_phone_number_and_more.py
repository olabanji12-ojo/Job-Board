# Generated by Django 5.1.1 on 2025-05-12 13:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_seekers', '0003_alter_customuser_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone_number',
        ),
        migrations.AddField(
            model_name='profile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[('employer', 'Employer'), ('employee', 'Employee')], max_length=30),
        ),
        migrations.CreateModel(
            name='Employer_Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=255)),
                ('company_details', models.TextField()),
                ('location', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=20, null=True)),
                ('company_logo', models.ImageField(blank=True, default='download.jpg', null=True, upload_to='static/images')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='employer_account', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
