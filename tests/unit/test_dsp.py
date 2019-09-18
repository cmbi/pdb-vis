import logging

from mock import patch
from nose.tools import eq_, ok_, raises

from pdb_vis.factory import create_app
from pdb_vis.services import dsp


_log = logging.getLogger(__name__)


class TestDsp(object):
    @classmethod
    def setup_class(cls):
        cls.flask_app = create_app({'TESTING': True})
        cls.app = cls.flask_app.test_client()

    @patch('bz2.open')
    @patch('os.path.exists', return_value=True)
    def test_parse(self, mock_exists, mock_bz2file):
        instance = mock_bz2file.return_value
        instance.__enter__.return_value.readlines.return_value = [
            "1aie",
            "Chain A              10        20        30",
            "                      |         |         |",
            "   1 -   31  EYFTLQIRGRERFEMFRELNEALELKDAQAG",
            "   1 -   31          THHHHHHHHHHHHHHHHHHHH  ",
            "   1 -   31  ********** ** ***   ** ********",
            "   1 -   31  AAAAAAAAAAAAAAAAAAAAAAAAAAAAA A",
            "*END"]

        result = dsp.parse('1al3.dsp')

        eq_(len(result), 1)  # Only one chain
        ok_('A' in result.keys())  # Chain is 'A'

        for chain, data in result.items():
            _log.debug("Testing chain {}".format(chain))
            ok_('sequence' in data)
            ok_('secondary_structure' in data)
            ok_('contacts' in data)
            ok_('solvent_accessible' in data)

        eq_(len(result['A']['sequence']), 31)
        eq_(len(result['A']['secondary_structure']), 31)
        eq_(len(result['A']['contacts']), 31)
        eq_(len(result['A']['solvent_accessible']), 31)
        eq_(result['A']['sequence'], 'EYFTLQIRGRERFEMFRELNEALELKDAQAG')
        eq_(result['A']['secondary_structure'],
            '        THHHHHHHHHHHHHHHHHHHH  ')
        eq_(result['A']['contacts'],
            '********** ** ***   ** ********')
        eq_(result['A']['solvent_accessible'],
            'AAAAAAAAAAAAAAAAAAAAAAAAAAAAA A')

    @patch('bz2.open')
    @patch('os.path.exists', return_value=True)
    def test_parse_multiple_chains(self, mock_exists, mock_bz2file):
        with open('tests/12e8.dsp') as f:
            dsp_data = f.readlines()

        instance = mock_bz2file.return_value
        instance.__enter__.return_value.readlines.return_value = dsp_data
        result = dsp.parse('12e8.dsp')

        eq_(len(result), 4)
        for chain in 'LHMP':
            ok_(chain in result.keys())

        for chain, data in result.items():
            _log.debug("Testing chain {}".format(chain))
            ok_('sequence' in data)
            ok_('secondary_structure' in data)
            ok_('contacts' in data)
            ok_('solvent_accessible' in data)

        eq_(len(result['L']['sequence']), 214)
        eq_(len(result['H']['sequence']), 221)
        eq_(len(result['M']['sequence']), 214)
        eq_(len(result['P']['sequence']), 221)

    @raises(RuntimeError)
    @patch('bz2.open')
    @patch('os.path.exists', return_value=True)
    def test_parse_inconsistent_lengths(self, mock_exists, mock_bz2file):
        instance = mock_bz2file.return_value
        instance.__enter__.return_value.readlines.return_value = [
            "1aie",
            "Chain A              10        20        30",
            "                      |         |         |",
            "   1 -   31  EYFTLQIRGRERFEMFRELNEALELKDAQAG",
            "   1 -   31          THHHHHHHHHHHHHHHHHHHH ",
            "   1 -   31  ********** ** ***   ** ********",
            "   1 -   31  AAAAAAAAAAAAAAAAAAAAAAAAAAAAA A",
            "*END"]

        dsp.parse('1al3.dsp')

    @raises(ValueError)
    @patch('os.path.exists', return_value=False)
    def test_parse_dsp_file_not_found(self, mock_path_exists):
        dsp.parse('this-doesnt-exist')
        mock_path_exists.assert_called_with('this-doesnt-exist')

    def test_parse_chains(self):
        dsp_data = dsp.parse('tests/4eha.dsp.bz2')

        eq_(sorted(dsp_data.keys()), ['A', 'B', 'C', 'F'])

    def test_chain_lengths(self):
        dsp_data = dsp.parse('tests/4m61.dsp.bz2')

        eq_(len(dsp_data['A']['sequence']), 219)
        eq_(len(dsp_data['B']['sequence']), 220)
        eq_(len(dsp_data['C']['sequence']), 219)
        eq_(len(dsp_data['D']['sequence']), 220)
