import logging
import os
import re
from itertools import ifilter


_log = logging.getLogger(__name__)

_sep = "_"

RE_SCENE = re.compile("[a-z0-9]{4}" +   # PDB identifier
                      _sep +            # separator
                      "[a-z\-]+\.sce",  # scene type and extension
                      re.VERBOSE)


def get_scene_dir(sce_root, pdb_ac, sce_file, types):
    """Find the YASARA scene directory by scene filename.

    The file must exist and have a valid filename,
    otherwise a ValueError will be raised.
    """
    scene_dir = None

    if not re.match(RE_SCENE, sce_file):
        raise ValueError("Invalid YASARA scene filename: '{}'".format(
            sce_file))

    for k, v in types.iteritems():
        # Remove pdb ac and extension from filename
        if v == sce_file.split(_sep)[1].split(".")[0]:
            scene_dir = os.path.join(sce_root, k, pdb_ac)

    if not os.path.isdir(scene_dir):
        raise ValueError("Error finding YASARA scene directory")

    if not os.path.exists(os.path.join(scene_dir, sce_file)):
        raise ValueError("YASARA scene not found")

    return scene_dir


def find(sce_root, pdb_ac, types):
    # Build a list of candidate paths to YASARA scene files for the given PDB
    # accession code.
    scene_files = [
        os.path.join(sce_root, k, pdb_ac, "{}{}{}.sce".format(pdb_ac, _sep, v))
        for k, v in types.iteritems()]

    # Remove paths that don't exist
    # It's legitimate that some scene files don't exist, so this is not
    # considered an error case.
    scene_files[:] = list(ifilter(lambda x: os.path.exists(x), scene_files))

    # Remove the path leaving only the filename
    scene_files = [os.path.split(f)[1] for f in scene_files]

    return scene_files
