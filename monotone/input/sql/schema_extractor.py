#!/usr/bin/env python

####################################################################################
#
# schema_extractor.py - script to extract and convert database schema (Monotone_sql)
# Copyright (C) 2020  Braininger Dimitri
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
####################################################################################

import io
import os
import re


def remove_sngl_comments(text):

    comments_lst = re.findall(r"--.*", text)
    comments_lst.sort(reverse=True)
    for comment in comments_lst:
        text = text.replace(comment, "")
    return text.strip()


def mod_query(query):

    new_query = ""

    lines = query.split("\n")
    for line in lines:
        line = line.replace("\t", " ")
        line = line.replace("not null", "integer not null")
        line = line.replace("primary key", "integer primary key")
        new_query = "{} {}".format(new_query, line)

    new_query = " ".join(new_query.split())
    new_query = new_query.replace(", )", ")").replace("( ", "(").replace(" )", ")")
    return new_query


def main():

    for i in range(1, 49):
        if (i > 2) and (i < 10):
            continue

        file_name = "{}{}.sql".format("schema_0", i)
        with io.open("{}/{}".format(os.getcwd(), file_name), mode="r", encoding="utf-8") as f:

            text = f.read()
            #text = text.lower()  # important because MySQL is case sensitive

            lines_mod = list()
            lines = text.split("\n")
            for line in lines:
                line_mod = remove_sngl_comments(line)
                lines_mod.append(line_mod)

            text = "\n".join(lines_mod)

            queries = text.split(";")
            queries_list = list()
            for query in queries:
                if "create table" in query.lower():
                    query_mod = mod_query(query)
                    queries_list.append(query_mod)

        file_name = "{}{}_mod.sql".format("schema_0", i)
        mod_file = io.open("{}/{}".format(os.getcwd(), file_name), mode="w", encoding="utf-8")
        for query in queries_list:
            mod_file.write("{};\n\n".format(query))

        mod_file.close()

    print("Extraction and transformation of database schemas completed!")


if __name__ == "__main__":
    main()

