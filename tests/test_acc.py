# import bz2

# from mock import Mock, patch
# from nose.tools import eq_, ok_

from pdb_vis.factory import create_app


class TestAcc(object):
    @classmethod
    def setup_class(cls):
        cls.flask_app = create_app({'TESTING': True})
        cls.app = cls.flask_app.test_client()
