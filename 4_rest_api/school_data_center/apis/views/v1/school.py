from rest_framework import viewsets

from apis.models import School
from apis.serializers import SchoolSerializer, SchoolDetailSerializer
from apis.filters import SchoolFilter


class SchoolViewSet(viewsets.ModelViewSet):
    """CRUD for schools.

    - list:     filterable by `name`
    - retrieve: includes classroom/teacher/student counts
    """
    queryset = School.objects.all()
    filterset_class = SchoolFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SchoolDetailSerializer
        return SchoolSerializer
