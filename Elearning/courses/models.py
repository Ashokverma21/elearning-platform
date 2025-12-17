from django.db import models
from django.conf import settings
from django.utils import timezone

class Course(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()

    price = models.IntegerField(default=0)

    thumbnail = models.ImageField(upload_to='course_thumbnails/', null=True, blank=True)
    video = models.FileField(upload_to='course_videos/', null=True, blank=True)
    notes = models.FileField(upload_to="course_notes/", null=True, blank=True)
    notes_thumbnail = models.ImageField(upload_to="notes_thumbnails/", null=True, blank=True)
    instructor = models.CharField(max_length=150, default="Instructor")
    instructor_image = models.ImageField(upload_to="instructors/", null=True, blank=True)

    language = models.CharField(max_length=50, default="English")
    duration = models.CharField(max_length=50, default="Hours")
    lessons = models.IntegerField(default=0)

    def __str__(self):
        return self.title

from django.conf import settings
from django.utils import timezone

#Enrolled Courses

class EnrolledCourse(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(default=timezone.now)
    # optional: payment id / amount / status
    payment_id = models.CharField(max_length=200, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        unique_together = ('user', 'course')  # prevent duplicates

    def __str__(self):
        return f"{self.user.username} -> {self.course.title}"
    
    
#lesson

class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="course_lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to="lesson_videos/", null=True, blank=True)
    duration = models.CharField(max_length=20, default="10 min")

    def __str__(self):
        return self.title

from django.apps import AppConfig

class CoursesConfig(AppConfig):
    name = 'courses'

    def ready(self):
        import courses.signals


#lesson model
class Lesson(models.Model):
    course = models.ForeignKey(Course, related_name="course_lessons", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    video = models.FileField(upload_to="lesson_videos/", null=True, blank=True)
    duration = models.CharField(max_length=20, default="10 min")
    order = models.PositiveIntegerField(default=1)  # NEW

    def __str__(self):
        return self.title

#Progress model
class LessonProgress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)

    class Meta:
        unique_together = ('user', 'lesson')

#Discussion
class Discussion(models.Model):
    course = models.ForeignKey('Course', on_delete=models.CASCADE, related_name="course_discussions")
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE, related_name="lesson_discussions", null=True, blank=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q by {self.user.username}"
    
#Reply
class Reply(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="replies")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Reply by {self.user.username}"