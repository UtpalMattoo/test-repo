import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime
import sys
import os

# Add the server directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from app import app, db
from models.adoption_application import AdoptionApplication
from models.dog import Dog


class TestAdoptionApplications(unittest.TestCase):
    """Test cases for adoption application endpoints."""
    
    def setUp(self):
        """Set up test client and mock database."""
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
    @patch('app.db.session')
    @patch('app.AdoptionApplication')
    @patch('app.Dog')
    def test_post_adoption_application_success(self, mock_dog, mock_application, mock_session):
        """Test successful adoption application submission."""
        # Mock dog exists and is available
        mock_dog_instance = MagicMock()
        mock_dog_instance.id = 1
        mock_dog_instance.status = 'available'
        mock_dog.query.get.return_value = mock_dog_instance
        
        # Mock no existing application
        mock_application.query.filter_by.return_value.first.return_value = None
        
        # Mock successful application creation
        mock_new_application = MagicMock()
        mock_new_application.id = 42
        mock_application.return_value = mock_new_application
        
        test_data = {
            'applicant_name': 'John Doe',
            'applicant_email': 'john.doe@example.com', 
            'applicant_phone': '(555) 123-4567'
        }
        
        response = self.client.post('/api/dogs/1/applications',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        # This test should FAIL initially (endpoint doesn't exist yet)
        self.assertEqual(response.status_code, 201)
        response_data = json.loads(response.data)
        self.assertEqual(response_data['message'], 'submission accepted')
        self.assertEqual(response_data['application_id'], 42)
        
    @patch('app.db.session')
    @patch('app.AdoptionApplication')
    @patch('app.Dog')
    def test_post_adoption_application_duplicate(self, mock_dog, mock_application, mock_session):
        """Test application submission when dog already has application."""
        # Mock dog exists
        mock_dog_instance = MagicMock()
        mock_dog_instance.id = 1
        mock_dog.query.get.return_value = mock_dog_instance
        
        # Mock existing application
        mock_existing_app = MagicMock()
        mock_application.query.filter_by.return_value.first.return_value = mock_existing_app
        
        test_data = {
            'applicant_name': 'Jane Smith',
            'applicant_email': 'jane@example.com',
            'applicant_phone': '555-123-4567'
        }
        
        response = self.client.post('/api/dogs/1/applications',
                                  data=json.dumps(test_data),
                                  content_type='application/json')
        
        # This test should FAIL initially (endpoint doesn't exist yet)
        self.assertEqual(response.status_code, 400)
        response_data = json.loads(response.data)
        self.assertIn('already has an application', response_data['error'])
        
    @patch('app.db.session')
    @patch('app.AdoptionApplication')
    def test_get_applications_success(self, mock_application, mock_session):
        """Test successful retrieval of all applications."""
        # Mock applications data
        mock_app1 = MagicMock()
        mock_app1.to_dict.return_value = {
            'id': 1,
            'dog_id': 1,
            'applicant_name': 'John Doe',
            'applicant_email': 'john@example.com',
            'applicant_phone': '(555) 123-4567',
            'submission_timestamp': '2025-10-09T10:00:00',
            'application_status': 'PENDING'
        }
        
        mock_app2 = MagicMock()
        mock_app2.to_dict.return_value = {
            'id': 2,
            'dog_id': 2,
            'applicant_name': 'Jane Smith',
            'applicant_email': 'jane@example.com',
            'applicant_phone': '555-123-4567',
            'submission_timestamp': '2025-10-09T11:00:00',
            'application_status': 'PENDING'
        }
        
        mock_application.query.all.return_value = [mock_app1, mock_app2]
        
        response = self.client.get('/api/applications')
        
        # This test should FAIL initially (endpoint doesn't exist yet)
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertEqual(len(response_data), 2)
        self.assertEqual(response_data[0]['applicant_name'], 'John Doe')
        self.assertEqual(response_data[1]['applicant_name'], 'Jane Smith')


    @patch('app.db.session')
    def test_adoption_application_model_validation(self, mock_session):
        """Test AdoptionApplication model validation."""
        from models.adoption_application import AdoptionApplication
        
        # Test valid application
        valid_app = AdoptionApplication(
            dog_id=1,
            applicant_name="John Doe",
            applicant_email="john@example.com",
            applicant_phone="(555) 123-4567"
        )
        
        self.assertEqual(valid_app.dog_id, 1)
        self.assertEqual(valid_app.applicant_name, "John Doe")
        self.assertEqual(valid_app.applicant_email, "john@example.com")
        self.assertEqual(valid_app.applicant_phone, "(555) 123-4567")
        self.assertEqual(valid_app.application_status, "PENDING")
        
        # Test to_dict method
        app_dict = valid_app.to_dict()
        self.assertIn('id', app_dict)
        self.assertIn('dog_id', app_dict)
        self.assertIn('applicant_name', app_dict)
        self.assertIn('applicant_email', app_dict)
        self.assertIn('applicant_phone', app_dict)
        self.assertIn('application_status', app_dict)
        
        # Test __repr__ method
        repr_str = repr(valid_app)
        self.assertIn('AdoptionApplication', repr_str)
        self.assertIn('Dog 1', repr_str)


if __name__ == '__main__':
    unittest.main()