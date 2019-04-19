import logging
import datetime
from functions.pubmed import pubmed_search_for_id as _pubmed_search_for_id
from functions.pubmed import pubmed_id_to_records as _pubmed_id_to_records
from functions.pubmed import entrez_decoder as _entrez_decoder
import json

def main():

    
    results = _pubmed_search_for_id('tdcs', search_param={'retmax': 2})
    id_list = results['IdList']

    with open('/tmp/tdcs_ids.txt', 'a+') as fp:
        fp.write(id_list)

    papers = _pubmed_id_to_records(id_list)

    with open('/tmp/tdcs_records.txt', 'a+') as fp:
        fp.write(papers)

    # print( papers )

    papers_extracted = _entrez_decoder(papers)

    logging.info('Extracted')
    with open('/tmp/tdcs_extracted.json', 'a+') as fp:
        for line in papers_extracted:
            fp.write(
                json.dumps(line) + '\n'
            )

if __name__ == "__main__":
    print('Go Go Go: {}'.format( datetime.datetime.now().isoformat() ) )

    main()

    print('End of Game: {}'.format( datetime.datetime.now().isoformat() ) )