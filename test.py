import unittest
from main import OCR

class test_OCR(unittest.TestCase):
    def test_id(self):
        file = "documents/PANCard3.jpeg"
        handler = OCR(file)
        outputs = handler.get_text("id")
        fields = ["name", "dob", "pan_number"]
        valid = {'pan_number': 'BLUPS4233F', 'name': 'AMAR SINGH', 'dob': '10/12/1983'}
        for output in outputs:
            for field in fields:
                self.assertIn(field, output)
                self.assertEqual(output[field], valid[field])

if __name__ == '__main__':
    unittest.main()
