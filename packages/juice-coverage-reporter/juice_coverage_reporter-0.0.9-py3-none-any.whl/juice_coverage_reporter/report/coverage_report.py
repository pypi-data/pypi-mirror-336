"""
Created on December 2023

@author: Claudio Munoz Crego (ESAC)

This Module allows to report Coverage metrics in a generic way
"""

import os
import sys
import shutil
import logging
import datetime
import numpy as np

from operator import itemgetter

from juice_coverage_reporter.commons.env_variables import EnvVar
from juice_coverage_reporter.report.report_methods import ReportMethod
from juice_coverage_reporter.report.rst_report import RstReport
from juice_coverage_reporter.report.plan_stats import PlanStats


def get_template_rst2pdf():
    """
    Get the rst2pdf.style template hosted in source code within templates sub-directory

    :return: rst2pdf.style  path
    :rtype: python path
    """

    here = os.path.abspath(os.path.dirname(__file__))
    template_file = os.path.join(here, 'templates')
    template_file = os.path.join(template_file, 'default_rst2pdf.style')

    if not os.path.exists(template_file):
        logging.error('reference template file "%s" missing' % template_file)
        sys.exit()

    logging.info('{} loaded'.format(template_file))

    return template_file


def get_template_docx():
    """
    Get the style.docx template hosted in source code within templates sub-directory

    :param: orientation_landscape: Flag to enforce A4 landscape orientation; default False
    :return: style.docx   path
    :rtype: python path
    """

    default_template = 'custom-reference.docx'

    here = os.path.abspath(os.path.dirname(__file__))
    template_file = os.path.join(here, 'templates')
    template_file = os.path.join(template_file, default_template)

    if not os.path.exists(template_file):
        logging.error('reference template file "%s" missing' % template_file)
        sys.exit()

    logging.info('{} loaded'.format(template_file))

    return template_file


class CoverageReporter(ReportMethod):
    """
    This class allows to report Coverage metrics
    """

    def __init__(self, config, mission_phases):

        super().__init__(config, mission_phases)

    def create_report(self):
        """
        Creates reports
        """

        logging.info('Start report')

        proc_report = self.report
        title = self.contents['title']

        proc_report.write_head(0, title.upper())
        proc_report.out.write('.. contents:: Table of Contents\n')

        proc_report.write_text('\n* Trajectory is {}.\n'.format(self.config["crema_id"]))

        for chapter in self.contents['chapters']:

            self.fill_generic_section(chapter, level=1)

        proc_report.print_summary_end()
        proc_report.rst_to_html()

        here = os.getcwd()
        os.chdir(self.output_dir)
        proc_report.pandoc_html_to_docx(docx_style_file=get_template_docx())

        if 'report_name' in list(self.config.keys()):
            if self.config['report_name']:
                self.report.rename_report(self.config['report_name'], just_rename=True)

        os.chdir(here)

        logging.info('End report')

