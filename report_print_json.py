#!/usr/bin/env python
import os.path
import argparse
import json

# Coming from Puppetlabs/puppet lib/puppet/util/colors.rb
COLORS = {
  'BLACK':      "\033[0;30m",
  'RED':        "\033[0;31m",
  'GREEN':      "\033[0;32m",
  'YELLOW':     "\033[0;33m",
  'BLUE':       "\033[0;34m",
  'MAGENTA':    "\033[0;35m",
  'CYAN':       "\033[0;36m",
  'WHITE':      "\033[0;37m",
  'HBLACK':     "\033[1;30m",
  'HRED':       "\033[1;31m",
  'HGREEN':     "\033[1;32m",
  'HYELLOW':    "\033[1;33m",
  'HBLUE':      "\033[1;34m",
  'HMAGENTA':   "\033[1;35m",
  'HCYAN':      "\033[1;36m",
  'HWHITE':     "\033[1;37m",
  'BG_RED':     "\033[0;41m",
  'BG_GREEN':   "\033[0;42m",
  'BG_YELLOW':  "\033[0;43m",
  'BG_BLUE':    "\033[0;44m",
  'BG_MAGENTA': "\033[0;45m",
  'BG_CYAN':    "\033[0;46m",
  'BG_WHITE':   "\033[0;47m",
  'BG_HRED':    "\033[1;41m",
  'BG_HGREEN':  "\033[1;42m",
  'BG_HYELLOW': "\033[1;43m",
  'BG_HBLUE':   "\033[1;44m",
  'BG_HMAGENTA':"\033[1;45m",
  'BG_HCYAN':   "\033[1;46m",
  'BG_HWHITE':  "\033[1;47m",
  'RESET':      "\033[0m",
}

COLORMAP = {
    'debug':  'WHITE',
    'info':   'GREEN',
    'notice': 'CYAN',
    'warning':'YELLOW',
    'err':    'HMAGENTA',
    'alert':  'RED',
    'emerg':  'HRED',
    'crit':   'HRED',
}

class ReportPrint:
    def run(self):
        options = self.parse_args()
        self.start(options)


    def start(self, options):
        self.options = options
        for file_path in options.files:
            self.print_file(file_path)

    def print_file(self, file_path):
        if not os.path.isfile(file_path):
            raise Exception('%s is not a file' % file_path)
        with open(file_path, 'r') as stream:
            data = json.load(stream)
        for log_message in data['logs']:
            self.print_message(log_message)

    def print_message(self, log_message):
        if self.options.exclude is not None and log_message['level'] in self.options.exclude:
            return
        print("%s %s%s: %s: %s%s" % (
            log_message['time'],
            COLORS[COLORMAP[log_message['level']]],
            log_message['level'],
            log_message['source'],
            log_message['message'],
            COLORS['RESET'],
        ))

    def parse_args(self):
        parser = argparse.ArgumentParser(description='Print logs from puppet json reports')
        parser.add_argument('--exclude', metavar='exclude', nargs='*',
                            help='log level to exclude')
        parser.add_argument('files', metavar='file', nargs='+',
                            help='a puppet report file in json format')
        return parser.parse_args()


if __name__ == "__main__":
    ReportPrint().run()
