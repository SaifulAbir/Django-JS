from unittest import TestCase
from unittest.mock import MagicMock
from registration import utils
from registration.service import Service

class ServiceTest(TestCase):
    def testGetCandidateList_whenValid_shouldReturnCandidateList(self):
        jsonData = {
            "registration": [
                {
                    "candidate_id": "234234",
                    "candidate_name": "Ha",
                    "exam_id": "1",
                    "exam_name": "Python",
                    "duration_in_minutes": "30",
                    "status": "1",
                    "created_date": "2019-07-22T17:04:02Z"
                },
                {
                    "candidate_id": "32423",
                    "candidate_name": "WW",
                    "exam_id": "1",
                    "exam_name": "GO",
                    "duration_in_minutes": "30",
                    "status": "1",
                    "created_date": "2019-07-22T17:04:02Z"
                }
            ]
        }
        utils.getCadidateListFromDb = MagicMock(return_value = jsonData)
        service = Service()
        data = service.getCadidateList()
        numberOfRow = len(data['registration'])
        actual = numberOfRow
        expected = 2
        self.assertEqual(expected, actual)

    def testGetCandidateListIndividual_whenValid_shouldReturnCandidateList(self):
        jsonDataIndividual = {
            "registration": [
                {
                    "candidate_id": "234234",
                    "candidate_name": "Ha",
                    "exam_id": "1",
                    "exam_name": "Python",
                    "duration_in_minutes": "30",
                    "status": "1",
                    "created_date": "2019-07-22T17:04:02Z"
                }
            ]
        }
        utils.getSingleCadidateDetailsFromDb = MagicMock(return_value=jsonDataIndividual)
        service = Service()
        data = service.getIndividualCadidate()
        numberOfRow = len(data['registration'])
        actual = numberOfRow
        expected = 1
        self.assertEqual(expected, actual)