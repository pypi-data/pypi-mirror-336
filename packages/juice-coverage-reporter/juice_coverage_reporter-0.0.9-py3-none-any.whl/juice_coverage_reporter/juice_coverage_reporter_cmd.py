"""
Created on October 2022

@author: Claudio Munoz Crego (ESAC)

This Module generates a Juice's Coverage Report
"""

import argparse
import logging
import os
import signal
import sys

from esac_juice_pyutils.commons.my_log import setup_logger
from esac_juice_pyutils.commons import json_handler as my_json

from juice_coverage_reporter.commons.env_variables import EnvVar
from juice_coverage_reporter.report.coverage_report import CoverageReporter
from juice_coverage_reporter import version


def func_signal_handler(signal, frame):
    logging.error("Aborting ...")
    logging.info("Cleanup not yet implemented")
    sys.exit(0)


def parse_options():
    """
    This function allow to specify the input parameters
    - OutputDir: path of the Output directory
    - JsonFile: path of the configuration file
    - loglevel: debug, info
    :returns args; argument o parameter list passed by command line
    :rtype list
    """

    parser = argparse.ArgumentParser()

    parser.add_argument("-c", "--JsonFile",
                        help="Path of JsonFile defining report(s) required",
                        required=True)

    parser.add_argument("-l", "--loglevel",
                        help=" Must be debug, info ",
                        required=False)

    parser.add_argument("-v", "--version",
                        help="return version number and exit",
                        action="version",
                        version='%(prog)s {}'.format(version))

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit()

    return args


def main():
    """
        Entry point for processing
        """

    signal.signal(signal.SIGINT, func_signal_handler)

    args = parse_options()

    if args.loglevel:
        if args.loglevel in ['info', 'debug']:
            setup_logger(args.loglevel)
        else:
            setup_logger()
            logging.warning(
                'log level value "{0}" not valid (use debug);  So default INFO level applied'.format(args.loglevel))
    else:
        setup_logger()

    if args.JsonFile:
        if not os.path.exists(args.JsonFile):
            logging.error('Configuration File "{}" does not exist'.format(args.JsonFile))
            sys.exit(0)
        else:
            cfg_file = os.path.abspath(args.JsonFile)

    else:
        logging.error('Please define Coverage Configuration File')
        sys.exit(0)

    here = os.path.abspath(os.path.dirname(__file__))
    working_dir = os.path.dirname(cfg_file)

    cfg = my_json.load_to_dic(cfg_file)

    cfg_main = cfg['main']
    crema_id = cfg['main']['crema_id']
    if 'env_var' in list(cfg_main.keys()):

        env_var = EnvVar(cfg_main['env_var'])

        for k, v in cfg['main'].items():

            if isinstance(v, str) and "$" in v:
                cfg['main'][k] = env_var.subsitute_env_vars_in_path(v)

        for section in list(cfg['input'].keys()):

            for k, v in cfg['input'][section].items():

                if isinstance(v, str):

                    v = env_var.subsitute_env_vars_in_path(v)
                    v = v.replace("crema_x_y", crema_id).replace("crema_X_Y", crema_id)

                    cfg['input'][section][k] = v

    os.chdir(working_dir)

    p = CoverageReporter(cfg, working_dir)
    p.create_report()

    os.chdir(here)
    logging.debug('goto root original directory: {}'.format(here))


def debug():
    """
    debug: Print exception and stack trace
    """

    err = sys.exc_info()
    print("type: %s" % err[0])
    print("Msg: %s" % err[1])
    import traceback
    traceback.print_exc(err[2])
    traceback.print_tb(err[2])


if __name__ == "__main__":

    try:
        main()
    except SystemExit as e:
        print(e)
        print("<h5>Internal Error. Please contact JUICE SOC </h5>")
        raise

    sys.exit(0)
