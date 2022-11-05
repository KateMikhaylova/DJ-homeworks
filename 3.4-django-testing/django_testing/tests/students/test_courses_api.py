import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course
from django.urls import reverse
from django.conf import settings


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory


@pytest.mark.django_db
def test_get_course(client, course_factory):
    course = course_factory(_quantity=1)
    course_id = course[0].id
    url = reverse('courses-detail', args=[course_id])
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert data['id'] == course_id


@pytest.mark.django_db
def test_get_courses(client, course_factory):
    course = course_factory(_quantity=10)
    url = reverse('courses-list')
    response = client.get(url)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(course)
    for i, c in enumerate(data):
        assert c['id'] == course[i].id


@pytest.mark.django_db
def test_get_filtered_courses_id(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    for course in courses:
        filter_data = {'id': str(course.id)}
        response = client.get(url, filter_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['id'] == course.id
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_get_filtered_courses_name(client, course_factory):
    courses = course_factory(_quantity=10)
    url = reverse('courses-list')
    for course in courses:
        filter_data = {'name': course.name}
        response = client.get(url, filter_data)
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]['id'] == course.id
        assert data[0]['name'] == course.name


@pytest.mark.django_db
def test_create_course(client):
    new_course_name = 'Python'
    data = {'name': new_course_name}
    url = reverse('courses-list')
    response = client.post(url, data=data)
    assert response.status_code == 201
    reply = response.json()
    assert reply['name'] == new_course_name


@pytest.mark.django_db
def test_amend_course(client, course_factory):
    course = course_factory(_quantity=1)
    amended_course_name = 'C++'
    data = {'name': amended_course_name}
    course_id = course[0].id
    patch_url = reverse('courses-detail', args=[course_id])
    response = client.patch(patch_url, data=data)
    reply = response.json()
    assert response.status_code == 200
    assert reply['id'] == course_id
    assert reply['name'] == amended_course_name


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course = course_factory(_quantity=1)
    course_id = course[0].id
    delete_url = reverse('courses-detail', args=[course_id])
    response = client.delete(delete_url)
    assert response.status_code == 204
    course = Course.objects.filter(id=course_id)
    assert len(course) == 0


@pytest.fixture
def test_with_specific_settings(settings):
    settings.MAX_STUDENTS_PER_COURSE = 3
    assert settings.MAX_STUDENTS_PER_COURSE


@pytest.mark.parametrize(['students_quantity', 'response_status_codes'],
                         ((1, [201]),
                          (3, [201, 201, 201]),
                          (5, [201, 201, 201, 400, 400])))
@pytest.mark.django_db
def test_validate_students_quantity(client, course_factory, student_factory,
                                    test_with_specific_settings, students_quantity, response_status_codes):
    course = course_factory(_quantity=1)
    students = student_factory(_quantity=students_quantity)
    url = reverse('attendances-list')
    status_codes = []
    for student in students:
        response = client.post(url, data={'course': course[0].id, 'student': student.id})
        status_codes.append(response.status_code)
    assert status_codes == response_status_codes
