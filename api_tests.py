import unittest
import api
import flask

class testEvaApi(unittest.TestCase):
    def testGeneralSearch(self):
        self.assertEqual(len(api._generalSearch("Apollo 11")), 2)

    def testGetCrew(self):
        self.assertEqual(len(api._getCrew("Ed White")), 1)

    def testGetVehicle(self):
        self.assertEqual(len(api._getVehicle("Gemini XII")), 3)

    def testGetCountry(self):
        self.assertEqual(len(api._getCountry("Russia")), 139)

    def testDate(self):
        self.assertEqual(len(api._getDate("6/5/1966")), 1)

    def testDuration(self):
        self.assertEqual(len(api._getDuration("8:29")), 1)

    def testGetBetweenDurations(self):
        self.assertEqual(len(api._getBetweenDurations("0:00", "0:30")), 19)

    def testGetBetweenDates(self):
        self.assertEqual(len(api._getBetweenDates("6/1/1965", "6/1/1968")), 10)

if __name__ == '__main__':
    unittest.main()
