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
from juice_coverage_reporter.report.rst_report import RstReport
from juice_coverage_reporter.report.plan_stats import PlanStats


class ReportMethod(object):
    """
    This class allows to report Coverage metrics
    """

    def __init__(self, config, mission_phases):

        self.config = config['main']
        self.env_var = EnvVar(self.config['env_var'])
        self.input = config['input']
        self.contents = config['contents']
        self.crema = self.config['crema_id']
        self.output_dir = self.config['output_dir']
        self.plots_path = os.path.join(self.output_dir, 'plots')
        if os.path.exists(self.plots_path):
            shutil.rmtree(self.plots_path)
        os.makedirs(self.plots_path)

        self.report = RstReport(self.plots_path, out='rst', output_path=self.output_dir)

    def fill_statistics(self, level=1):
        """
        Fill Statistics chapter

        :param level: level of head section; chapter is level=1
        """

        proc_report = self.report

        plan_stats = PlanStats(output_dir=self.output_dir, plan_name=self.config['plan_name'])

        stats = plan_stats.get_plan_stats()

        proc_report.write_head(level + 1, "Plan info")

        metrics_summary = [['Plan Name', self.config['plan_name']],
                           ['Number of Segments', stats['segment_number']],
                           ['Start', stats['start']],
                           ['End', stats['end']],
                           ]

        proc_report.print_rst_table(metrics_summary)

        proc_report.write_head(2, "Working Group Summary info")

        sum_total_seconds = 0
        for k, v in stats['stats']['working_group_stats'].items():
            sum_total_seconds += v

        metrics_working_groups = [['Working Group', 'total time [sec] ', 'total time [dTH:M:S]', '%']]
        for k in sorted(stats['stats']['working_group_stats'].keys()):
            v = stats['stats']['working_group_stats'][k]
            v_dthms = sec_2_dhms(v)
            metrics_working_groups.append([k, v, v_dthms, round(v / sum_total_seconds * 100, ndigits=2)])

        proc_report.print_rst_table(metrics_working_groups)

        proc_report.write_text('\nNote: "Generic" means operation and Downlinks\n')

        proc_report.write_head(level, "Annex")
        proc_report.write_head(level + 1, "Segment Summary")

        metrics_segment_definition = [['Segments', 'total time [sec] ', 'total time [dTH:M:S]', '%']]
        for k in sorted(stats['stats']['segment_definition_stats'].keys()):
            v = stats['stats']['segment_definition_stats'][k]
            v_dthms = sec_2_dhms(v)
            metrics_segment_definition.append([k, v, v_dthms, round(v / sum_total_seconds * 100, ndigits=2)])

        proc_report.print_rst_table(metrics_segment_definition)

    def fill_generic_section(self, section, level=1):
        """
        Fill Coverage section

        :param section: section information
        :param level: level of head section; chapter is level=1
        """

        proc_report = self.report

        proc_report.write_head(level, section['title'])

        if section['text']:
            text = ''.join(section['text'])
            proc_report.write_text(f'\n{text}\n')

        if 'input_id' in list(section.keys()):

            self.fill_input_id(section['title'], section['input_id'], level=level)

        if 'plot_files' in list(section.keys()):

            for plots in section['plot_files']:
                self.insert_plot_files(plots, level)

    def fill_input_id(self, section_title, input_id, level=1):
        """
        Fill specific sections

        :param section_title: section title
        :param input_id: specific identifier
        :param level: section title header level
        :return:
        """

        if input_id == 'coverage_statistics':

            self.fill_statistics(level=level)

        elif input_id == 'segmentation_moon_coverage_plots':

            self.fill_segmentation_moon_coverage_plots(self.input[input_id], level=level)

        elif input_id == 'segment_coverage_plots':

            self.fill_segment_coverage_plots(self.input[input_id], level=level)

        elif input_id == 'main_parameters_geopipeline':

            self.fill_geopipeline_plots(self.input[input_id], level=level)

        else:

            logging.warning(f'Undefined input_id "{input_id}" for section {section_title}')

    def insert_plot_files(self, plot_files, level):
        """
        insert plot files

        :param plot_files: structure including plot parameters
        :param level: sub-section level
        """

        input_path = plot_files['path']

        input_path = input_path.replace('crema_x_y', self.crema).replace('crema_X_Y', self.crema)
        input_path = self.env_var.subsitute_env_vars_in_path(input_path)

        if not os.path.exists(input_path):

            logging.error(f'path does not exist: {input_path}')
            sys.exit()

        elif os.path.isdir(input_path):

            self.insert_list_of_plot_file(input_path, plot_files, level)

        else:  # is a file

            self.insert_plot_file(input_path, plot_files, level)

    def insert_list_of_plot_file(self, input_path, plot_files, level):
        """
        Insert a list of plot files from a given directory after filtering using sub-strings

        notes: captions and title are derived from file names

        :param input_path: plot path
        :param plot_files: structure including plot parameters
        :param level: sub-section level
        """

        list_of_plot_paths = [f for f in os.listdir(input_path) if
                              os.path.isfile(os.path.join(input_path, f))]

        if "path_filter" in list(plot_files.keys()):

            new_list_of_plot_paths = []
            for f in list_of_plot_paths:

                file_to_select = True
                for str in plot_files['path_filter']:

                    if (str.startswith('!') and str in f) or str not in f:
                        file_to_select = False
                        break

                if file_to_select:
                    new_list_of_plot_paths.append(f)

            list_of_plot_paths = new_list_of_plot_paths

        for f in list_of_plot_paths:
            f_path = os.path.join(input_path, f)
            plot_title = f.split('.')[0].split('_')
            plot_title = ' '.join(plot_title).capitalize()

            description = plot_title

            self.report.write_head(level + 1, plot_title)

            source = f_path
            dst = os.path.join(self.plots_path, f)
            shutil.copy(source, dst)

            self.report.rst_insert_figure(dst, description, text='')

    def insert_plot_file(self, input_path, plot_files, level):
        """
        Insert specific plot file including specific caption, title

        :param input_path: plot path
        :param plot_files: structure including plot parameters
        :param level: sub-section level
        """

        file_name = os.path.basename(input_path)
        plot_title = file_name.split('.')[0].split('_')
        plot_title = ' '.join(plot_title).capitalize()

        description = plot_title
        if "caption" in list(plot_files.keys()):
            description = plot_files['caption']

        if "title" in list(plot_files.keys()):

            if plot_files['title'] == '*':
                title = description.capitalize()
            elif plot_files['title'] == '':
                title = plot_title.capitalize()
            else:
                title = plot_files['title'].capitalize()

            self.report.write_head(level + 1, title)

        dst = os.path.join(self.plots_path, file_name)
        shutil.copy(input_path, dst)

        self.report.rst_insert_figure(dst, description, text='')


def sec_2_dhms(number_of_seconds, return_dhms=True):
    nb_days, rest_days = divmod(number_of_seconds, 86400)
    nb_hours, rest_hours = divmod(rest_days, 3600)
    nb_minutes, rest_minutes = divmod(rest_hours, 60)
    nb_seconds = rest_minutes

    # print(f"Day {nb_days} |Hour {nb_days} |Min {nb_minutes} |Sec {nb_seconds}")

    if return_dhms:

        return '%03dT%02d:%02d:%02d' % (nb_days, nb_hours, nb_minutes, nb_seconds)

    else:

        return nb_days, nb_hours, nb_minutes, nb_seconds
