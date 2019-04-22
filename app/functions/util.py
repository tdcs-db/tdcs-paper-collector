import logging
import pandas as pd
import os
import ast


def get_val_recursively(dictionary, names):
    """
    Get value of a dictionary according to specified path (names)
    :param dict dictionary: input dictionary
    :param names: path to the value to be obtained
    **Attention**: Function can't fail: will always return value or None.
    >>> get_val_recursively({1:{2:{'3':'hi'}}},[1,2])
    {'3': 'hi'}
    >>> get_val_recursively({1:{2:{3:'hi'}}},[1,'2',3])
    {'hi'}
    """
    if isinstance(names, list):
        tmp = names.copy()
    elif isinstance(names, str):
        tmp = [names].copy()
    else:
        raise ValueError('names must be str or list')
    if len(tmp) > 1:
        pop = tmp.pop(0)
        try:
            pop = int(pop)
        except ValueError:
            pass

        try:
            return get_val_recursively(dictionary[pop], tmp)
        except:
            logging.log(20, pop)
            return None
    elif len(tmp) == 0:
        return None
    else:
        try:
            val = int(tmp[0])
        except:
            val = tmp[0]
        try:
            return dictionary[val]
        except KeyError:
            logging.log(20, 'KeyError: Could not find {}'.format(tmp[0]))
            return None
        except TypeError:
            logging.log(20, 'TypeError: Could not find {}'.format(tmp[0]))
            return None



def pubmed_json2csv(json_file_path, csv_file_path):
    """This function converts json of pubmed download to csv to be uploaded to google spreadsheet.
    """
    
    if not os.path.isfile(json_file_path):
        raise Exception('json file input does not exist: {}'.format(json_file_path) )
    
    
    df_from_json = pd.read_json(json_file_path, lines=True)
    
    df_from_json.to_csv(csv_file_path, index=False)
        
    