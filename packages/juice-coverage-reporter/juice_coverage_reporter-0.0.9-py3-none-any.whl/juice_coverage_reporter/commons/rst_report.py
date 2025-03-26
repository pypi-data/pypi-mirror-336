"""
Created on February, 2018

@author: Claudio Munoz Crego (ESAC)

This Module allows to generate an rst report
"""

import logging
import os
import sys

from esac_juice_pyutils.commons.rst_handler import RstHandler


class RstReport(RstHandler):
    """
    This class allows to generate an rst report
    """

    def __init__(self, input_path, output_path='', out=sys.stdout):
        """
        :param output_path:
        :param out:
        :param input_path: path of directory containing plots
        """

        if not os.path.exists(input_path):
            logging.error('input path "{}" does not exist'.format(input_path))
        else:
            self.input_path = os.path.abspath(os.path.expandvars(input_path))

        if output_path == '':
            output_path = self.input_path
            if not os.path.exists(output_path):
                logging.error('output path "{}" does not exist'.format(output_path))

        self.output_dir = output_path

        super(RstReport, self).__init__(output_path, out)

    def print_summary_intro(self, title='Title', objective_summary='', metrics=[]):
        """
        Produces summary intro

        :objectif_summary: summary of the objective of study
        """

        # self.write_head_chapter(title.upper())
        self.write_head(0, title.upper())
        self.out.write('.. contents:: Table of Contents\n')
        # self.out.write('\n.. section - numbering::\n\n')

        # self.write_head_section('Introduction')
        self.insert_page_break()
        self.write_head(1, 'Introduction')
        intro = ("\n"
                 ".. |date| date::\n"
                 ".. |time| date:: %H:%M:%S\n"
                 "\n"
                 "This document was automatically generated on |date| at |time|.\n\n")

        self.out.write(intro)

        self.out.write('\n' + objective_summary + '\n')
        if len(metrics) > 0:
            # self.print_rst_metrics_summary_table([['uno', 1.00,'unit']])
            self.print_rst_table(metrics)

    def print_summary_end(self):
        """
        Produces summary end
        """

        self.out.close()

        logging.info('rst file {} generated'.format(self.rst_file_name))

    def print_summary_section(self, n_level, title, objective_summary='', metrics=[], figure=[]):
        """
        Produces subsection

        :param n_level: number form 0 to 6
        :param title: section level
        :param objective_summary: objective summary of the section
        :param metrics: metric table (list of list)
        :param figure: list of figure
        :return:
        """

        # self.write_head_subsection(title)
        self.write_head(n_level, title)
        self.out.write('\n' + objective_summary + '\n\n')

        if len(metrics) > 0:
            # self.print_rst_metrics_summary_table([['uno', 1.00,'unit']])
            self.print_rst_table(metrics)

        if len(figure) > 0:
            for fig in figure:
                fig = os.path.expandvars(fig)
                if not os.path.exists(fig):
                    logging.error('input path "{}" does not exist'.format(fig))
                else:
                    self.rst_insert_figure(fig, title=title, text=objective_summary)

    def print_summary_subsection(self, title, objective_summary='', metrics=[], figure=[]):
        """
        Produces summary intro

        :objectif_summary: summary of the objective of study
        """

        self.write_head_subsection(title)
        self.out.write('\n' + objective_summary + '\n')

        if len(metrics) > 0:
            # self.print_rst_metrics_summary_table([['uno', 1.00,'unit']])
            self.print_rst_table(metrics)

        if len(figure) > 0:
            for fig in figure:
                fig = os.path.expandvars(fig)
                if not os.path.exists(fig):
                    logging.error('input path "{}" does not exist'.format(fig))
                else:
                    self.rst_insert_figure(fig, title=title, text=objective_summary)

    def print_summary_sub_subsection(self, title, objective_summary='', metrics=[], figure=[]):
        """
        Produces summary intro

        :objectif_summary: summary of the objective of study
        """

        self.write_head_subsubsection(title)
        self.out.write('\n' + objective_summary + '\n')

        if len(metrics) > 0:
            self.print_rst_csv_table(metrics, title)
            self.out.write('\n')

        if len(figure) > 0:
            for fig in figure:
                fig = os.path.expandvars(fig)
                self.rst_insert_figure(fig, title=title, text=objective_summary)

    def create_plot_pie(self, plots_path, title, percent, min_values=0):
        """
        Create pie plot

        :param min_values: the min value to plot, i.e. 0.01 %; mainly remove too small values
        :param plots_path:
        :param title:
        :param percent:
        :return:
        """

        import matplotlib.pyplot as plt

        percent_keys = list(percent.keys())
        for k in reversed(percent_keys):
            if percent[k] < min_values:
                del percent[k]

        labels = sorted(percent.keys())
        sizes = [percent[k] for k in labels]
        labels = ['{} [{}%]'.format(k, percent[k]) for k in labels]
        explode = [i % 2 * 0.1 for i, x in enumerate(percent.keys())]

        pies = plt.pie(sizes, startangle=90, autopct='%1.0f%%', pctdistance=0.9, radius=1.2,
                       explode=explode)

        plt.legend(pies[0], labels, bbox_to_anchor=(1, 0.5), loc="center right", fontsize=8,
                   bbox_transform=plt.gcf().transFigure)
        plt.subplots_adjust(left=0.0, bottom=0.1, right=0.50)

        plt.axis('equal')
        plot_file_path = os.path.join(plots_path, title + '.png')
        plt.savefig(plot_file_path)
        plt.close()

        return plot_file_path

    def print_rst_table_2(self, metrics, title=True, return_line_sep='\\n'):
        """
        Generate (print) a table in rst format

        :param title: flag which specify if the table have a title line or not.
        :param metrics: list of table lines, if title=True, the title must be in metrics[0]
        :param out: unit where to write report summary
        :return:
        """

        self.out.write('\n')

        d = [0] * len(metrics[0])

        extended_metrics = []
        for line in metrics:
            nb_of_next_line = 0
            for cell in line:
                if not isinstance(cell, str):  # avoid non string casting them str
                    cell = str(cell)
                if cell.count(return_line_sep) > nb_of_next_line:
                    nb_of_next_line = cell.count(return_line_sep)

            columns = []
            # print(line)
            n_col = len(line)

            for i in range(n_col):
                cell = line[i]
                if not isinstance(cell, str):  # avoid non string casting them str
                    cell = str(cell)
                # print(cell)
                column = [''] * (nb_of_next_line + 1)
                sub_lines = cell.split(return_line_sep)
                sub_lines = [str(ele) for ele in sub_lines]
                if len(max([str(ele) for ele in sub_lines], key=len)) > d[i]:
                    d[i] = len(max([str(ele) for ele in sub_lines], key=len))
                column[:len(sub_lines)] = sub_lines
                columns.append(column)

            rows = [list(i) for i in zip(*columns)]
            extended_metrics.append(rows)

        metrics = extended_metrics

        table_title_format = '|'
        table_line_format = '|'

        for i in range(len(metrics[0][0])):  # we use the first line of the title (Most of time there is only one)

            table_title_format += ' {' + str(i) + ':' + str(d[i]) + 's} |'
            table_line_format += ' {' + str(i) + ':' + str(d[i]) + 's} |'
        table_title_format += '\n'
        table_line_format += '\n'

        table_line = ''
        table_line_title = ''
        for i in range(len(d)):
            table_line += '+{}'.format('-' * (d[i] + 2))
            table_line_title += '+{}'.format('=' * (d[i] + 2))

        table_line += '+\n'
        table_line_title += '+\n'

        if title:
            self.out.write(table_line)

            for ele in metrics[0]:
                print(table_title_format.format(*ele))
                self.out.write(table_title_format.format(*ele))
            self.out.write(table_line_title)

            metrics.pop(0)

        else:
            self.out.write(table_line)

        for ele in metrics:
            for sub_ele in ele:
                # print(table_line_format.format(*sub_ele))
                self.out.write(table_line_format.format(*sub_ele))
            self.out.write(table_line)

        self.out.write('\n')

