# Copyright 2017 Adrian-Ioan Gărovăț, Emanuel Covaci, Sebastian-Valeriu Maleș
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
# Copyright 2017 Adrian-Ioan Gărovăț, Emanuel Covaci, Sebastian-Valeriu Maleș
#
# This file is part of WebsiteISJ
#
# WebsiteISJ is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# WebsiteISJ is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
#Copyright 2017 Adrian-Ioan Gărovăț, Emanuel Covaci, Sebastian-Valeriu Maleș
#
#This file is part of WebsiteISJ
#
#WebsiteISJ is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#WebsiteISJ is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
#Copyright 2017 Adrian-Ioan Gărovăț, Emanuel Covaci, Sebastian-Valeriu Maleș
#
#This file is part of WebsiteISJ
#
#WebsiteISJ is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#
#WebsiteISJ is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with WebsiteISJ.   If not, see <http://www.gnu.org/licenses/>.
import os
import argparse
parser = argparse.ArgumentParser(description="This script is used to append comments to .py and .html extensions")

parser.add_argument('-n', action="store", dest="dirname", help="Store the name of the directory", type=str)
parser.add_argument('-c', action="store", dest="comment", help="Store the comment to be appended", type=str)


def line_appender(filename_path, lines):
    if os.path.exists(filename_path):
        if os.path.isfile(filename_path):
            with open(filename_path, "r+") as file:
                if filename_path.endswith(".py"):
                    file_content = file.read()
                    file.seek(0, 0)
                    for line in lines:
                        file.write("# " + line.rstrip('\r\n') + "\n")
                    file.write(file_content)
                elif filename_path.endswith(".html"):
                    file_content = file.read()
                    file.seek(0, 0)
                    for line in lines:
                        file.write("<!--" + line.rstrip('\r\n') + "-->" + "\n")
                    file.write(file_content)
        else:
            print("This is not a file")
    else:
        print("File dosen't exists")


def direct_appender(directory_path, file_comment):
    dir_path = os.path.dirname(os.path.abspath(directory_path))
    if os.path.exists(dir_path) and os.path.isdir(dir_path):
        for root, dirs, files in os.walk(dir_path, topdown=False):
            for name in files:
                line_appender(os.path.join(root, name), file_comment)
    else:
        print("This folder dosen't exist or isn't a directory at all")

if __name__ == "__main__":

    commands = parser.parse_args()
    if commands.dirname and commands.comment:
        with open(commands.comment, 'r') as comm:
            comms = [line for line in comm.readlines()]
            direct_appender(commands.dirname, comms)
