import logging
import datetime
from functions.pubmed import pubmed_search_for_id as _pubmed_search_for_id
from functions.pubmed import pubmed_id_to_records as _pubmed_id_to_records
from functions.pubmed import entrez_decoder as _entrez_decoder
import json
import argparse

def main():

    parser = argparse.ArgumentParser(description='Download Pubmed tDCS data')
    parser.add_argument(
        '--keywords',
        nargs='+',
        dest='task', 
        default='tdcs',
        help='keywords to be searched'
        )
    parser.add_argument(
        '--limit', 
        dest='limit', 
        default='10000',
        help='limit the number of items to be downloaded'
        )
    args = parser.parse_args()
    args_keywords = args.keywords
    args_limit = args.limit

    results = _pubmed_search_for_id(
        args_keywords, 
        search_param={'retmax': args_limit}
        )
    
    id_list = results['IdList']

    with open('/tmp/tdcs_ids.txt', 'a+') as fp:
        for line in id_list:
            fp.write( str(line) + '\n' )

    papers = _pubmed_id_to_records(id_list)

    with open('/tmp/tdcs_records.txt', 'a+') as fp:
        fp.write( str(papers) )

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