import requests

from mock import Mock, patch
from nose.tools import eq_

from pdb_vis.factory import create_app
from pdb_vis.services.whatif import pdb_sequence


class TestWhatif(object):
    @classmethod
    def setup_class(cls):
        cls.flask_app = create_app({'TESTING': True,
                                    'WHATIF_REST_URL': 'http://fake.url/rest/'})
        cls.app = cls.flask_app.test_client()

    @patch('requests.get')
    def test_pdb_sequence(self, mock_requests):
        with open('tests/4bxu_whatif.xml') as xml_1crn_file:
            xml_1crn = xml_1crn_file.read()

        mock = Mock(spec=requests.Response)
        mock.status_code = 200
        mock.text = xml_1crn
        mock_requests.return_value = mock

        with self.flask_app.test_request_context('/'):
            result = pdb_sequence('4bxu')
            eq_(len(result), 2)
            eq_(result.keys(), ['A', 'B'])
            eq_(len(result['A']), 69)
            eq_(len(result['B']), 15)
            eq_(result['A'], 'GAMATPGSENVLPREPLIATAVKFLQNSRVRQSPLATRRAFLKKKG' +
                             'LTDEEIDMAFQQSGTAADEPSSL')
            eq_(result['B'], 'ASEDELVAEFLQDQN')

        mock_requests.assert_called_with(
            'http://fake.url/rest/PDB_sequence/id/4bxu/')
