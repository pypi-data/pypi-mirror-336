"""
Created on May, 2021

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle SHT rest-api

"""
import logging


from juice_coverage_reporter.commons.sht_rest_api import get_plan_stats, get_list_of_plans


def test_get_plans():

    url = 'https://juicesoc.esac.esa.int/rest_api/'
    url_2 = 'https://juicesoc.esac.esa.int/rest_api/plan/58/stats'
    file_name = 'plan'
    file_name2 = 'stats'


    stats_json = get_plan_stats(url_2, file_name2)


    plan_json = get_list_of_plans(url, file_name)


if __name__ == '__main__':

    import os

    from esac_juice_pyutils.commons.my_log import setup_logger

    here = os.path.abspath(os.path.dirname(__file__))
    test_dir = os.path.dirname(here)

    print(here)
    print(test_dir)

    setup_logger('debug')
    print(os.getcwd())

    print('\n-----------------------------------------------\n')

    logging.info('Start of test ...')

    test_get_plans()

    # "curl -X GET "https://juicesoc.esac.esa.int/rest_api/trajectory/CREMA_3_0/segment_definition" -H  "accept: application/json

    logging.info('End test!')

