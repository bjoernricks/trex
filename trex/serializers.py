from rest_framework.serializers import HyperlinkedModelSerializer

from trex.models.project import Project


class ProjectSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = Project
        fields = ("url", "description", "active", "created")
        view_name = "project-details"
