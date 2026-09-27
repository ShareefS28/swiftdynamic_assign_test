from rest_framework import serializers

from .models import School, Classroom, Teacher, Student


# ---------------------------------------------------------------------------
# Lightweight nested serializers (used inside detail responses)
# ---------------------------------------------------------------------------

class TeacherNestedSerializer(serializers.ModelSerializer):
    """Compact teacher representation for nesting in classroom detail."""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'full_name', 'gender')

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class StudentNestedSerializer(serializers.ModelSerializer):
    """Compact student representation for nesting in classroom detail."""
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'full_name', 'gender')

    def get_full_name(self, obj):
        return f'{obj.first_name} {obj.last_name}'


class ClassroomNestedSerializer(serializers.ModelSerializer):
    """Compact classroom representation for nesting in teacher/student detail."""
    school_name = serializers.CharField(source='school.name', read_only=True)

    class Meta:
        model = Classroom
        fields = ('id', 'school', 'school_name', 'grade_level', 'section')


# ---------------------------------------------------------------------------
# School serializers
# ---------------------------------------------------------------------------

class SchoolSerializer(serializers.ModelSerializer):
    """Used for create / update / list."""

    class Meta:
        model = School
        fields = ('id', 'name', 'abbreviation', 'address')


class SchoolDetailSerializer(serializers.ModelSerializer):
    """Detail view exposes aggregate counts."""
    classroom_count = serializers.SerializerMethodField()
    teacher_count = serializers.SerializerMethodField()
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = School
        fields = (
            'id', 'name', 'abbreviation', 'address',
            'classroom_count', 'teacher_count', 'student_count',
        )

    def get_classroom_count(self, obj):
        return obj.classrooms.count()

    def get_teacher_count(self, obj):
        # Distinct teachers across all classrooms of this school.
        return Teacher.objects.filter(classrooms__school=obj).distinct().count()

    def get_student_count(self, obj):
        return Student.objects.filter(classroom__school=obj).count()


# ---------------------------------------------------------------------------
# Classroom serializers
# ---------------------------------------------------------------------------

class ClassroomSerializer(serializers.ModelSerializer):
    """Used for create / update / list."""

    class Meta:
        model = Classroom
        fields = ('id', 'school', 'grade_level', 'section')


class ClassroomDetailSerializer(serializers.ModelSerializer):
    """Detail view exposes nested teachers and students."""
    school_name = serializers.CharField(source='school.name', read_only=True)
    teachers = TeacherNestedSerializer(many=True, read_only=True)
    students = StudentNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Classroom
        fields = (
            'id', 'school', 'school_name', 'grade_level', 'section',
            'teachers', 'students',
        )


# ---------------------------------------------------------------------------
# Teacher serializers
# ---------------------------------------------------------------------------

class TeacherSerializer(serializers.ModelSerializer):
    """Used for create / update / list."""

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'gender', 'classrooms')


class TeacherDetailSerializer(serializers.ModelSerializer):
    """Detail view exposes the nested list of classrooms."""
    classrooms = ClassroomNestedSerializer(many=True, read_only=True)

    class Meta:
        model = Teacher
        fields = ('id', 'first_name', 'last_name', 'gender', 'classrooms')


# ---------------------------------------------------------------------------
# Student serializers
# ---------------------------------------------------------------------------

class StudentSerializer(serializers.ModelSerializer):
    """Used for create / update / list."""

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'gender', 'classroom')


class StudentDetailSerializer(serializers.ModelSerializer):
    """Detail view exposes the nested classroom object."""
    classroom = ClassroomNestedSerializer(read_only=True)

    class Meta:
        model = Student
        fields = ('id', 'first_name', 'last_name', 'gender', 'classroom')
