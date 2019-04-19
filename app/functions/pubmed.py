import logging
from Bio import Entrez
import json

Entrez.email = 'admin@neutrino.xyz'

def pubmed_search_for_id(query, search_param = None, entrez = None):
    """Search keywords on pubmed and return result in dict

    :query str: kewords to be searched on pubmed; 
                Syntax of the form '(tdcs[Title/Abstract]) OR (tacs[Title/Abstract])' is also supported
    :return: dictionary of results; 
             article list can be obtained using .get('IdList)
    """

    if entrez is None:
        entrez = Entrez
    if search_param is None:
        search_param = {}

    search_param = {
        **dict(
            term=query,
            db='pubmed',
            sort='relevance',
            retmax='20000',
            retmode='xml'),
        **search_param
    }
    
    handle = entrez.esearch(**search_param)

    try:
        results = entrez.read(handle)
    except Exception as ee:
        logging.error('Could not read Entrez handle!')

    return results
    
def entrez_decoder():
    """
    """

    decorder_map = {

    }

    return 

def pubmed_id_to_records(pubmed_ids, fetch_params = None, entrez = None):
    """Extract publication details for a pubmed id

    :pubmed_ids: pudmed ids to be analyzed
    :return: 
    """

    if isinstance(pubmed_ids, list):
        pubmed_ids = ','.join( pubmed_ids )
    elif isinstance(pubmed_ids, str):
        pubmed_ids = pubmed_ids

    if entrez is None:
        entrez = Entrez

    if fetch_params is None:
        fetch_params = {}

    fetch_params = {
        **dict(
        db='pubmed',
        retmode='xml'),
        **fetch_params
    }

    fetch_params = {
        **{'id':pubmed_ids},
        **fetch_params
    }

    handle = entrez.efetch(**fetch_params)
    results = entrez.read(handle)
    return results

if __name__ == '__main__':
    results = pubmed_search_for_id('tdcs', search_param={'retmax': 2})
    id_list = results['IdList']
    print(id_list)
    papers = pubmed_id_to_records(id_list)

    print( papers.values() )
    for i in papers:
        print(i)