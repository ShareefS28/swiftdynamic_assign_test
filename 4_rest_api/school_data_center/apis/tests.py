from django.urls import reverse as django_reverse
from rest_framework import status
from rest_framework.test import APITestCase

from apis.models import School, Classroom, Teacher, Student


def reverse(name, *args, **kwargs):
    """Reverse a router URL name within the 'v1' application namespace."""
    return django_reverse(f'v1:{name}', *args, **kwargs)


class SchoolAPITests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(
            name='Bangkok High School',
            abbreviation='BHS',
            address='123 Sukhumvit Rd',
        )

    def test_create_school(self):
        url = reverse('school-list')
        payload = {
            'name': 'Chiang Mai School',
            'abbreviation': 'CMS',
            'address': '456 Nimman Rd',
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(School.objects.count(), 2)

    def test_list_schools(self):
        url = reverse('school-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_filter_school_by_name(self):
        School.objects.create(name='Phuket School', abbreviation='PKS', address='9 Beach Rd')
        url = reverse('school-list')
        response = self.client.get(url, {'name': 'bangkok'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['abbreviation'], 'BHS')

    def test_school_detail_counts(self):
        classroom = Classroom.objects.create(school=self.school, grade_level=1, section=1)
        classroom2 = Classroom.objects.create(school=self.school, grade_level=2, section=1)
        teacher = Teacher.objects.create(first_name='Somchai', last_name='Jaidee', gender='M')
        teacher.classrooms.add(classroom, classroom2)
        Student.objects.create(first_name='Nong', last_name='A', gender='M', classroom=classroom)
        Student.objects.create(first_name='Nong', last_name='B', gender='F', classroom=classroom2)

        url = reverse('school-detail', args=[self.school.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['classroom_count'], 2)
        self.assertEqual(response.data['teacher_count'], 1)  # distinct
        self.assertEqual(response.data['student_count'], 2)

    def test_update_school(self):
        url = reverse('school-detail', args=[self.school.id])
        response = self.client.patch(url, {'name': 'Updated Name'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.school.refresh_from_db()
        self.assertEqual(self.school.name, 'Updated Name')

    def test_delete_school(self):
        url = reverse('school-detail', args=[self.school.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(School.objects.count(), 0)


class ClassroomAPITests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name='S1', abbreviation='S1', address='addr')
        self.other_school = School.objects.create(name='S2', abbreviation='S2', address='addr')
        self.classroom = Classroom.objects.create(school=self.school, grade_level=1, section=1)

    def test_create_classroom(self):
        url = reverse('classroom-list')
        payload = {'school': self.school.id, 'grade_level': 3, 'section': 2}
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Classroom.objects.count(), 2)

    def test_filter_classroom_by_school(self):
        Classroom.objects.create(school=self.other_school, grade_level=1, section=1)
        url = reverse('classroom-list')
        response = self.client.get(url, {'school': self.school.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)

    def test_classroom_detail_lists_teachers_and_students(self):
        teacher = Teacher.objects.create(first_name='T', last_name='One', gender='F')
        teacher.classrooms.add(self.classroom)
        Student.objects.create(first_name='St', last_name='One', gender='M', classroom=self.classroom)

        url = reverse('classroom-detail', args=[self.classroom.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['teachers']), 1)
        self.assertEqual(len(response.data['students']), 1)

    def test_update_and_delete_classroom(self):
        url = reverse('classroom-detail', args=[self.classroom.id])
        patch = self.client.patch(url, {'section': 5}, format='json')
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        self.classroom.refresh_from_db()
        self.assertEqual(self.classroom.section, 5)

        delete = self.client.delete(url)
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)


class TeacherAPITests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name='S1', abbreviation='S1', address='addr')
        self.classroom = Classroom.objects.create(school=self.school, grade_level=1, section=1)
        self.teacher = Teacher.objects.create(first_name='Somsak', last_name='Meesuk', gender='M')
        self.teacher.classrooms.add(self.classroom)

    def test_create_teacher_with_classrooms(self):
        url = reverse('teacher-list')
        payload = {
            'first_name': 'Malee', 'last_name': 'Rakdee', 'gender': 'F',
            'classrooms': [self.classroom.id],
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Teacher.objects.count(), 2)

    def test_filter_teacher_by_school(self):
        other_school = School.objects.create(name='S2', abbreviation='S2', address='a')
        other_room = Classroom.objects.create(school=other_school, grade_level=1, section=1)
        t2 = Teacher.objects.create(first_name='X', last_name='Y', gender='O')
        t2.classrooms.add(other_room)

        url = reverse('teacher-list')
        response = self.client.get(url, {'school': self.school.id})
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['first_name'], 'Somsak')

    def test_filter_teacher_by_classroom_name_gender(self):
        url = reverse('teacher-list')
        self.assertEqual(self.client.get(url, {'classroom': self.classroom.id}).data['count'], 1)
        self.assertEqual(self.client.get(url, {'first_name': 'som'}).data['count'], 1)
        self.assertEqual(self.client.get(url, {'last_name': 'mee'}).data['count'], 1)
        self.assertEqual(self.client.get(url, {'gender': 'M'}).data['count'], 1)
        self.assertEqual(self.client.get(url, {'gender': 'F'}).data['count'], 0)

    def test_teacher_detail_lists_classrooms(self):
        url = reverse('teacher-detail', args=[self.teacher.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['classrooms']), 1)
        self.assertEqual(response.data['classrooms'][0]['id'], self.classroom.id)

    def test_update_and_delete_teacher(self):
        url = reverse('teacher-detail', args=[self.teacher.id])
        patch = self.client.patch(url, {'last_name': 'Changed'}, format='json')
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        delete = self.client.delete(url)
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)


class StudentAPITests(APITestCase):
    def setUp(self):
        self.school = School.objects.create(name='S1', abbreviation='S1', address='addr')
        self.classroom = Classroom.objects.create(school=self.school, grade_level=1, section=1)
        self.student = Student.objects.create(
            first_name='Anan', last_name='Suksan', gender='M', classroom=self.classroom,
        )

    def test_create_student(self):
        url = reverse('student-list')
        payload = {
            'first_name': 'Ploy', 'last_name': 'Dee', 'gender': 'F',
            'classroom': self.classroom.id,
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Student.objects.count(), 2)

    def test_filter_student_by_school_classroom_name_gender(self):
        other_school = School.objects.create(name='S2', abbreviation='S2', address='a')
        other_room = Classroom.objects.create(school=other_school, grade_level=1, section=1)
        Student.objects.create(first_name='Z', last_name='W', gender='F', classroom=other_room)

        url = reverse('student-list')
        self.assertEqual(self.client.get(url, {'school': self.school.id}).data['count'], 1)
        self.assertEqual(self.client.get(url, {'classroom': self.classroom.id}).data['count'], 1)
        self.assertEqual(self.client.get(url, {'first_name': 'ana'}).data['count'], 1)
        self.assertEqual(self.client.get(url, {'last_name': 'suk'}).data['count'], 1)
        self.assertEqual(self.client.get(url, {'gender': 'M'}).data['count'], 1)

    def test_student_detail_shows_classroom(self):
        url = reverse('student-detail', args=[self.student.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['classroom']['id'], self.classroom.id)
        self.assertEqual(response.data['classroom']['school_name'], 'S1')

    def test_update_and_delete_student(self):
        url = reverse('student-detail', args=[self.student.id])
        patch = self.client.patch(url, {'first_name': 'Changed'}, format='json')
        self.assertEqual(patch.status_code, status.HTTP_200_OK)
        delete = self.client.delete(url)
        self.assertEqual(delete.status_code, status.HTTP_204_NO_CONTENT)
