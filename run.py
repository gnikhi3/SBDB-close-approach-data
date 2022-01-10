#! /usr/bin/env python
import argparse
import pytest
import logging as log
import os

PARSER = argparse.ArgumentParser()
ARGS = None


def get_args():
    global ARGS
    if not ARGS:
        ARGS, unknown_args = PARSER.parse_known_args()
        if unknown_args:
            log.info("Ignoring unrecognized input options %s", unknown_args)
    return ARGS


# arg PARSER
PARSER.add_argument('--keyword', default='test', type=str, help='Keyword to pass to pytest to run specific tests')
PARSER.add_argument('--pytest-args', default='', type=str, help='Args to pass to pytest')
# todo: smoke tests and various other test markers can be added as and when required
# PARSER.add_argument('--smoke-test', action='store_true', help='Run Smoke Tests')
ARGS = get_args()


def set_test_schedule():
    args = ['cases', '-vs', '--instafail', '-rx', '--html=report.html', '--capture=tee-sys']
    # todo: can uncomment the below code when smoke tests are marked
    # if ARGS.smoke_test:
    #     args.append('-m smoke_test')
    #     log.info("running only smoke tests")
    if ARGS.keyword:
        args.append('-k {}'.format(ARGS.keyword))
        log.info("running regressions with keyword: {}".format(ARGS.keyword))
    if ARGS.pytest_args:
        args.append(ARGS.pytest_args.strip())
        log.info("running pytest with arguments: {}".format(ARGS.pytest_args))
    print(args)
    return args


def main():
    # Remove data file if already exists
    report_file = '{}/report.html'.format(os.getcwd())
    if os.path.exists(report_file):
        os.remove(report_file)
    pytest.main(set_test_schedule())


if __name__ == "__main__":
    main()