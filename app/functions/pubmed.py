import logging
from Bio import Entrez
import json
from functions.util import get_val_recursively as _get_val_recursively

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
    
def entrez_decoder(pubmed_records):
    """Decode return value of entrez decoder
    """
    def articledate(article__date):
        if len(article__date) >=1 :
            return {
                'year': article__date[0].get('Year'),
                'month': article__date[0].get('Month'),
                'day': article__date[0].get('Day')
            }
        else:
            return None

    def articleabstract(article__abstract):
        if article__abstract:
            return article__abstract.get('AbstractText')
        else:
            return None

    def articlejournal(article__journal):
        if article__journal:
            return {
                'title': article__journal.get('Title'),
                'iso_abbrev': article__journal.get('ISOAbbreviation'),
                'date': {
                    'year': article__journal.get('PubDate',{}).get('Year'),
                    'month': article__journal.get('PubDate',{}).get('Month'),
                    'day': article__journal.get('PubDate',{}).get('Day')
                }
            }
        else:
            return None

    def articleauthors(article__authors):
        
        authors = []

        if article__authors:
            for author in article__authors:
                author__details = {
                    'last_name': author.get('LastName'),
                    'first_name': author.get('ForeName'),
                    'affiliations': [
                        i.get('Affiliation') for i in author.get('AffiliationInfo', [])
                    ]
                }
                authors.append(author__details)

        return authors

    pubmed_articles = pubmed_records.get('PubmedArticle')


    articles_export = []

    for record in pubmed_articles:
        record_medlinecitation = record.get('MedlineCitation', {})
        record_medlinecitation_pmid = str(record_medlinecitation.get('PMID', ''))
        record_medlinecitation_article = record_medlinecitation.get('Article', {})
        record_medlinecitation_article__title = record_medlinecitation_article.get('ArticleTitle')
        record_medlinecitation_article__date = articledate(
            record_medlinecitation_article.get('ArticleDate', [])
        )
        record_medlinecitation_article__journal = articlejournal(
            record_medlinecitation_article.get('Journal')
        )
        record_medlinecitation_article__abstract = articleabstract(
            record_medlinecitation_article.get('Abstract')
        )
        record_medlinecitation_article__authors = articleauthors(
            record_medlinecitation_article.get('AuthorList')
            )
        record_medlinecitation_article__doi = str(record_medlinecitation_article.get('ELocationID',[]) )
        record_export = {
            'title': record_medlinecitation_article__title,
            'date': record_medlinecitation_article__date,
            'journal': record_medlinecitation_article__journal,
            'abstract': record_medlinecitation_article__abstract,
            'authors': record_medlinecitation_article__authors,
            'doi': record_medlinecitation_article__doi,
            'pmid': record_medlinecitation_pmid
        }

        articles_export.append(record_export)

    return articles_export

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

    # print( papers )
    

    papers_extracted = entrez_decoder(papers)
    print(
        papers_extracted
    )
        

    print('END of GAME')