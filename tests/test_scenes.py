import logging
import os

from mock import patch

from pdb_vis.factory import create_app
from pdb_vis.services import scenes


_log = logging.getLogger(__name__)


class TestScenes(object):
    @classmethod
    def setup_class(cls):
        cls.flask_app = create_app({'TESTING': True})
        cls.app = cls.flask_app.test_client()

    @patch('os.path.exists')
    def test_find_exists(self, mock_exists):
        SCENES_ROOT = '/sce_root'
        test_data = {
            SCENES_ROOT + '/ss2/1crn/1crn_sym-contacts.sce': True
        }
        mock_exists.side_effect = lambda a: test_data[a]

        expected_files = [os.path.split(k)[1]
                          for k, v in test_data.iteritems() if v]
        scene_files = scenes.find('/sce_root', '1crn', {'ss2': 'sym-contacts'})

        assert scene_files == expected_files

    @patch('os.path.exists')
    def test_find_doesnt_exist(self, mock_exists):
        SCENES_ROOT = '/sce_root'
        test_data = {
            SCENES_ROOT + '/ss2/1crn/1crn_sym-contacts.sce': False
        }
        mock_exists.side_effect = lambda a: test_data[a]

        expected_files = [os.path.split(k)[1]
                          for k, v in test_data.iteritems() if v]
        scene_files = scenes.find('/sce_root', '1crn', {'ss2': 'sym-contacts'})

        assert scene_files == expected_files
