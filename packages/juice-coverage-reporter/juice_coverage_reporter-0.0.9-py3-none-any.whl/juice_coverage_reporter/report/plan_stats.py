"""
Created on March, 2022

@author: Claudio Munoz Crego (ESAC)

This Module allows to handle SHT plans and statistics

"""

import os
import sys
import logging
import datetime
import pandas as pd

from juice_coverage_reporter.commons.sht_rest_api import get_list_of_plans, get_plan_stats


class PlanStats(object):
    """
    This Class allows read and parse segment definition file
    """

    def __init__(self, output_dir="./", plan_name=""):

        self.output_dir = output_dir

        self.list_of_plans = self.get_list_of_plans()

        self.plan_name = plan_name

    def get_list_of_plans(self):

        list_of_plans = get_list_of_plans(output_dir=self.output_dir)

        return list_of_plans

    def get_plan_stats(self):

        id = self.get_plan_id(self.plan_name)

        if id is None:
            logging.error('Plan "{}" does not exist in SHT "https://juicesoc.esac.esa.int/rest_api/plan"'.format(
                self.plan_name))
            sys.exit()

        else:

            stats = get_plan_stats(id, output_dir=self.output_dir)

        return stats

    def get_plan_id(self, plan_mnemonic):

        plan_id = None

        for p in self.list_of_plans:

            if p['name'] == plan_mnemonic:

                plan_id = p['id']
                break

        return plan_id
