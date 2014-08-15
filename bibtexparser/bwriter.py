#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Francois Boulogne
# License:

import json
import logging

logger = logging.getLogger(__name__)

__all__ = ['to_bibtex', 'to_json']


def to_bibtex(parsed):
    """
    Convert parsed data to a bibtex string.
    All fields must be strings, which is the expected behavior without
    customization.

    :param parsed: BibTexParser object
    :returns: string -- bibtex
    :raises: TypeError if a field is not a string
    """
    data = parsed.get_entry_dict()
    bibtex = ''

    # Add bibliographic blocks
    for entry in sorted(data.keys()):
        # Write BibTeX key
        bibtex += '@' + data[entry]['type'] + '{' + data[entry]['id']

        # Write field = value lines
        for field in [i for i in sorted(data[entry]) if i not in ['type', 'id']]:
            try:
                bibtex += ",\n " + field + " = {" + data[entry][field] + "}"
            except TypeError:
                raise TypeError("The field %s in entry %s must be a string"
                                % (field, entry))
        bibtex += "\n}\n\n"

    # Add comment blocks
    for comment in parsed.comments:
        bibtex += "@comment{{{0}}}\n\n".format(comment)
    return bibtex


def to_json(parsed):
    """
    Convert parsed data to json. This function is EXPERIMENTAL.

    :param parsed: BibTexParser object
    :returns: string -- json
    """
    return json.dumps(parsed.get_entry_dict(), sort_keys=True,
                      indent=4, separators=(',', ': '))
