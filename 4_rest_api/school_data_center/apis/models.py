from django.db import models


class Gender(models.TextChoices):
    """Gender choices shared by Teacher and Student."""
    MALE = 'M', 'Male'
    FEMALE = 'F', 'Female'
    OTHER = 'O', 'Other'


class School(models.Model):
    """A school (โรงเรียน)."""
    name = models.CharField(max_length=255)                 # ชื่อโรงเรียน
    abbreviation = models.CharField(max_length=50)          # ตัวย่อชื่อโรงเรียน
    address = models.TextField()                            # ที่อยู่

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Classroom(models.Model):
    """A classroom (ห้องเรียน) that belongs to a single school."""
    school = models.ForeignKey(
        School,
        on_delete=models.CASCADE,
        related_name='classrooms',
    )
    grade_level = models.PositiveSmallIntegerField()        # ชั้นปี
    section = models.PositiveSmallIntegerField()            # ทับ (ห้อง/section)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['school', 'grade_level', 'section']
        # A school cannot have two classrooms with the same grade/section.
        constraints = [
            models.UniqueConstraint(
                fields=['school', 'grade_level', 'section'],
                name='unique_classroom_per_school',
            )
        ]

    def __str__(self):
        return f'{self.grade_level}/{self.section} - {self.school.abbreviation}'


class Teacher(models.Model):
    """A teacher (ครู). A teacher can belong to many classrooms."""
    first_name = models.CharField(max_length=150)           # ชื่อ
    last_name = models.CharField(max_length=150)            # นามสกุล
    gender = models.CharField(max_length=1, choices=Gender.choices)  # เพศ

    # Many-to-many: a teacher can be in many classrooms and a classroom
    # can have many teachers.
    classrooms = models.ManyToManyField(
        Classroom,
        related_name='teachers',
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Student(models.Model):
    """A student (นักเรียน). A student belongs to exactly one classroom."""
    first_name = models.CharField(max_length=150)           # ชื่อ
    last_name = models.CharField(max_length=150)            # นามสกุล
    gender = models.CharField(max_length=1, choices=Gender.choices)  # เพศ

    # Many-to-one: a student is in a single classroom; a classroom can
    # have many students.
    classroom = models.ForeignKey(
        Classroom,
        on_delete=models.CASCADE,
        related_name='students',
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
