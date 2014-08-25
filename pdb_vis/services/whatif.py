import requests
import xml.etree.ElementTree as et

from flask import current_app as app


_AMINO_ACID_LT = {
    'ALA': 'A', 'ARG': 'R', 'ASN': 'N', 'ASP': 'D', 'CYS': 'C', 'GLU': 'E',
    'GLN': 'Q', 'GLY': 'G', 'HIS': 'H', 'ILE': 'I', 'LEU': 'L', 'LYS': 'K',
    'MET': 'M', 'PHE': 'F', 'PRO': 'P', 'SER': 'S', 'THR': 'T', 'TRP': 'W',
    'TYR': 'Y', 'VAL': 'V',
}


def pdb_sequence(pdb_id):
    """
    Queries what if for the sequence data for the given PDB id.

    :return: A dict where the key is the chain and the value is the sequence for
             that chain.
    """

    # et.register_namespace('wiws', 'http://swift.cmbi.ru.nl/wiws')
    namespaces = {'wiws': 'http://swift.cmbi.ru.nl/wiws'}

    url = '{}PDB_sequence/id/{}/'.format(app.config['WHATIF_REST_URL'], pdb_id)
    r = requests.get(url)
    r.raise_for_status()

    result = {}
    root = et.fromstring(r.text)
    for res_elem in root.iterfind('.//wiws:residue', namespaces=namespaces):
        chain_elem = res_elem.find('./wiws:chain', namespaces=namespaces)
        type_elem = res_elem.find('./wiws:type', namespaces=namespaces)

        residue = _AMINO_ACID_LT[type_elem.text]
        chain = chain_elem.text

        if chain in result:
            result[chain] = result[chain] + residue
        else:
            result[chain] = residue
    return result
