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
            acc_data = f.readlines()

        instance = mock_bz2file.return_value
        instance.__enter__.return_value.readlines.return_value = acc_data
        result = acc.parse('17gs.acc.bz2')

        eq_(len(result), 2)
        for chain in 'AB':
            ok_(chain in result.keys())

        eq_(len(result['A']), 210)
        eq_(len(result['B']), 208)
        mock_exists.assert_called_with('17gs.acc.bz2')

    @patch('bz2.BZ2File')
    @patch('os.path.exists', return_value=True)
    def test_parse_acc_and_reason(self, mock_exists, mock_bz2file):
        with open('tests/1evq.acc') as f:
            acc_data = f.readlines()

        instance = mock_bz2file.return_value
        instance.__enter__.return_value.readlines.return_value = acc_data
        result = acc.parse('1evq.acc.bz2')

        eq_(len(result), 1)
        eq_(len(result['A']), 308)
        mock_exists.assert_called_with('1evq.acc.bz2')

    @patch('bz2.BZ2File')
    @patch('os.path.exists', return_value=True)
    def test_parse_multiple_chains_reason(self, mock_exists, mock_bz2file):
        """Tests that multiple chains are parsed correctly.

        Test that chain id can be lowercase or integer.
        Test that reasons in multiple chains are handled correctly.
        """
        acc_data = ['   54 PHE (  17 )a     H    0.17',
                    '  195 DTHY(-158C)a Residue is not intact',
                    '  415 GLU ( 394 )1 Residue is not intact',
                    '  410 PRO ( 373 )1         47.44']
        instance = mock_bz2file.return_value
        instance.__enter__.return_value.readlines.return_value = acc_data
        result = acc.parse('test.acc.bz2')

        eq_(len(result), 2)
        eq_(len(result['a']), 2)
        eq_(len(result['1']), 2)
        mock_exists.assert_called_with('test.acc.bz2')

    @raises(ValueError)
    @patch('os.path.exists', return_value=False)
    def test_parse_file_not_found(self, mock_exists):
        acc.parse('17gs.acc.bz2')
        mock_exists.assert_called_with('17gs.acc.bz2')

    @raises(Exception)
    @patch('bz2.BZ2File')
    @patch('os.path.exists', return_value=True)
    def test_parse_regex_fail(self, mock_exists, mock_bz2file):
        instance = mock_bz2file.return_value
        instance.__enter__.return_value.read.return_value = ""
        acc.parse('17gs.acc.bz2')
        mock_exists.assert_called_with('17gs.acc.bz2')

    @raises(ValueError)
    @patch('bz2.BZ2File')
    @patch('os.path.exists', return_value=True)
    def test_parse_acc_no_float(self, mock_exists, mock_bz2file):
        acc_data = ['   54 PHE (  17 )a     H    0.0.0']
        instance = mock_bz2file.return_value
        instance.__enter__.return_value.readlines.return_value = acc_data
        acc.parse('test.acc.bz2')
        mock_exists.assert_called_with('test.acc.bz2')

    def test_parse_chains(self):
        acc_data = acc.parse('tests/4eha.acc.bz2')

        eq_(sorted(acc_data.keys()), ['A', 'B', 'C', 'F'])
