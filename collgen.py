#!/usr/bin/python
#-*- encoding: utf-8 -*-


import sys
import os
from optparse import OptionParser


from libkindle.collection import *


def get_args():
    parser = OptionParser(description=("Generates collections.json file from "
                                       "a given path. Calculates collections "
                                       "based on the directory structure where "
                                       "books reside"))
    parser.add_option('-d', '--book-directory',
                      help=("Book directory which is used to "
                            "generate collections.json from"))
    parser.add_option('-o', '--output-json-path',
                      default='./',
                      help=("Location where collections.json will be generated"))

    (options, args) = parser.parse_args()

    if(not os.path.isdir(options.book_directory)):
        print >> sys.stderr, ("Error: --book-directory does not "
                              "exists or not a directory: %s")\
                             % options.book_directory
        sys.exit(1)
    if(not os.path.isdir(options.output_json_path)):
        print >> sys.stderr, ("Error: --output-json-path does not "
                              "exists or not a directory: %s")\
                             % options.output_json_path
        sys.exit(1)

    return (options, args)


def main():
    (options, args) = get_args()
    book_directory = os.path.abspath(options.book_directory)
    output_json_path = os.path.abspath(options.output_json_path)

    collections_json = BookCollector(book_directory).collections_json
    output_file_path = os.path.join(output_json_path, COLLECTIONS_FILENAME)
    try:
        open(output_file_path, 'w').write(collections_json)
    except Exception, err:
        print >> sys.stderr, "Error: Could not write json file: %s" % str(err)
        sys.exit(1)

    print "Collections file written to:\n%s" % output_file_path


if(__name__ == '__main__'):
    main()
