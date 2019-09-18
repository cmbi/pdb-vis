import bz2
import logging
import os


_log = logging.getLogger(__name__)


def parse(dsp_path):
    _log.info("Parsing '{}'".format(dsp_path))

    if not os.path.exists(dsp_path):
        raise ValueError('File not found: {}'.format(dsp_path))

    with bz2.open(dsp_path, 'rt') as f:
        dsp_lines = f.readlines()

    _log.debug("DSP contains {} lines".format(len(dsp_lines)))

    num_chains = (len(dsp_lines) - 2) / 6

    _log.debug("Expecting {} chains".format(num_chains))

    chains = {}
    for i in range(1, len(dsp_lines) - 1, 6):
        chn = dsp_lines[i][6:7]

        _log.debug("Processing chain {}".format(chn))

        seq = dsp_lines[i+2][13:].strip('\n')
        sst = dsp_lines[i+3][13:].strip('\n')
        con = dsp_lines[i+4][13:].strip('\n')
        sol = dsp_lines[i+5][13:].strip('\n')

        if not (len(seq) == len(sst) == len(con) == len(sol)):
            raise RuntimeError("The lengths of the secondary structure, " +
                               "contacts, solvent accessibility and " +
                               "sequence don't match.")

        assert chn not in chains
        chains[chn] = {'sequence': seq,
                       'secondary_structure': sst,
                       'contacts': con,
                       'solvent_accessible': sol}
    _log.debug("Parsed {} chains".format(len(chains.keys())))
    return chains
