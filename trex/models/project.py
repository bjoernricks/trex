# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models


class Project(models.Model):

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True, default="")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(
        settings.AUTH_USER_MODEL, through="ProjectUsers",
        related_name="projects")

    class Meta:
        ordering = ("name", "active")

    def get_absolute_url(self):
        return reverse_lazy("project-detail", kwargs={"pk": self.id})


class Entry(models.Model):

    project = models.ForeignKey(Project, related_name="entries")
    date = models.DateField()
    duration = models.PositiveIntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length="5", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    tags = models.ManyToManyField("Tags", related_name="entries")

    class Meta:
        ordering = ("date", "created")


class Tags(models.Model):

    project = models.ForeignKey(Project, related_name="tags")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, default="")
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ("name",)


class ProjectUsers(models.Model):

    project = models.ForeignKey(Project)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    user_abbr = models.CharField("User abbreviation for the project",
                                 max_length=25)

    class Meta:
        unique_together = ("project", "user")
