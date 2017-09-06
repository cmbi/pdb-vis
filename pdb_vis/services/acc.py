import bz2
import logging
import os
import re


_log = logging.getLogger(__name__)

RE_ACC = re.compile("""
                    ^
                    (?P<seq_num>[ ]*\d+)           # Residue number WHAT IF
                    [ ]                            #
                    (?P<res_type>[ ]*\w[ \w]{0,3}) # Residue type WHAT IF
                    \((?P<res_num>[\d -]{3}\d)     # Residue number PDB
                    (?P<res_ic>[A-Z ])\)           # Insertion code PDB
                    (?P<chain>\w)                  # Chain WHAT IF
                    [ ]{5}
                    (?P<ss>[ HSTEGB?])             # Secondary structure
                    [ ]+
                    (?P<acc>[0-9\.]+)              # Molecular accessibility
                    $
                    """, re.VERBOSE)

# Currently, the only reason is 'Residue not intact'
# However, we allow other reasons for future compatibility
RE_NAC = re.compile("""
                    ^
                    (?P<seq_num>[ ]*\d+)           # Residue number WHAT IF
                    [ ]                            #
                    (?P<res_type>[ ]*\w[ \w]{0,3}) # Residue type WHAT IF
                    \((?P<res_num>[\d -]{3}\d)     # Residue number PDB
                    (?P<res_ic>[A-Z ])\)           # Insertion code PDB
                    (?P<chain>\w)                  # Chain WHAT IF
                    [ ]
                    (?P<reason>[a-zA-Z][ a-zA-Z]+) # Reason for acc absence
                    $
                    """, re.VERBOSE)


def parse(acc_path):
    _log.info("Parsing acc file '{}'".format(acc_path))

    if not os.path.exists(acc_path):
        raise ValueError('File not found: {}'.format(acc_path))

    acc = {}
    with bz2.BZ2File(acc_path) as f:
        acc_lines = f.readlines()

    for line in acc_lines:
        m = re.match(RE_ACC, line)
        n = re.match(RE_NAC, line)
        if m:
            chain = m.group("chain")
            acc_value = m.group("acc")
            if chain in acc:
                acc[chain].append(float(acc_value))
            else:
                acc[chain] = [float(acc_value)]
        elif n:
            chain = n.group("chain")
            reason = n.group("reason")
            if chain in acc:
                acc[chain].append(reason)
            else:
                acc[chain] = [reason]

    if not acc:
        raise Exception("Error parsing '{}'".format(acc_path))

    return acc
