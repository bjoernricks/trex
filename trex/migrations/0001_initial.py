# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(default=django.utils.timezone.now, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(max_length=30, verbose_name='first name', blank=True)),
                ('last_name', models.CharField(max_length=30, verbose_name='last name', blank=True)),
                ('email', models.EmailField(unique=True, max_length=254, verbose_name='email address', db_index=True)),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('groups', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Group', blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of his/her group.', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(related_query_name='user', related_name='user_set', to='auth.Permission', blank=True, help_text='Specific permissions for this user.', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateField()),
                ('duration', models.PositiveIntegerField()),
                ('description', models.TextField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('state', models.CharField(max_length=b'5', blank=True)),
                ('workpackage', models.CharField(max_length=255, blank=True)),
            ],
            options={
                'ordering': ('date', 'created'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(unique=True, max_length=50)),
                ('description', models.TextField(default=b'', blank=True)),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ('name', 'active'),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_abbr', models.CharField(max_length=25, verbose_name=b'User abbreviation for the project')),
                ('project', models.ForeignKey(related_name=b'project_users', to='trex.Project')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField(default=b'', blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('project', models.ForeignKey(related_name=b'tags', to='trex.Project')),
            ],
            options={
                'ordering': ('name',),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='projectuser',
            unique_together=set([('project', 'user_abbr')]),
        ),
        migrations.AddField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name=b'projects', through='trex.ProjectUser', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='project',
            field=models.ForeignKey(related_name=b'entries', to='trex.Project'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='tags',
            field=models.ManyToManyField(related_name=b'entries', to='trex.Tag'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='entry',
            name='user',
            field=models.ForeignKey(related_name=b'entries', to='trex.ProjectUser'),
            preserve_default=True,
        ),
    ]
