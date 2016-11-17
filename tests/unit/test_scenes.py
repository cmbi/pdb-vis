import logging
import os

from mock import patch
from nose.tools import eq_, raises

from pdb_vis.factory import create_app
from pdb_vis.services import scenes


_log = logging.getLogger(__name__)


class TestScenes(object):
    @classmethod
    def setup_class(cls):
        cls.flask_app = create_app({'TESTING': True})
        cls.app = cls.flask_app.test_client()

    @raises(ValueError)
    def test_get_scene_dir_invalid_scene(self):
        name = '1crn-sym-contacts.sce'
        scenes.get_scene_dir(None, None, name, None)

    @raises(ValueError)
    def test_get_scene_dir_invalid_scene_2(self):
        name = '1crn_sym_contacts.sce'
        scenes.get_scene_dir(None, None, name, None)

    @raises(ValueError)
    def test_get_scene_dir_invalid_scene_3(self):
        name = '1crn_sym-contacts'
        scenes.get_scene_dir(None, None, name, None)

    @patch('os.path.isdir')
    @patch('os.path.exists')
    def test_get_scene_dir_exists(self, *args):
        SCENES_ROOT = '/sce_root'
        sce_type = 'ss2'
        pdb_ac = '1crn'
        expected_dir = os.path.join(SCENES_ROOT, sce_type, pdb_ac)
        scene_dir = scenes.get_scene_dir('/sce_root', '1crn',
                                         '1crn_sym-contacts.sce',
                                         {'ss2': 'sym-contacts'})
        eq_(scene_dir, expected_dir)

    @raises(ValueError)
    def test_get_scene_dir_doesnt_exist(self, *args):
        SCENES_ROOT = '/sce_root'
        sce_type = 'ss2'
        pdb_ac = '1crn'
        expected_dir = os.path.join(SCENES_ROOT, sce_type, pdb_ac)
        scene_dir = scenes.get_scene_dir('/sce_root', '1crn',
                                         '1crn_sym-contacts.sce',
                                         {'ss2': 'sym-contacts'})
        eq_(scene_dir, expected_dir)

    @raises(ValueError)
    @patch('os.path.isdir')
    def test_get_scene_dir_file_doesnt_exist(self, *args):
        SCENES_ROOT = '/sce_root'
        sce_type = 'ss2'
        pdb_ac = '1crn'
        expected_dir = os.path.join(SCENES_ROOT, sce_type, pdb_ac)
        scene_dir = scenes.get_scene_dir('/sce_root', '1crn',
                                         '1crn_sym-contacts.sce',
                                         {'ss2': 'sym-contacts'})
        eq_(scene_dir, expected_dir)

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
