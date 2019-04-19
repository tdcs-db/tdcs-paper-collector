import logging
from functions.pubmed import pubmed_search_for_id as _pubmed_search_for_id
from functions.pubmed import pubmed_id_to_records as _pubmed_id_to_records
from functions.pubmed import entrez_decoder as _entrez_decoder

results = _pubmed_search_for_id('tdcs', search_param={'retmax': 2})
id_list = results['IdList']
print(id_list)
papers = _pubmed_id_to_records(id_list)

# print( papers )

papers_extracted = _entrez_decoder(papers)
print(
    papers_extracted
)