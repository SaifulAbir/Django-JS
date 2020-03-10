from django.core.exceptions import ValidationError
from django.test import TestCase

# Create your tests here.
from exam.models import Exam
from helpers import setup


class ExamTest(TestCase):

    def setUp(self):
        setup.subject(self)
        setup.topic(self)
        setup.sub_topic(self)
        setup.exam_category(self)
        setup.exam_level(self)

    def test__when_exam_code_is_null__should_raise_error(self):
        exam = Exam(exam_name='python', pass_mark='30', duration='10', exam_category = self.exam_category1, exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, instruction = "Instruction about exam", question_selection_type = 'auto',
                    exam_type = 'public', exam_fee = '0', promo_code = 'ishraak-offer', discount_price = '30', discount_percent = '40', re_registration_delay = '4')
        with self.assertRaises(ValidationError):
            exam.full_clean()

    def test__when_exam_code_is_blank__should_raise_error(self):
        exam = Exam(exam_code='', exam_name='python', pass_mark='30', duration='10', exam_category = self.exam_category1, exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, instruction = "Instruction about exam", question_selection_type = 'auto',
                    exam_type = 'public', exam_fee = '0', promo_code = 'ishraak-offer', discount_price = '30', discount_percent = '40', re_registration_delay = '4')
        with self.assertRaises(ValidationError):
            exam.full_clean()

    def test__max_length_validation_is__added_with_exam_code(self):
        max_length = Exam._meta.get_field('exam_code').max_length
        self.assertEquals(max_length, 50)

    def test__when_everything_is_given_for_exam___should_pass(self):
        exam = Exam(exam_code='ish-1010', exam_name='python', pass_mark='30', duration='10', exam_category=self.exam_category1,
                    exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, instruction="Instruction about exam", question_selection_type='auto',
                    exam_type='public', exam_fee='0', promo_code='ishraak-offer', discount_price='30',
                    discount_percent='40', re_registration_delay='4')
        try:
            exam.full_clean()
        except:
            self.fail()

    def test__when_exam_name_is_null__should_raise_error(self):
        exam = Exam(exam_code='ish-10', pass_mark='30', duration='10', exam_category = self.exam_category1, exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, instruction = "Instruction about exam", question_selection_type = 'auto',
                    exam_type = 'public', exam_fee = '50', promo_code = 'ishraak-offer', discount_price = '30', discount_percent = '40', re_registration_delay = '4')
        with self.assertRaises(ValidationError):
            exam.full_clean()

    def test__when_exam_name_is_blank__should_raise_error(self):
        exam = Exam(exam_code='ish-10', exam_name='', pass_mark='30', duration='10', exam_category = self.exam_category1, exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, instruction = "Instruction about exam", question_selection_type = 'auto',
                    exam_type = 'public', exam_fee = '0', promo_code = 'ishraak-offer', discount_price = '30', discount_percent = '40', re_registration_delay = '4')
        with self.assertRaises(ValidationError):
            exam.full_clean()

    def test__max_length_validation_is__added_with_exam_name(self):
        max_length = Exam._meta.get_field('exam_name').max_length
        self.assertEquals(max_length, 256)

    def test__when_pass_mark_is_null__should_raise_error(self):
        exam = Exam(exam_code='ish-10', exam_name='python', duration='10', exam_category = self.exam_category1, exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, instruction = "Instruction about exam", question_selection_type = 'auto',
                    exam_type = 'public', exam_fee = '0', promo_code = 'ishraak-offer', discount_price = '30', discount_percent = '40', re_registration_delay = '4')
        with self.assertRaises(ValidationError):
            exam.full_clean()

    def test__when_pass_mark_is_blank__should_raise_error(self):
        exam = Exam(exam_code='ish-10', exam_name='python', pass_mark='', duration='10', exam_category = self.exam_category1, exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, instruction = "Instruction about exam", question_selection_type = 'auto',
                    exam_type = 'public', exam_fee = '0', promo_code = 'ishraak-offer', discount_price = '30', discount_percent = '40', re_registration_delay = '4')
        with self.assertRaises(ValidationError):
            exam.full_clean()

    def test__max_length_validation_is__added_with_pass_mark(self):
        max_length = Exam._meta.get_field('pass_mark').max_length
        self.assertEquals(max_length, 200)

    def test__when_duration_is_null__should_raise_error(self):
        exam = Exam(exam_code='ish-10', exam_name='python', pass_mark='30', exam_category = self.exam_category1, exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, instruction = "Instruction about exam", question_selection_type = 'auto',
                    exam_type = 'public', exam_fee = '0', promo_code = 'ishraak-offer', discount_price = '30', discount_percent = '40', re_registration_delay = '4')
        with self.assertRaises(ValidationError):
            exam.full_clean()

    def test__when_duration_is_blank__should_raise_error(self):
        exam = Exam(exam_code='ish-10', exam_name='python', pass_mark='30', duration='', exam_category = self.exam_category1, exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, instruction = "Instruction about exam", question_selection_type = 'auto',
                    exam_type = 'public', exam_fee = '0', promo_code = 'ishraak-offer', discount_price = '30', discount_percent = '40', re_registration_delay = '4')
        with self.assertRaises(ValidationError):
            exam.full_clean()

    def test__max_length_validation_is__added_with_duration(self):
        max_length = Exam._meta.get_field('duration').max_length
        self.assertEquals(max_length, 100)

    def test__when_instruction_is_null__should_raise_error(self):
        exam = Exam(exam_code='ish-10', exam_name='python', pass_mark='30', duration='20', exam_category = self.exam_category1, exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, question_selection_type = 'auto',
                    exam_type = 'public', exam_fee = '0', promo_code = 'ishraak-offer', discount_price = '30', discount_percent = '40', re_registration_delay = '4')
        with self.assertRaises(ValidationError):
            exam.full_clean()

    def test__when_instruction_is_blank__should_raise_error(self):
        exam = Exam(exam_code='ish-10', exam_name='python', pass_mark='30', duration='20', exam_category = self.exam_category1, exam_level=self.exam_level1, subject=self.subject1, topic=self.topic1, sub_topic=self.subtopic1,
                    is_featured=False, instruction = "", question_selection_type = 'auto',
                    exam_type = 'public', exam_fee = '0', promo_code = 'ishraak-offer', discount_price = '30', discount_percent = '40', re_registration_delay = '4')
        with self.assertRaises(ValidationError):
            exam.full_clean()

