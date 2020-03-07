from django.test import TestCase

# Create your tests here.
from helpers import setup
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from questionnaire.models import Questionnaire, QuestionnaireDetail


class QuestionnaireTest(TestCase):

    def setUp(self):
        setup.subject(self)
        setup.topic(self)
        setup.sub_topic(self)
        setup.questionnaire(self)

    def test__when_name_is_null__should_raise_error(self):
        s = Questionnaire(remarks='hi', subject = self.subject1, topic = self.topic1, sub_topic = self.subtopic1)
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test__when_name_is_blank__should_raise_error(self):
        s = Questionnaire(name='', remarks='hi',subject = self.subject1, topic = self.topic1, sub_topic = self.subtopic1)
        with self.assertRaises(ValidationError):
            s.full_clean()


    def test__when_questionnaire_name_is_duplicate__should_raise_error(self):
        s1 = Questionnaire( name='Machine Learning', remarks='hi',subject = self.subject1, topic = self.topic1, sub_topic = self.subtopic1)
        s2 = Questionnaire( name='Machine Learning', remarks='hi',subject = self.subject1, topic = self.topic1, sub_topic = self.subtopic1)
        with self.assertRaises(IntegrityError):
            s1.save()
            s2.save()

    def test__max_length_validation_is__added_for_name(self):
        max_length = Questionnaire._meta.get_field('name').max_length
        self.assertEquals(max_length, 255)

    def test__when_everything_is_given___should_pass(self):
        s = Questionnaire( name='Machine Learning', remarks='hi',subject = self.subject1, topic = self.topic1, sub_topic = self.subtopic1)
        try:
            s.full_clean()
        except:
            self.fail()

    def test__when_Remarks_is_null___should_pass(self):
        s = Questionnaire( name='Machine Learning',subject = self.subject1, topic = self.topic1, sub_topic = self.subtopic1)
        try:
            s.full_clean()
        except:
            self.fail()

    def test__when_subject_is_null___should_pass(self):
        s = Questionnaire( name='Machine Learning',remarks='hi', topic = self.topic1, sub_topic = self.subtopic1)
        try:
            s.full_clean()
        except:
            self.fail()

    def test__when_topic_is_null___should_pass(self):
        s = Questionnaire( name='Machine Learning',subject = self.subject1, remarks = 'hi', sub_topic = self.subtopic1)
        try:
            s.full_clean()
        except:
            self.fail()

    def test__when_sub_topic_is_null___should_pass(self):
        s = Questionnaire( name='Machine Learning',subject = self.subject1, topic = self.topic1, remarks = 'hi')
        try:
            s.full_clean()
        except:
            self.fail()

    def test__when_Remarks_is_blank___should_pass(self):
        s = Questionnaire( name='Machine Learning', remarks='',subject = self.subject1, topic = self.topic1, sub_topic = self.subtopic1)
        try:
            s.full_clean()
        except:
            self.fail()


class QuestionnairieDetailTest(TestCase):
    def setUp(self):
        setup.subject(self)
        setup.topic(self)
        setup.sub_topic(self)
        setup.qtype(self)
        setup.difficulty(self)
        setup.question(self)
        setup.questionnaire(self)


    def test__when_everything_is_given___should_pass(self):
        s = QuestionnaireDetail(questionnaire_id=self.questionnaire1, question_id=self.question1)
        try:
            s.full_clean()
        except:
            self.fail()

    def test__when_questionnaire_id_is_null__should_raise_error(self):
        s = QuestionnaireDetail(question_id=self.question1,)
        with self.assertRaises(ValidationError):
            s.full_clean()

    def test__when_question_id_is_null__should_raise_error(self):
        s = QuestionnaireDetail(questionnaire_id=self.questionnaire1,)
        with self.assertRaises(ValidationError):
            s.full_clean()
