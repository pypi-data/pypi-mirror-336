from typing import List
from hestia_earth.schema import TermTermType

from .lookup import get_table_value, download_lookup, column_name, lookup_term_ids
from .model import find_primary_product

_COLUMN_NAME = 'inHestiaDefaultSystemBoundary'
_ALLOW_ALL = 'all'


def emission_is_in_system_boundary(term_id: str, termType: TermTermType = TermTermType.EMISSION) -> bool:
    """
    Check if the emission is included in the HESTIA system boundary.

    Parameters
    ----------
    term_id : str
        The emission term ID

    Returns
    -------
    bool
        True if the emission is included in the HESTIA system boundary, False otherwise.
    """
    lookup = download_lookup(f"{termType.value}.csv")
    value = get_table_value(lookup, 'termid', term_id, column_name(_COLUMN_NAME))
    # handle numpy boolean
    return not (not value)


def emissions_in_system_boundary(termType: TermTermType = TermTermType.EMISSION) -> List[str]:
    """
    Get all emissions included in HESTIA system boundary.

    Returns
    -------
    List[str]
        List of emission IDs
    """
    lookup = download_lookup(f"{termType.value}.csv")
    # find all emissions in system boundary
    return list(filter(emission_is_in_system_boundary, lookup_term_ids(lookup)))


def cycle_emission_is_in_system_boundary(cycle: dict, termType: TermTermType = TermTermType.EMISSION):
    lookup = download_lookup(f"{termType.value}.csv")
    site_type = cycle.get('site', {}).get('siteType')
    product = find_primary_product(cycle) or {}
    inputs = cycle.get('inputs', [])

    def is_allowed(emission_term_id: str, column: str, condition: str):
        values = get_table_value(lookup, 'termid', emission_term_id, column_name(column))
        values = (values or _ALLOW_ALL).split(';')
        return True if _ALLOW_ALL in values or not condition else condition in values

    def filter_term(term_id: str):
        return emission_is_in_system_boundary(term_id) and all([
            is_allowed(term_id, 'siteTypesAllowed', site_type),
            is_allowed(term_id, 'productTermTypesAllowed', product.get('term', {}).get('termType')),
            is_allowed(term_id, 'productTermIdsAllowed', product.get('term', {}).get('@id')),
            not inputs or any([
                is_allowed(term_id, 'inputTermTypesAllowed', input.get('term', {}).get('termType')) for input in inputs
            ]),
            not inputs or any([
                is_allowed(term_id, 'inputTermIdsAllowed', input.get('term', {}).get('@id')) for input in inputs
            ])
        ])

    return filter_term


def cycle_emissions_in_system_boundary(cycle: dict, termType: TermTermType = TermTermType.EMISSION):
    """
    Get all emissions relevant for the Cycle, included in HESTIA system boundary.

    Returns
    -------
    List[str]
        List of emission IDs
    """
    lookup = download_lookup(f"{termType.value}.csv")
    # find all emissions in system boundary
    return list(filter(cycle_emission_is_in_system_boundary(cycle), lookup_term_ids(lookup)))
