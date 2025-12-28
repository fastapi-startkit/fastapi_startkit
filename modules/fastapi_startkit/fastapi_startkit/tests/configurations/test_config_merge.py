from unittest.mock import MagicMock, patch
from fastapi_startkit.configuration import Configuration
from fastapi_startkit.loader import Loader

class TestConfiguration:
    def test_merge_with_dict(self):
        """Test merge_with accepts a dictionary and merges it as defaults."""
        app = MagicMock()
        config = Configuration(app)

        # Set up the existing config
        config.set('testkey', {'existing_key': 'existing_value'})

        # Dictionary to merge (defaults)
        defaults = {'new_key': 'new_value', 'existing_key': 'default_value'}

        # Act
        config.merge_with('testkey', defaults)

        # Assert
        merged = config.get('testkey')
        # New keys should be added
        assert merged['new_key'] == 'new_value'
        # Existing keys should be PRESERVED (Low Priority behavior of merge_with)
        # {**base_config, **self.get(path, {})} -> Existing overwrites base
        assert merged['existing_key'] == 'existing_value'

    def test_merge_with_file_path(self):
        """Test merge_with accepts a file path, loads it, and merges as defaults."""
        app = MagicMock()
        config = Configuration(app)

        # Setup
        config.set('testkey', {'existing': 'orig'})

        # Mock Loader to return params from file
        with patch('fastapi_startkit.configuration.Configuration.Loader') as MockLoaderClass:
            mock_loader = MockLoaderClass.return_value
            mock_loader.get_parameters.return_value = {
                'New': 'from_file',
                'Existing': 'default_from_file'
            }

            # Act
            config.merge_with('testkey', '/path/to/config.py')

            # Assert
            mock_loader.get_parameters.assert_called_once_with('/path/to/config.py')

            merged = config.get('testkey')
            # Keys are lowercased by merge_with logic: {name.lower(): value ...}
            assert merged['new'] == 'from_file'
            # Existing check
            assert merged['existing'] == 'orig'
