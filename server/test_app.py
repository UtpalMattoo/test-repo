import unittest
from unittest.mock import patch, MagicMock
import json
from app import app  # Changed from relative import to absolute import

# filepath: server/test_app.py
class TestApp(unittest.TestCase):
    def setUp(self):
        # Create a test client using Flask's test client
        self.app = app.test_client()
        self.app.testing = True
        # Turn off database initialization for tests
        app.config['TESTING'] = True
        
    class SimpleDog:
        def __init__(self, id, name, breed, status='AVAILABLE'):
            self.id = id
            self.name = name
            self.breed = breed
            self.status = status

    def _create_mock_dog(self, dog_id, name, breed):
        """Helper method to create a mock dog with standard attributes"""
        dog = MagicMock(spec=['to_dict', 'id', 'name', 'breed'])
        dog.id = dog_id
        dog.name = name
        dog.breed = breed
        dog.to_dict.return_value = {'id': dog_id, 'name': name, 'breed': breed}
        return dog
        
    def _setup_query_mock(self, mock_query, dogs):
        """Helper method to configure the query mock"""
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.join.return_value = mock_query_instance
        mock_query_instance.all.return_value = dogs
        return mock_query_instance

    def _setup_paginate_mock(self, mock_query, dogs):
        """Helper to mock the paginate method for SQLAlchemy query."""
        mock_query_instance = MagicMock()
        mock_query.return_value = mock_query_instance
        mock_query_instance.join.return_value = mock_query_instance
        mock_query_instance.filter.return_value = mock_query_instance
        mock_query_instance.order_by.return_value = mock_query_instance

        # Mock the paginate result
        mock_paginate = MagicMock()
        mock_paginate.items = dogs
        mock_paginate.total = len(dogs)
        mock_paginate.pages = 1
        mock_query_instance.paginate.return_value = mock_paginate
        return mock_query_instance

    @patch('app.db.session.query')
    def test_get_dogs_success(self, mock_query):
        """Test successful retrieval of multiple dogs"""
        # Arrange
        dog1 = self.SimpleDog(1, "Buddy", "Labrador")
        dog2 = self.SimpleDog(2, "Max", "German Shepherd")
        mock_dogs = [dog1, dog2]

        self._setup_paginate_mock(mock_query, mock_dogs)

        # Act
        response = self.app.get('/api/dogs')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(len(data['dogs']), 2)
        self.assertEqual(data['dogs'][0]['id'], 1)
        self.assertEqual(data['dogs'][0]['name'], "Buddy")
        self.assertEqual(data['dogs'][0]['breed'], "Labrador")
        self.assertEqual(data['dogs'][1]['id'], 2)
        self.assertEqual(data['dogs'][1]['name'], "Max")
        self.assertEqual(data['dogs'][1]['breed'], "German Shepherd")
        mock_query.assert_called_once()

    @patch('app.db.session.query')
    def test_get_dogs_empty(self, mock_query):
        """Test retrieval when no dogs are available"""
        self._setup_paginate_mock(mock_query, [])

        response = self.app.get('/api/dogs')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['dogs'], [])

    @patch('app.db.session.query')
    def test_get_dogs_structure(self, mock_query):
        """Test the response structure for a single dog"""
        dog = self.SimpleDog(1, "Buddy", "Labrador")
        self._setup_paginate_mock(mock_query, [dog])

        response = self.app.get('/api/dogs')
        data = json.loads(response.data)
        self.assertTrue(isinstance(data['dogs'], list))
        self.assertEqual(len(data['dogs']), 1)
        self.assertEqual(set(data['dogs'][0].keys()), {'id', 'name', 'breed'})


if __name__ == '__main__':
    unittest.main()