import time
import unittest
import pandas as pd

from selenium import webdriver

from test_ui.test_careeradvice import addCareeradvice
from test_ui.test_currency import *
from test_ui.test_difficulty import *
from test_ui.test_exam import *
from test_ui.test_exam_category import *
from test_ui.test_exam_level import *
from test_ui.test_gender import *
from test_ui.test_industry import *
from test_ui.test_job_type import *
from test_ui.test_professional import *
from test_ui.test_qtype import *
from test_ui.test_qualification import *
from test_ui.test_question import *
from test_ui.test_questionnaire import *
from test_ui.test_sign_up import *
from test_ui.test_skill import *
from test_ui.test_sub_topic import *
from test_ui.test_subject import *
from test_ui.test_testimonial import addTestimonial
from test_ui.test_topic import *
from test_ui.test_trendingkeyword import addTrendingkeyword
from .test_district import *
from .test_division import *
from .test_job_post import *
from .test_company import *
from .test_login import *
from .test_experience import *
from .config import *



class TestUI(unittest.TestCase):

    # def setUpClass():
    #     print("Data Entry started ..")
    #     TestUI.dataEntry()


    def setUp(self):
        print("Setup function is running")
        self.driver = webdriver.Chrome(CHROME_DRIVER_LOCATION)
        self.driver.get(MAIN_URL)
        time.sleep(DELAY_SHORT)

    def dataEntry():
        driver = webdriver.Chrome(CHROME_DRIVER_LOCATION)
        adminLogin(driver, {'_email': 'admin', '_password': '@dmin123#', 'name': 'admin'})
        IndEntry = pd.read_csv("test_ui/data/data_industry.csv", dtype=str)
        JTypEntry = pd.read_csv("test_ui/data/data_job_type.csv", dtype=str)
        ExpEntry = pd.read_csv("test_ui/data/data_experience.csv", dtype=str)
        CurrEntry = pd.read_csv("test_ui/data/data_currency.csv", dtype=str)
        GendEntry = pd.read_csv("test_ui/data/data_gender.csv", dtype=str)
        QualiEntry = pd.read_csv("test_ui/data/data_qualification.csv", dtype=str)
        DivEntry = pd.read_csv("test_ui/data/data_division.csv", dtype=str)
        DisEntry = pd.read_csv("test_ui/data/data_district.csv", dtype=str)
        CompEntry = pd.read_csv("test_ui/data/data_company.csv", dtype=str)

        QtypeEntry = pd.read_csv("test_ui/data/data_qtype.csv", dtype=str)
        DiffEntry = pd.read_csv("test_ui/data/data_difficulty.csv", dtype=str)
        SubjectEntry = pd.read_csv("test_ui/data/data_subject.csv", dtype=str)
        TopicEntry = pd.read_csv("test_ui/data/data_topic.csv", dtype=str)
        SubTopicEntry = pd.read_csv("test_ui/data/data_sub_topic.csv", dtype=str)
        QEntry = pd.read_csv("test_ui/data/data_question.csv", dtype=str)
        QnaireEntry = pd.read_csv("test_ui/data/data_questionnaire.csv", dtype=str)
        ExamCatEntry = pd.read_csv("test_ui/data/data_exam_category.csv", dtype=str)
        ExamLevelEntry = pd.read_csv("test_ui/data/data_exam_level.csv", dtype=str)
        ExamEntry = pd.read_csv("test_ui/data/data_exam.csv", dtype=str)
        SkillEntry = pd.read_csv("test_ui/data/data_skill.csv", dtype=str)
        TrendingkeywordEntry = pd.read_csv("test_ui/data/data_trendingkeyword.csv", dtype=str)


        f = 1
        for idx, row in IndEntry.iterrows():
            driver.get(ADMIN_URL + INDUSTRY_URL)
            actual1 = addIndustry(driver, row)
        for idx, row in JTypEntry.iterrows():
            driver.get(ADMIN_URL + JOB_TYPE_URL)
            actual2 = addJobType(driver, row)
        for idx, row in ExpEntry.iterrows():
            driver.get(ADMIN_URL + EXPERIENCE_URL)
            actual3 = addExperience(driver, row)
        for idx, row in CurrEntry.iterrows():
            driver.get(ADMIN_URL + CURRENCY_URL)
            actual4 = addCurrency(driver, row)
        for idx, row in GendEntry.iterrows():
            driver.get(ADMIN_URL + GENDER_URL)
            actual5 = addGender(driver, row)
        for idx, row in QualiEntry.iterrows():
            driver.get(ADMIN_URL + QUALIFICATION_URL)
            actual6 = addQualification(driver, row)
        for idx, row in DivEntry.iterrows():
            actual7 = addDivision(driver, row)
        for idx, row in DisEntry.iterrows():
            actual8 = addDistrict(driver, row)
        for idx, row in CompEntry.iterrows():
            driver.get(ADMIN_URL + COMPANY_URL)
            actual9 = addCompany(driver, row)

        for idx, row in QtypeEntry.iterrows():
            driver.get(ADMIN_URL + QTYPE_URL)
            actual10 = addQtype(driver, row)
        for idx, row in DiffEntry.iterrows():
            driver.get(ADMIN_URL + DIFFICULTY_URL)
            actual11 = addDifficulty(driver, row)
        for idx, row in SubjectEntry.iterrows():
            driver.get(ADMIN_URL + SUBJECT_URL)
            actual12 = addSubject(driver, row)
        for idx, row in TopicEntry.iterrows():
            driver.get(ADMIN_URL + TOPIC_URL)
            actual13 = addTopic(driver, row)
        for idx, row in SubTopicEntry.iterrows():
            driver.get(ADMIN_URL + SUB_TOPIC_URL)
            actual14 = addSubTopic(driver, row)
        for idx, row in QEntry.iterrows():
            driver.get(ADMIN_URL + QUESTION_URL)
            actual15 = addQuestion(driver, row)
        for idx, row in QnaireEntry.iterrows():
            driver.get(ADMIN_URL + QUESTIONNAIRE_URL)
            actual16 = addQuestionnaire(driver, row)
        for idx, row in ExamCatEntry.iterrows():
            driver.get(ADMIN_URL + EXAM_CATEGORY_URL)
            actual17 = addExamCategory(driver, row)
        for idx, row in ExamLevelEntry.iterrows():
            driver.get(ADMIN_URL + EXAM_LEVEL_URL)
            actual18= addExamLevel(driver, row)
        for idx, row in SkillEntry.iterrows():
             actual18 = addSkill(driver, row)
        for idx, row in TrendingkeywordEntry.iterrows():
            driver.get(ADMIN_URL + TRENDINGKEYWORD_URL)
            actual18 = addTrendingkeyword(driver, row)
        # # for idx, row in ExamEntry.iterrows():
        # #     driver.get(ADMIN_URL + EXAM_URL)
        # #     actual19 = addExam(driver, row)
        #
        #
            # try:
            #     if actual1==actual2==actual3==actual4==actual5==actual6==actual7==actual8==actual9==actual10==actual11==actual12==actual13==actual14==actual15==actual16==actual17==actual18:
            #         print("Data Entry succeeded")
            #     else:
            #         print("Error In Data Entry")
            #
            # except Exception as ex:
            #     print("Error In Data Entry")


    def testSignUp(self):
        data = pd.read_csv("test_ui/testdata/sign_up_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.fullscreen_window()
            self.driver.get(MAIN_URL)
            actual = addSignUp(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testLogin(self):
        data = pd.read_csv("test_ui/testdata/login.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(MAIN_URL)
            actual = login(self.driver, row)
            time.sleep(1)
            try:

                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row[
                        'test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
            if actual == 1:
                logout(self.driver)
                self.driver.get(MAIN_URL)
                time.sleep(1)
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")
    # def setUpClass():
    #     print("Data Entry started ..")
    #     TestUI.dataEntry()

    def testLoginAdmin(self):
        data = pd.read_csv("test_ui/testdata/admin_login.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL)
            actual = adminLogin(self.driver, row)
            time.sleep(1)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row[
                        'test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
            if actual == 1:
                adminLogout(self.driver)
                self.driver.get(ADMIN_URL)
                time.sleep(1)
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testIndustry(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/industry_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + INDUSTRY_URL)
            actual = addIndustry(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row[
                        'test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testJobType(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/job_type_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + JOB_TYPE_URL)
            actual = addJobType(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row[
                        'test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testExperience(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/experience_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + EXPERIENCE_URL)
            actual = addExperience(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testCurrency(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', 'name': 'admin'})
        data = pd.read_csv("test_ui/testdata/currency_add.csv", dtype=str)
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL+CURRENCY_URL)
            actual = addCurrency(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testGender(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/gender_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + GENDER_URL)
            actual = addGender(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row['test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testQualification(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/qualification_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + QUALIFICATION_URL)
            actual = addQualification(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row[
                        'test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testDivision(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', 'name': 'admin'})
        data = pd.read_csv("test_ui/testdata/division_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            actual = addDivision(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testDistrict(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', 'name': 'admin'})
        data = pd.read_csv("test_ui/testdata/district_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            actual = addDistrict(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    # def testCompany(self):
    #     adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', 'name': 'admin'})
    #     data = pd.read_csv("test_ui/data/basis_company.csv", dtype=str)
    #     for idx, row in data.iterrows():
    #         self.driver.get(ADMIN_URL+COMPANY_URL)
    #         actual = addCompany(self.driver, row)
    #         try:
    #             self.assertEqual(row['expected_result'], str(actual))
    #         except Exception as ex:
    #
    #             print(ex)

    def testJobHome(self):
        login(self.driver, {'_email': 'tanvir@ishraak.com', '_password': '@dmin123#45678a', 'name': 'admin'})
        data = pd.read_csv("test_ui/testdata/job_post_add.csv", dtype=str)
        for idx, row in data.iterrows():
            self.driver.get(MAIN_URL)
            actual = addJobHome(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
            except Exception as ex:

                print(ex)

    def testJobAdmin(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', 'name': 'admin'})
        data = pd.read_csv("test_ui/data/bdjobs_detail_list.csv", dtype=str)
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + ADMIN_JOB_POST_URL)
            actual = addJobAdmin(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
            except Exception as ex:

                print(ex)

    def testProfessional(self):
        adminLogin(self.driver, {'_email': 'tanvir@ishraak.com', '_password': '@dmin123#45678a', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/professional_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + PROFESSIONAL_URL)
            actual = addProfessional(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row['test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testQtype(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/qtype_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + QTYPE_URL)
            actual = addQtype(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testDifficulty(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/difficulty_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + DIFFICULTY_URL)
            actual = addDifficulty(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testSubject(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/subject_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + SUBJECT_URL)
            actual = addSubject(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row['test_description'])
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testTopic(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/topic_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + TOPIC_URL)
            actual = addTopic(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testSubTopic(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/sub_topic_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + SUB_TOPIC_URL)
            actual = addSubTopic(self.driver, row)
            try:
                # data['actual_result'] = actual
                # data['execution_time'] = now()
                # data['status'] = (row['expected_result'] == str(actual))
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testQuestion(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/question_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + QUESTION_URL)
            actual = addQuestion(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row['test_description'])
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testQuestionnaire(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/questionnaire_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + QUESTIONNAIRE_URL)
            actual = addQuestionnaire(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row['test_description'])
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testExamCategory(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/exam_category_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + EXAM_CATEGORY_URL)
            actual = addExamCategory(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row['test_description'])
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testExamLevel(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/exam_level_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + EXAM_LEVEL_URL)
            actual = addExamLevel(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row['test_description'])
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testSkill(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', 'name': 'admin'})
        data = pd.read_csv("test_ui/testdata/skill_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            actual = addSkill(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testTrendingkeyword(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/trendingkeyword_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + TRENDINGKEYWORD_URL)
            actual = addTrendingkeyword(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testTestimonial(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/testimonial_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + TESTIMONIAL_URL)
            actual = addTestimonial(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testCareeradvice(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/careeradvice_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + CAREERADVICE_URL)
            actual = addCareeradvice(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(
                    row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row[
                    'test_description'])
                print(ex)
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    def testExam(self):
        adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
        data = pd.read_csv("test_ui/testdata/exam_add.csv", dtype=str)
        f = 0
        for idx, row in data.iterrows():
            self.driver.get(ADMIN_URL + EXAM_URL)
            actual = addExam(self.driver, row)
            try:
                self.assertEqual(row['expected_result'], str(actual))
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
            except Exception as ex:
                print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row['test_description'])
                f = f + 1
        if f != 0:
            raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
        else:
            print("All passed")

    # def testExam(self):
    #     adminLogin(self.driver, {'_email': 'admin', '_password': '@dmin123#', '_name': 'Admin'})
    #     data = pd.read_csv("test_ui/testdata/exam_add.csv", dtype=str)
    #     f = 0
    #     for idx, row in data.iterrows():
    #         self.driver.get(ADMIN_URL + EXAM_URL)
    #         actual = addExam(self.driver, row)
    #         try:
    #             self.assertEqual(row['expected_result'], str(actual))
    #             print(row['test_case_id'] + " Expected " + row['expected_result'] + " Pass : " + row['test_description'])
    #         except Exception as ex:
    #             print(row['test_case_id'] + " Expected " + row['expected_result'] + " Failed : " + row['test_description'])
    #             f = f + 1
    #     if f != 0:
    #         raise Exception("Total pass: " + str(idx + 1 - f) + " and Failed: " + str(f))
    #     else:
    #         print("All passed")

if __name__ == '__main__':
    unittest.main()
