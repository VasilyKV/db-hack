import random

from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist


def get_schoolkid(schoolkid_name):
    try:
        return Schoolkid.objects.get(full_name__contains=schoolkid_name)
    except MultipleObjectsReturned:
        raise MultipleObjectsReturned(
            'Найдено несколько ученикофф, уточните ФИО')
    except ObjectDoesNotExist:
        raise ObjectDoesNotExist('Ученик не найден')


def fix_marks(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    schoolkid_bad_marks = Mark.objects.filter(
        schoolkid=schoolkid, points__in=[1, 2, 3])
    for schoolkid_bad_mark in schoolkid_bad_marks:
        schoolkid_bad_mark.points = 5
        schoolkid_bad_mark.save()


def remove_chastisements(schoolkid_name):
    schoolkid = get_schoolkid(schoolkid_name)
    schoolkid_chastisement = Chastisement.objects.filter(
        schoolkid=schoolkid).delete()


def create_commendation(schoolkid_name, subject):
    compliments = [
        'Молодец!',
        'Отлично!',
        'Хорошо!',
        'Гораздо лучше, чем я ожидал!',
        'Ты меня приятно удивил!',
        'Великолепно!',
        'Прекрасно!',
        'Ты меня очень обрадовал!',
        'Именно этого я давно ждал от тебя!',
        'Сказано здорово – просто и ясно!',
        'Ты, как всегда, точен!',
        'Очень хороший ответ!',
        'Талантливо!',
        'Ты сегодня прыгнул выше головы!',
        'Я поражен!',
        'Уже существенно лучше!',
        'Потрясающе!',
        'Замечательно!',
        'Прекрасное начало!',
        'Так держать!',
        'Ты на верном пути!',
        'Здорово!',
        'Это как раз то, что нужно!',
        'Я тобой горжусь!',
        'С каждым разом у тебя получается всё лучше!',
        'Мы с тобой не зря поработали!',
        'Я вижу, как ты стараешься!',
        'Ты растешь над собой!',
        'Ты многое сделал, я это вижу!',
        'Теперь у тебя точно все получится!'
    ]
    schoolkid = get_schoolkid(schoolkid_name)
    lessons_schoolkid_subject = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject__title=subject
    ).order_by('-date')

    if not lessons_schoolkid_subject:
        print(
            f'Уроки ученика {schoolkid.full_name} по предмету {subject} не найдены')
        return
    for lesson_schoolkid_subject in lessons_schoolkid_subject:
        is_commendation_exist = Commendation.objects.filter(
            created=lesson_schoolkid_subject.date,
            schoolkid=schoolkid,
            subject=lesson_schoolkid_subject.subject,
            teacher=lesson_schoolkid_subject.teacher
        )
        if not is_commendation_exist:
            Commendation.objects.create(
                text=random.choice(compliments),
                created=lesson_schoolkid_subject.date,
                schoolkid=schoolkid,
                subject=lesson_schoolkid_subject.subject,
                teacher=lesson_schoolkid_subject.teacher
            )
            return
