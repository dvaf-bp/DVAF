"""
DVAF -  offers the security-research community with up-to-date information
        about vulnerability trends, types, etc.

Copyright (C) 2019-2020
Nikolaos Alexopoulos <alexopoulos@tk.tu-darmstadt.de>,
Lukas Hildebrand <lukas.hildebrand@stud.tu-darmstadt.de>,
Jörn Schöndube <joe.sch@protonmail.com>,
Tim Lange <tim.lange@stud.tu-darmstadt.de>,
Moritz Wirth <mw@flanga.io>,
Paul-David Zürcher <mail@pauldavidzuercher.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.
"""
import os
import re
import argparse
from termcolor import colored
import inquirer
import time


def getListOfFiles(dirName):
    # create a list of file and sub directories
    # names in the given directory
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory
        if os.path.isdir(fullPath):
            allFiles += getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)

    return allFiles


def getFilesInDirectoryAnSubdirectory(path, ingorePattern, pattern):
    filesRet = []
    root = '.././'
    list_of_files_root = getListOfFiles(root)
    for file_walker in list_of_files_root:
        if re.match(
                pattern,
                file_walker) and not re.match(
            ingorePattern,
                file_walker):
            filesRet.append(os.path.join(file_walker))
    return filesRet


def prepLinesAsComment(filename, lines):
    with open(filename, 'r+') as f:
        patAndComments = {
            r".*\.py": ['"""', '"""'],
            r".*\.(js|jsx|cpp|c)": ['/*', '*/'],
            r".*\.(md|txt)": ['', ''],
            r".*\.html": ['<!--', '-->'],
            r".*\.scss": ['/*', '*/']
        }

        comment_start_and_end = []

        for pattern, comment_start_and_end_walker in patAndComments.items():
            if re.match(pattern, filename):
                comment_start_and_end = comment_start_and_end_walker

        if len(comment_start_and_end) == 0:
            print(
                colored("i have no idea"
                        " how to comment this thing Oo: " + filename, "red"))
            return

        content = f.read()
        f.seek(0, 0)
        f.write('\r\n'.join([comment_start_and_end[0]] + [lines] + [
            comment_start_and_end[1]]) + '\n' + content)


def loadCopyright():
    with open("../LICENSE_PREAMBLE") as copyrightFile:
        copyright_lines = copyrightFile.read()
        return copyright_lines


def appendCopyRightIfNotIn(files, copyright):
    fileToAddCopyright = []
    for file in files:
        with open(file) as inspectedFile:
            # first line is filetype specific comment
            # (e.g. python:'"""', js: '/*' )
            # then follows 2 copyright and one emty line => 4 before
            fifthLine = ""
            firstLine = ""
            inspectedFile_content = inspectedFile.readlines()
            if len(inspectedFile_content) >= 5:
                fifthLine = inspectedFile_content[4]
                firstLine = inspectedFile_content[0]

        if not fifthLine.startswith("Copyright") and "no-automatic-copyright-generation" not in firstLine:
            fileToAddCopyright.append(file)
    return fileToAddCopyright


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('--root',
                        help='where to root the file search (default: .././)',
                        type=str,
                        default=".././")
    parser.add_argument('--pattern', help='pattern for path to catch ',
                        type=str,
                        default=r".*(\.py|\.txt|\.js|\.md|\.c|\.cpp|\.scss)")
    parser.add_argument(
        '--ignore',
        help='patterns for path to ignore',
        type=str,
        default=r".*(/node_modules/.*|__pycache__.*|"
        r"\.public/.*|/build/.*|\.png|\.jpg|/.*/\..*)|.*(\.json|\.sh"
        r"|license\.md|robots.txt|cvecollector/.*|resources/.*|requirements.txt)")

    parser.add_argument('--confirm',
                        action='store_true')
    args = parser.parse_args()

    filesAccToPatt = getFilesInDirectoryAnSubdirectory(
        args.root, args.ignore, args.pattern)
    copyrightlines = loadCopyright()
    filesMissCR = appendCopyRightIfNotIn(filesAccToPatt,
                                         copyrightlines)

    if not args.confirm and len(filesMissCR) > 0:
        questions = [
            inquirer.Checkbox(
                'filesToCopyWRight',
                message="Please confirm that exactly these files"
                        "need CR Info :) \n use <Space> to select"
                        "and <enter> to start adding copyright info",
                choices=filesMissCR,
                default=filesMissCR)]

        filesMissCR = inquirer.prompt(questions)["filesToCopyWRight"]
    elif len(filesMissCR) == 0:
        print(colored("no files according to pattern,"
                      "needing Copyright clauses found", "green"))
    elif args.confirm:
        print(colored("Files Needing CR-Clause found:",
                      "green"))
        for filePath in filesMissCR:
            print("\t - " + filePath)
        print(colored("Bypassing conformation due to --confirm in 10s",
                      "magenta"))
        for i in reversed(range(10)):
            time.sleep(1)
            print(str(i) + "...")

    for file in filesMissCR:
        prepLinesAsComment(file, copyrightlines)
    print(colored("licensing is done :)", "green"))

    if(len(filesMissCR) > 0):
        exit(1)
