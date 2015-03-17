#! /usr/bin/env python2

import os
import sys
import argparse
import time
import snotes_persistence

config_dir = os.path.expanduser('~/.snotes')
data_file = "snotes.data"


def err_write(msg):
    sys.stderr.write(msg)


def init():
    if os.path.exists(config_dir):
        if not os.path.isdir(config_dir):
            err_write('{0} exists and is not a directory\n'.format(config_dir))
            sys.exit(1)
    else:
        os.makedirs(config_dir)
        os.chdir(config_dir)
        with open(data_file, 'w') as f:
            f.write('\n')
    os.chdir(config_dir)

def add(args):
    current_time = time.time()
    entry = snotes_persistence.Entry(current_time,
                                     current_time,
                                     args.tags,
                                     ' '.join(args.note))
    global journal
    journal.add_or_merge_entry(entry)
    journal.to_file(data_file)

def get(args):
    global journal
    entries = journal.get_entries(
        lambda entry:snotes_persistence.filter_tags_inclusive(args.tags, entry.tags),
        lambda entry:entry.update_timestamp
    )
    for entry in entries:
        print entry.value
    
init()
arg_parser = argparse.ArgumentParser()
action_parsers = arg_parser.add_subparsers()
get_action = action_parsers.add_parser('get')
get_action.add_argument('-t', '--tags', nargs='+')
get_action.set_defaults(func=get)
add_action = action_parsers.add_parser('add')
add_action.add_argument('-t', '--tags', nargs='+')
add_action.add_argument('-n', '--note', nargs='+')
add_action.set_defaults(func=add)
args = arg_parser.parse_args()
journal = snotes_persistence.Journal.from_file(data_file)
args.func(args)
