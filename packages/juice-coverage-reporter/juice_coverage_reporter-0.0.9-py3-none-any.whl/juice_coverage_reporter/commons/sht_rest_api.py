"""
Created on March, 2022

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle SHT rest-api

"""

import os
import sys
import logging
import requests

from esac_juice_pyutils.commons.json_handler import create_file


def get_plans(url):
    """
    Get segmentation definition json via REST_API

    :param url: url
    :return: response.json: segmentation definition json
    """

    try:

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        # Code here will only run if the request is successful

        return response.json()

    except requests.exceptions.HTTPError as err:
        print(err)

    except requests.exceptions.ConnectionError as err:
        print(err)

    except requests.exceptions.Timeout as err:
        print(err)

    except requests.exceptions.RequestException as err:
        print(err)

    sys.exit()


def get_and_create_segmentation_file(crema="CREMA_3_0",
                                     url_root='https://juicesoc.esac.esa.int/rest_api/trajectory',
                                     file_name='segment_definition',
                                     output_dir='./',
                                     generate_json_file=True):
    """
    Create segmentation definition json file using REST_API

    :param crema: Crema Id
    :param url_root: url root name
    :param file_name: file name to get
    :param output_dir: output directory
    :param generate_json_file: flag to create a local copay of the json file
    """

    crema = str(crema).upper()

    url = os.path.join(url_root, crema)
    url = os.path.join(url, file_name)

    file_path = os.path.join(output_dir, file_name)

    response_json = get_plans(url)
    logging.info('REST_API completed: {}'.format(url))

    if generate_json_file:
        create_file(file_path + '.json', response_json)
        logging.info('file created: {}'.format(file_name + '.json'))

    return response_json


def get_list_of_plans(url='https://juicesoc.esac.esa.int/rest_api',
                      file_name='plan',
                      output_dir='./',
                      generate_json_file=True):
    """
    Create segmentation definition json file using REST_API

    :param url: rest-api url
    :param file_name: file name to get
    :param output_dir: output directory
    :param generate_json_file: flag to create a local copay of the json file
    """

    url = os.path.join(url, file_name)

    file_path = os.path.join(output_dir, file_name)

    response_json = get_plans(url)
    logging.info('REST_API completed: {}'.format(url))

    if generate_json_file:
        create_file(file_path + '.json', response_json)
        logging.info('file created: {}'.format(file_name + '.json'))

    return response_json


def get_plan_stats(id, url_root ='https://juicesoc.esac.esa.int/rest_api/plan',
                   file_name='stats',
                   output_dir='./',
                   generate_json_file=True):
    """
    Create segmentation definition json file using REST_API

    :param id: plan id within SHT Plans
    :param url: rest-api url
    :param file_name: file name to get
    :param output_dir: output directory
    :param generate_json_file: flag to create a local copay of the json file
    """

    url = os.path.join(url_root, str(id))
    url = os.path.join(url, file_name)

    file_path = os.path.join(output_dir, file_name)

    response_json = get_plans(url)
    logging.info('REST_API completed: {}'.format(url))

    if generate_json_file:
        create_file(file_path + '.json', response_json)
        logging.info('file created: {}'.format(file_name + '.json'))

    return response_json
