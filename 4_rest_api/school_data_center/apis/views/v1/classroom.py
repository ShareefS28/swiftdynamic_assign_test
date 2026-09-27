from rest_framework import viewsets

from apis.models import Classroom
from apis.serializers import ClassroomSerializer, ClassroomDetailSerializer
from apis.filters import ClassroomFilter


class ClassroomViewSet(viewsets.ModelViewSet):
    """CRUD for classrooms.

    - list:     filterable by `school`
    - retrieve: includes nested teachers and students
    """
    queryset = Classroom.objects.select_related('school').all()
    filterset_class = ClassroomFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClassroomDetailSerializer
        return ClassroomSerializer
