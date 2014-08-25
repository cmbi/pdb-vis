import logging

from flask import Blueprint, redirect, render_template, request, url_for
from wtforms.validators import Regexp

from pdb_vis.frontend.dashboard.forms import PdbForm
from pdb_vis.services import dsp


_log = logging.getLogger(__name__)

bp = Blueprint('dashboard', __name__)


@bp.route("/", methods=['GET', 'POST'])
def index():
    form = PdbForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard.output', pdb_ac=form.pdb_id.data))
    return render_template("dashboard/index.html", form=form)


@bp.route("/<pdb_ac>/", methods=['GET'])
def output(pdb_ac):
    pdb_data = dsp.parse(pdb_ac)
    return render_template("dashboard/output.html",
                           pdb_ac=pdb_ac,
                           pdb_data=pdb_data)
