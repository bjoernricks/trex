# -*- coding: utf-8 -*-
#
# (c) 2014 Bjoern Ricks <bjoern.ricks@gmail.com>
#
# See LICENSE comming with the source of 'trex' for details.
#

from django.conf import settings
from django.core.urlresolvers import reverse_lazy
from django.db import models, transaction


class BaseQuerySet(models.QuerySet):
    use_for_related_fields = True

    def as_manager(cls, use_for_related_fields=None):
        # override method to allow setting use_for_related_fields

        if use_for_related_fields is None:
            use_for_related_fields = cls.use_for_related_fields

        manager_cls = models.manager.Manager.from_queryset(cls)
        manager_cls.use_for_related_fields = use_for_related_fields
        return manager_cls()
    as_manager.queryset_only = True
    as_manager = classmethod(as_manager)


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

    def create_entries_from_zeiterfassung(self, zeiterfassung):
        with transaction.atomic():
            read_count = 0
            for zentry in zeiterfassung.read():
                try:
                    user = ProjectUsers.objects.get(project=self,
                                                    user_abbr=zentry.get_user()
                                                    ).user
                except ProjectUsers.DoesNotExist:
                    user = None

                entry = Entry.objects.create(
                    project=self, date=zentry.get_date(),
                    duration=zentry.get_duration(), state=zentry.get_state(),
                    description=zentry.get_description(), user=user,
                    user_abbr=zentry.user
                )

                # raise ValueError(
                #     "Zeiterfassung entry %s has already been imported "
                #     "to the project %s" % (zentry, self.name))

                tag, created = Tag.objects.get_or_create(
                    project=self, name=zentry.get_workpackage()
                )
                entry.tags.add(tag)
                read_count += 1
            return read_count


class Entry(models.Model):

    project = models.ForeignKey(Project, related_name="entries")
    date = models.DateField()
    duration = models.PositiveIntegerField()
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    state = models.CharField(max_length="5", blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True)
    user_abbr = models.CharField("User abbreviation", max_length=25, blank=True,
                                 default="")
    tags = models.ManyToManyField("Tag", related_name="entries")

    class Meta:
        ordering = ("date", "created")

    def get_absolute_url(self):
        return reverse_lazy("entry-detail", kwargs={"pk": self.id})


class Tag(models.Model):

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
