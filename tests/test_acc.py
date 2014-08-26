import logging

from mock import patch
from nose.tools import eq_, ok_, raises

from pdb_vis.factory import create_app
from pdb_vis.services import acc


_log = logging.getLogger(__name__)


class TestAcc(object):
    @classmethod
    def setup_class(cls):
        cls.flask_app = create_app({'TESTING': True})
        cls.app = cls.flask_app.test_client()

    @patch('bz2.BZ2File')
    @patch('os.path.exists', return_value=True)
    def test_parse_multiple_chains(self, mock_exists, mock_bz2file):
        with open('tests/17gs.acc') as f:
            acc_data = f.read()

        instance = mock_bz2file.return_value
        instance.__enter__.return_value.read.return_value = acc_data
        result = acc.parse('17gs')

        eq_(len(result), 2)  # Only one chain
        for chain in 'AB':
            ok_(chain in result.keys())

        eq_(len(result['A']), 210)
        eq_(len(result['B']), 208)

    @raises(ValueError)
    @patch('os.path.exists', return_value=False)
    def test_parse_file_not_found(self, mock_exists):
        acc.parse('17gs')

    @raises(Exception)
    @patch('bz2.BZ2File')
    @patch('os.path.exists', return_value=True)
    def test_parse_regex_fail(self, mock_exists, mock_bz2file):
        instance = mock_bz2file.return_value
        instance.__enter__.return_value.read.return_value = ""
        acc.parse('17gs')
