import pytest
from model_bakery import baker
from rest_framework.test import APIClient
from django.urls import reverse
from students.models import Course, Student


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
def test_get_courses_list(client, course_factory):
    courses = course_factory(_quantity=10)

    url = reverse('courses-list')
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)


@pytest.mark.django_db
def test_get_one_course(client, course_factory):
    courses = course_factory(_quantity=10)
    first_course = courses[0]

    url = reverse('courses-detail', args=[first_course.id])
    response = client.get(url)

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == first_course.name


@pytest.mark.django_db
def test_get_id_filter_course(client, course_factory):
    courses = course_factory(_quantity=10)
    first_course = courses[0]

    url = reverse('courses-list')
    response = client.get(url, {'id': first_course.id})

    assert response.status_code == 200
    data = response.json()
    assert data[0]['id'] == first_course.id


@pytest.mark.django_db
def test_get_filter_course(client, course_factory):
    courses = course_factory(_quantity=10)
    first_course = courses[0]

    url = reverse('courses-list')
    response = client.get(url, {'name': first_course.name})

    assert response.status_code == 200
    data = response.json()
    assert data[0]['name'] == first_course.name


@pytest.mark.django_db
def test_create_course(client):
    url = reverse('courses-list')
    data = {'name': 'some course', 'srudents': []}
    response = client.post(url, data)

    assert response.status_code == 201
    data = response.json()
    assert Course.objects.get(id=data['id']).name == 'some course'


@pytest.mark.django_db
def test_update_course(client, course_factory):
    courses = course_factory(_quantity=10)
    update_course = Course.objects.first()

    url = reverse('courses-detail', args=[update_course.id])
    data = {'name': 'some course'}
    response = client.patch(url, data)

    assert response.status_code == 200
    data = response.json()
    assert data['name'] == 'some course'


@pytest.mark.django_db
def test_delete_course(client, course_factory):
    course_factory(_quantity=5)
    update_course = Course.objects.first()

    url = reverse('courses-detail', args=(update_course.id,))
    response = client.delete(url)

    assert response.status_code == 204
