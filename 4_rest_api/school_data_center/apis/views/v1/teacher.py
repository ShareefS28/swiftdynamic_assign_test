from rest_framework import viewsets

from apis.models import Teacher
from apis.serializers import TeacherSerializer, TeacherDetailSerializer
from apis.filters import TeacherFilter


class TeacherViewSet(viewsets.ModelViewSet):
    """CRUD for teachers.

    - list:     filterable by `school`, `classroom`, `first_name`,
                `last_name`, `gender`
    - retrieve: includes nested list of classrooms
    """
    queryset = Teacher.objects.prefetch_related('classrooms__school').all()
    filterset_class = TeacherFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return TeacherDetailSerializer
        return TeacherSerializer
