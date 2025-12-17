from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Lesson, Course

@receiver(post_save, sender=Lesson)
@receiver(post_delete, sender=Lesson)
def update_lessons_count(sender, instance, **kwargs):
    course = instance.course
    course.lessons = course.course_lessons.count()
    course.save()
