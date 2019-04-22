import logging
import datetime
from functions.pubmed import pubmed_search_for_id as _pubmed_search_for_id
from functions.pubmed import pubmed_id_to_records as _pubmed_id_to_records
from functions.pubmed import entrez_decoder as _entrez_decoder
import json
import argparse
from functions.util import pubmed_json2csv as _pubmed_json2csv
import os

def prepare_data_directory(working_dir):
    """Create folders for the input output data
    """

    try:
        # Create target Directory
        os.mkdir(working_dir)
        logging.info("Working directory created: {}".format(working_dir) )
    except FileExistsError:
        logging.warning("Working directory already exists: {}".format(working_dir) )

    return working_dir


def main():

    parser = argparse.ArgumentParser(description='Download Pubmed tDCS data')
    parser.add_argument(
        '--keywords',
        nargs='+',
        dest='keywords', 
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

    ## prepare the working direction for data
    today_string = datetime.date.today().isoformat()
    working_directory = '/tmp/tdcs_{}'.format(today_string)
    prepare_data_directory(working_directory)

    tdcs_extracted_path = os.path.join(working_directory, 'tdcs_extracted.json')
    tdcs_records_path = os.path.join(working_directory, 'tdcs_records.txt')
    tdcs_ids_path = os.path.join(working_directory,'tdcs_ids.txt')
    tdcs_extracted_csv_path = os.path.join(working_directory, 'tdcs_extracted.csv')

    results = _pubmed_search_for_id(
        args_keywords, 
        search_param={'retmax': args_limit}
        )
    
    id_list = results['IdList']
    
    with open(tdcs_ids_path, 'a+') as fp:
        for line in id_list:
            fp.write( str(line) + '\n' )

    papers = _pubmed_id_to_records(id_list)

    

    with open(tdcs_records_path, 'a+') as fp:
        fp.write( str(papers) )


    papers_extracted = _entrez_decoder(papers)

    logging.info('Extracted')

    with open(tdcs_extracted_path, 'a+') as fp:
        for line in papers_extracted:
            fp.write(
                json.dumps(line) + '\n'
            )
        
    logging.info('Dumped: {}'.format(tdcs_extracted_path) )

    _pubmed_json2csv(
        tdcs_extracted_path,
        tdcs_extracted_csv_path
    )

    logging.info('Converted to csv: {}'.format(tdcs_extracted_csv_path) )



if __name__ == "__main__":
    print('Go Go Go: {}'.format( datetime.datetime.now().isoformat() ) )

    main()
    

    print('End of Game: {}'.format( datetime.datetime.now().isoformat() ) )