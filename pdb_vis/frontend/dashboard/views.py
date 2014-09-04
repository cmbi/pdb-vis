import logging
import os

from flask import Blueprint, current_app, redirect, render_template, url_for

from pdb_vis.frontend.dashboard.forms import PdbForm
from pdb_vis.services import acc, dsp, scenes


_log = logging.getLogger(__name__)

bp = Blueprint('dashboard', __name__)


@bp.route("/", methods=['GET', 'POST'])
def index():
    form = PdbForm()
    if form.validate_on_submit():
        return redirect(url_for('dashboard.output',
                                pdb_type=form.type_.data,
                                pdb_ac=form.pdb_id.data))
    return render_template("dashboard/index.html", form=form)


@bp.route("/<pdb_type>/<pdb_ac>/", methods=['GET'])
def output(pdb_type, pdb_ac):
    if pdb_type == 'pdb':
        dsp_root = current_app.config['DSP_ROOT_PDB']
        acc_root = current_app.config['ACC_ROOT_PDB']
        sce_root = current_app.config['SCE_ROOT_PDB']
    elif pdb_type == 'pdb_redo':
        dsp_root = current_app.config['DSP_ROOT_PDB_REDO']
        acc_root = current_app.config['ACC_ROOT_PDB_REDO']
        sce_root = current_app.config['SCE_ROOT_PDB_REDO']
    else:
        raise ValueError("Invalid pdb type '{}'".format(pdb_type))

    dsp_data = dsp.parse(os.path.join(dsp_root, pdb_ac, pdb_ac + ".dsp.bz2"))
    acc_data = acc.parse(os.path.join(acc_root, pdb_ac, pdb_ac + ".acc.bz2"))
    sce_files = scenes.find(sce_root, pdb_ac, current_app.config['SCE_TYPES'])

    # Ensure that the parsed dsp data and acc data lengths match.
    # This will help catch errors in whatif.
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
                           pdb_data=pdb_data,
                           scenes=sce_files)


@bp.errorhandler(Exception)  # pragma: no cover
def exception_error_handler(error):
    return render_template('dashboard/error.html', msg=error), 500
