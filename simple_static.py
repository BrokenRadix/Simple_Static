#!/usr/bin/python

import argparse
import logging
import os
import shutil
from datetime import datetime
from shutil import copytree

parser = argparse.ArgumentParser(
    description='Simple Static: Create a static website in a single command.'
)
parser.add_argument(
    '-v', '--verbose', action='store_true', help='display debug messages'
)
parser.add_argument(
    '-db', '--disable',
    action='store_true', help='disable automatic "build" directory backups'
)
args = parser.parse_args()

# display debug messages
if args.verbose:
    logging.basicConfig(level=logging.DEBUG)

# some general variables
valid_file_ext = ".html"
open_element_tag = "#### "
close_element_tag = " ####"

# the required directories
build_dir = "./build"
source_dir = "./source"
assets_dir = source_dir + "/assets"
elements_dir = source_dir + "/elements"
pages_dir = source_dir + "/pages"

# the required files
header_file = elements_dir + "/header.html"
footer_file = elements_dir + "/footer.html"
index_file = pages_dir + "/index.html"

# check for the build dir, and back it up, or build it.
if os.path.exists(build_dir) and os.path.isdir(build_dir):
    backup_dir = "%s.%s.bak" % (
        build_dir,
        datetime.now().strftime('%Y%m%d_%H%M%S')
    )
    # check for disabled backup, if no backup, remove build dir
    if not args.disable:
        logging.debug("Moving %s to %s" % (build_dir, backup_dir))
        os.rename(build_dir, backup_dir)
    else:
        logging.debug("Removing %s" % build_dir)
        shutil.rmtree(build_dir)
elif os.path.exists(build_dir) and os.path.isfile(build_dir):
    logging.error("Found %s, but it's not a directory... Exiting." % build_dir)
    exit(0)

# check for the required dirs/files, make them if needed
required_dirs = (source_dir, assets_dir, elements_dir, pages_dir)
for directory in required_dirs:
    if not os.path.exists(directory):
        logging.debug(
            "No '%s' directory, creating one at: %s" % (directory, directory)
            )
        os.makedirs(directory)
    if not os.path.isdir(directory):
        logging.error(
            "Found %s, but it's not a directory... Exiting." % directory
            )
        exit(0)
required_files = (
    header_file, footer_file, index_file
)
for file in required_files:
    if not os.path.exists(file):
        logging.debug("No '%s' file, creating one at: %s" % (file, file))
        open(file, 'w')
    if not os.path.isfile(file):
        logging.error("Found %s, but it's not a file... Exiting." % file)
        exit(0)

# get list of all files in 'elements'
# assumes all good files end in valid_file_ext
# also, use the amount of characters to strip off
elements_files = {
    file[:(len(valid_file_ext) * -1)]: file for file in os.listdir(
        elements_dir
    ) if os.path.isfile(
        os.path.join(elements_dir, file)
    ) and file.endswith(valid_file_ext)
}

# copy the entire pre-parsed pages dir to build
copytree(pages_dir, build_dir)

# recursively get all the pre-parsed files in 'build'
pages_files = []
for root, directories, filenames in os.walk(build_dir):
    for filename in filenames:
        path = os.path.join(root, filename)
        if os.path.isfile(path):
            pages_files.append(path)

# parse all pages, filling in elements HTML when called
for page_file in pages_files:
    # get all the content of the file
    current_file = open(page_file, "r")
    current_file_content = current_file.read()
    current_file.close()

    # loop through each of the elements
    for element_key, element_file in elements_files.iteritems():
        # get the element's content
        element_file = open("%s/%s" % (elements_dir, element_file), "r")
        element_file_content = element_file.read()
        element_file.close()
        # if the element key is found, write to the "build" content
        current_file_content = current_file_content.replace(
            "%s%s%s" % (open_element_tag, element_key, close_element_tag),
            element_file_content
        )
    # end for elements

    # write the content to the file
    current_file = open(page_file, "w")
    current_file.write(current_file_content)
    current_file.close()
# end for pages

# copy the entire assets dir to build
copytree(assets_dir, "%s/%s" % (
    build_dir, os.path.basename(os.path.normpath(assets_dir)))
    )

logging.debug("Done: created %s" % build_dir)
