import logging

from flask import Blueprint, redirect, render_template, url_for

from pdb_vis.frontend.dashboard.forms import PdbForm
from pdb_vis.services import dsp, acc


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
    dsp_data = dsp.parse(pdb_ac)
    acc_data = acc.parse(pdb_ac)

    # Ensure that the parsed dsp data and acc data lengths match. This will help
    # catch errors in whatif.
    if dsp_data.keys() != acc_data.keys():
        msg = "Chain mismatch between ACC and DSP data for '{}'".format(pdb_ac)
        _log.error(msg)
        raise Exception(msg)

    for chain in dsp_data.keys():
        if len(dsp_data[chain]['sequence']) != len(acc_data[chain]):
            msg = "Length mismatch between DSP sequence and " + \
                  "ACC data for '{}'".format(pdb_ac)
            _log.error(msg)
            raise Exception(msg)

    # Add the accessibility to the pdb data dict
    pdb_data = dsp_data
    for chain, acc_values in acc_data.iteritems():
        pdb_data[chain]['accessibility'] = acc_values

    return render_template("dashboard/output.html",
                           pdb_ac=pdb_ac,
                           pdb_data=pdb_data)


@bp.errorhandler(Exception)
def exception_error_handler(error):
    return render_template('dashboard/error.html', msg=error), 500
