#!/usr/bin/env python

####################################################################################
#
# schema_extractor.py - script to extract and convert database schema (BiblioteQ)
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

import os
import io
import re


def remove_sngl_comments(text):

    comments_lst = re.findall(r"--.*", text)
    comments_lst.sort(reverse=True)
    for comment in comments_lst:
        text = text.replace(comment, "")
    return text.strip()


def remove_mult_comments(text):

    idx = text.find("/*")
    if idx != -1:
        return text[:idx]
    return text


def remove_default_value(text):

    t_values = re.findall("'(.+?)'", text)
    for dv in t_values:
        text = text.replace(dv, "")

    default_values = re.findall("DEFAULT(.+?),", text)
    for dv in default_values:
        text = text.replace(dv, "")

    text = text.replace(" DEFAULT", "")
    text = text.replace("'", "")
    return text


def mod_query(query):

    new_query = ""

    lines = [el for el in query.split("\n") if el.strip() != ""]
    for line in lines:
        line = line.replace("\t", " ")
        line = line.replace(", )", " )")

        # SQLite -> MySQL (revision >= 35)
        line = line.replace("BYTEA", "BLOB")
        line = line.replace("AUTOINCREMENT", "AUTO_INCREMENT")

        if "FOREIGN" in line:
            continue

        new_query = "{} {}".format(new_query, line)

    new_query = " ".join(new_query.split())
    new_query = new_query.replace(", )", " )")
    return new_query


def main():

    files = os.scandir(os.getcwd())
    files_lst = list()

    for file in files:
        if file.name.endswith(".sql"):
            sql_dct = dict()
            sql_dct["name"] = file.name
            sql_dct["path"] = file.path
            sql_dct["rev"] = int(file.name.split(".")[1].replace("r", ""))
            files_lst.append(sql_dct)

    files_dct_lst = sorted(files_lst, key=lambda k: k["rev"])

    for file_dct in files_dct_lst:
        with io.open(file_dct["path"], mode="r", encoding="utf-8") as f:
            text = f.read()
            queries = text.split(";")

            lines_mod = list()
            lines = text.split("\n")
            for line in lines:
                line_mod = remove_sngl_comments(line)
                line_mod = remove_mult_comments(line_mod)
                #line_mod = remove_default_value(line_mod)

                lines_mod.append(line_mod)

            text = "\n".join(lines_mod)

            queries = text.split(";")
            queries_list = list()
            for query in queries:
                if "create table" in query.lower():
                    query_mod = mod_query(query)
                    queries_list.append(query_mod)

        new_file_name = "db_create_schema_mod.r{}.sql".format(file_dct["rev"])
        mod_file = io.open("{}/{}".format(os.getcwd(), new_file_name), mode="w", encoding="utf-8")
        for query in queries_list:
            mod_file.write("{};\n\n".format(query))

        mod_file.close()

    print("Extraction and transformation of database schemas completed!")


if __name__ == "__main__":
    main()

