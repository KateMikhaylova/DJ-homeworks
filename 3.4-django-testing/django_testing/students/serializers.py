from rest_framework import serializers

from students.models import Course, Attendance

from django.conf import settings
from django.core.exceptions import ValidationError


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = ("id", "name", "students")


class AttendanceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = ('id', 'course', 'student')

    def validate(self, attrs):
        course = attrs['course']
        attendances = Attendance.objects.filter(course=course)
        if len(attendances) >= settings.MAX_STUDENTS_PER_COURSE:
            raise ValidationError(f'error: max {settings.MAX_STUDENTS_PER_COURSE} students per course')
        return attrs
