import logging

from mock import patch
from nose.tools import eq_, ok_

from pdb_vis.factory import create_app


_log = logging.getLogger(__name__)


class TestDashboardViews(object):
    @classmethod
    def setup_class(cls):
        cls.flask_app = create_app({'TESTING': True,
                                    'SECRET_KEY': 'testing',
                                    'WTF_CSRF_ENABLED': False})
        cls.app = cls.flask_app.test_client()

    def test_index_get(self):
        rv = self.app.get('/')
        eq_(rv.status_code, 200)
        ok_('<input class="form-control" id="pdb_id" name="pdb_id"' in rv.data)

    @patch('pdb_vis.services.dsp.parse')
    @patch('pdb_vis.services.acc.parse')
    def test_index_post(self, mock_acc_parse, mock_dsp_parse):
        mock_acc_parse.return_value = {
            'A': [1.0, 2.0, 3.0, 4.0],
            'B': [5.0, 6.0, 7.0, 8.0]
        }
        mock_dsp_parse.return_value = {
            'A': {'sequence': 'MELK',
                  'secondary_structure': 'THLT',
                  'contacts': '** *',
                  'solvent_accessible': ' A A'},
            'B': {'sequence': 'MELK',
                  'secondary_structure': 'HLL3',
                  'contacts': '* * ',
                  'solvent_accessible': 'AAAA'},
        }

        rv = self.app.post('/', data={'pdb_id': '12e8'}, follow_redirects=True)
        eq_(rv.status_code, 200)

        assert '<h4>Chain A</h4>' in rv.data
        assert '<h4>Chain B</h4>' in rv.data

        ps_1 = '        var seq = new ProteinSequence("canvas_chain_A",\n' + \
               '                                      "MELK",\n' + \
               '                                      "THLT",\n' + \
               '                                      [1.0, 2.0, 3.0, 4.0]);'
        assert ps_1 in rv.data

        ps_2 = '        var seq = new ProteinSequence("canvas_chain_B",\n' + \
               '                                      "MELK",\n' + \
               '                                      "HLL3",\n' + \
               '                                      [5.0, 6.0, 7.0, 8.0]);\n'
        assert ps_2 in rv.data
