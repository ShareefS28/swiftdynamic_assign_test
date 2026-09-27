from django_filters import rest_framework as filters

from .models import School, Classroom, Teacher, Student


class SchoolFilter(filters.FilterSet):
    """Filter schools by name (case-insensitive partial match)."""
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = School
        fields = ['name']


class ClassroomFilter(filters.FilterSet):
    """Filter classrooms by school."""

    class Meta:
        model = Classroom
        fields = ['school']


class TeacherFilter(filters.FilterSet):
    """Filter teachers by school, classroom, name and gender.

    Teachers have no direct School FK, so 'school' is resolved through the
    many-to-many classroom relationship.
    """
    school = filters.NumberFilter(field_name='classrooms__school', distinct=True)
    classroom = filters.NumberFilter(field_name='classrooms', distinct=True)
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = Teacher
        fields = ['school', 'classroom', 'first_name', 'last_name', 'gender']


class StudentFilter(filters.FilterSet):
    """Filter students by school, classroom, name and gender.

    Students reach School through their single classroom.
    """
    school = filters.NumberFilter(field_name='classroom__school')
    first_name = filters.CharFilter(field_name='first_name', lookup_expr='icontains')
    last_name = filters.CharFilter(field_name='last_name', lookup_expr='icontains')

    class Meta:
        model = Student
        fields = ['school', 'classroom', 'first_name', 'last_name', 'gender']
