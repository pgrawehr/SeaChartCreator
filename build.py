#!/usr/bin/python3
# encoding: utf-8

'''

Copyright (C) 2017  Steffen Volkmann

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

'''

from optparse import OptionParser
from Utils.Mobac import ExtractMapsFromAtlas
from atlas.generator import AtlasGenerator
from Utils.glog import getlog, initlog
from tile.sqllitedb import TileSqlLiteDB

DBDIR = './work/database/'
WDIR = './work/'


def main():
    parser = OptionParser()
    parser.add_option("-i", "--InFile", type="string", help="MOBAC Project File", dest="ProjectFile", default="./sample/atlas/mobac/mobac-profile-testprj.xml")
    parser.add_option("-d", "--DatabaseDirectory", type="string", help="tile store directory", dest="DBDIR", default=DBDIR)
    parser.add_option("-q", "--quiet", action="store_false", dest="quiet", default=True, help="set log level to info (instead debug)")

    options, arguments = parser.parse_args()
    arguments = arguments

    initlog('build', options.quiet)
    logger = getlog()

    logger.info('Start fetch tiles')

    # get maps from mobac project file
    if options.ProjectFile is not None:
        # get list of chart areas from project file
        atlas, name = ExtractMapsFromAtlas(options.ProjectFile)
    else:
        exit()

    db = TileSqlLiteDB(options.DBDIR)
    gen = AtlasGenerator(WDIR, db)
    gen.GenerateKAP(atlas, name)
    logger.info('ready')
    db.CloseDB()

    return


if __name__ == "__main__":
    exit(main())