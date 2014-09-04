from rest_framework import generics

from trex.models.project import Project
from trex.serializers import ProjectSerializer


class ProjectListCreateAPIView(generics.ListCreateAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectDetailAPIView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
