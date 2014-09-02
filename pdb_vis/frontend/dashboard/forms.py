import re

from flask_wtf import Form
from wtforms.fields import SelectField, TextField
from wtforms.validators import Regexp


RE_PDB_ID = re.compile(r"^[0-9a-zA-Z]{4}$")


class PdbForm(Form):
    type_ = SelectField(u'Method',
                        choices=[('pdb', 'PDB'),
                                 ('pdb_redo', 'PDB Redo')])
    pdb_id = TextField(u'PDB id', [Regexp(regex=RE_PDB_ID)])
