from rest_framework import viewsets

from apis.models import Student
from apis.serializers import StudentSerializer, StudentDetailSerializer
from apis.filters import StudentFilter


class StudentViewSet(viewsets.ModelViewSet):
    """CRUD for students.

    - list:     filterable by `school`, `classroom`, `first_name`,
                `last_name`, `gender`
    - retrieve: includes the nested classroom
    """
    queryset = Student.objects.select_related('classroom__school').all()
    filterset_class = StudentFilter

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return StudentDetailSerializer
        return StudentSerializer
