#!/usr/bin/env python
import sys
import subprocess
import logging

import os


def rreplace(s, old, new, occurrence):
    li = s.rsplit(old, occurrence)
    return new.join(li)

def call_command(command_list):
    try:
        output = subprocess.check_output(command_list)
        output = rreplace(output, '\n', '', 1)
        logging.info("AE has finished: '%s'" % output)
        return True
    except subprocess.CalledProcessError as e:
        logging.error("AE exited with an error status code: '%s'" % e)
    except OSError as e:
        logging.error("Error calling AE: '%s'" % e)
    finally:
        return False

def remove_file(path):
    try:
        os.remove(path)
        logging.info("Deleted file '%s'" % path)
    except OSError as e:
        logging.error("Could not delete file '%s': '%s'" % (path, e))

def on_created(src_path):
    success = call_command(['false', '||' 'echo OK'])
    if success:
        remove_file(src_path)

def main():
    logging.basicConfig(filename='automat.log', level=logging.INFO,
                        format='%(asctime)s %(levelname)s: %(message)s',
                        datefmt='%d.%m.%Y %H:%M:%S')

    event_type = sys.argv[1]
    object = sys.argv[2]
    src_path = sys.argv[3]

    logging.debug("Handling event '%s %s'" % (object, event_type))

    if (event_type == 'created'):
        logging.info("Handling new file '%s'" % src_path)
        on_created(src_path)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        msg = "Expected 3 arguments, got %s: %s " % (len(sys.argv), sys.argv)
        logging.error(msg)
        raise ValueError(msg)

    try:
        main()
    except:
        logging.error("Unexpected error: '%s'" % sys.exc_info()[0])
        raise
