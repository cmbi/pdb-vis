import logging
import os
from itertools import ifilter


_log = logging.getLogger(__name__)


def find(sce_root, pdb_ac, types):
    # Build a list of candidate paths to YASARA scene files for the given PDB
    # accession code.
    scene_files = [
        os.path.join(sce_root, k, pdb_ac, "{}_{}.sce".format(pdb_ac, v))
        for k, v in types.iteritems()]

    # Remove paths that don't exist
    # It's legitimate that some scene files don't exist, so this is not
    # considered an error case.
    scene_files[:] = list(ifilter(lambda x: os.path.exists(x), scene_files))

    # Remove the path leaving only the filename
    scene_files = [os.path.split(f)[1] for f in scene_files]

    return scene_files
