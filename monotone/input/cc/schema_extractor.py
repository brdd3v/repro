#!/usr/bin/env python

####################################################################################
#
# schema_extractor.py - script to extract and convert database schema (Monotone_cc)
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
from collections import Counter

"""
Important!
Files "schema_01_mod.sql" and "schema_02_mod.sql" were copied from the folder "input/sql".

Need to check parsing strategy.

Unfortunately, without pattern(s) from the original work, 
it is impossible to repeat the method of extracting database schemas.
"""


def remove_sngl_comments(text):

    comments_lst = re.findall(r"--.*", text)
    comments_lst.sort(reverse=True)
    for comment in comments_lst:
        text = text.replace(comment, "")
    return text.strip()


def remove_unc_chr(text):

    for c in ['\\n', '\n', '\\t', '\t', '"']:
        text = text.replace(c, '')
    return text


def get_t_name(query):

    if "DROP TABLE" in query:
        t_name = query[query.find("DROP TABLE"):].replace("DROP TABLE ", "")
        t_name = t_name[:t_name.find(";")]
        if "NULL" in t_name:
            t_name = t_name[:t_name.find(", NULL")]
    elif "CREATE TABLE" in query:
        t_name = query[:query.find(" (")].replace("CREATE TABLE ", "")

    t_name = remove_unc_chr(t_name)
    t_name = re.sub(r'^a-zA-Z_', '', t_name)
    t_name = t_name.strip()
    return t_name


def mod_query(query):

    new_query = ""

    lines = query.split("\n")
    for line in lines:

        line = line.replace("\t", " ")
        line = line.replace("not null", "integer not null")
        line = line.replace("primary key", "integer primary key")
        new_query = "{} {}".format(new_query, line)

    new_query = " ".join(new_query.split())
    new_query = new_query[new_query.find("CREATE TABLE "):]
    new_query = new_query.replace(", )", ")").replace("( ", "(").replace(" )", ")")
    new_query = new_query.replace(")))", "))")
    new_query = new_query.replace(", NULL, NULL, errmsg)", "")
    new_query = new_query.replace("disk corruption", "")
    return new_query


def main():

    # for manual check
    ct_tnames_set = set()
    dt_tnames_set = set()

    for i in range(10, 49):

        if i >= 43:
            file_name = "migrate_schema_0{}.cc".format(i)
        else:
            file_name = "schema_migration_0{}.cc".format(i)
        with io.open("{}/{}".format(os.getcwd(), file_name), mode="r", encoding="utf-8") as f:

            text = f.read()
            query_start = False

            tables_drp = list()
            tables_crt = list()

            lines_mod = list()
            lines = text.split("\n")
            for line in lines:

                if "DROP TABLE " in line:
                    if "DROP TABLE tmp" in line or ";" not in line:
                        continue

                    drp_table_name = get_t_name(line)
                    if len(drp_table_name) != 0:
                        tables_drp.append(drp_table_name)
                        continue

                """
                # Tables have been renamed in "tmp" and deleted
                if "ALTER TABLE" in line and "RENAME TO tmp;" in line:
                    drp_table_name = line.replace("ALTER TABLE", "")\
                                         .replace("RENAME TO tmp;", "")\
                                         .replace('"', '')\
                                         .replace("\\n", "")\
                                         .strip()
                    tables_drp.append(drp_table_name)
                    continue
                """

                if ("CREATE TABLE " in line) and ("%" not in line) and ('"CREATE TABLE ";' not in line):
                    query_start = True
                    line_mod = line[line.find("CREATE TABLE "):]
                    line_mod = remove_unc_chr(line_mod)
                    lines_mod.append(line_mod)
                    continue

                if (query_start is True) and (('")"' in line) or ('");"' in line)):
                    lines_mod.append(');')
                    lines_mod.append('')
                    query_start = False
                    continue

                elif query_start is True:
                    line_mod = remove_sngl_comments(line)
                    line_mod = remove_unc_chr(line_mod)
                    lines_mod.append(line_mod)

            text = "\n".join(lines_mod)

            queries = text.split(";")
            queries_list = list()
            for query in queries:
                if "CREATE TABLE" in query:
                    query_mod = mod_query(query)
                    queries_list.append(query_mod)

                    crp_table_name = get_t_name(query_mod)
                    tables_crt.append(crp_table_name.strip())

        # Remove redundant CREATE TABLE-queries
        tbls_cnt = dict(Counter(tables_crt))
        for tc in tbls_cnt.keys():
            if tbls_cnt[tc] > 1:
                for x in range(tbls_cnt[tc]-1):
                    for query in queries_list[:]:
                        if "CREATE TABLE {}".format(tc) in query:
                            queries_list.pop(queries_list.index(query))
                            break

        # REMOVE tables (According to the queries "DROP TABLE" from the source code)
        """
        for idx, name in enumerate(tables_drp):
            if name.endswith("_tmp"):
                tables_drp[idx] = name.replace("_tmp", "")
        """

        if i >= 30:  # special case (This two tables were deleted and created again)
            tables_drp.remove("rosters")
            tables_drp.remove("roster_deltas")

        for td in tables_drp:
            for query in queries_list[:]:
                if "CREATE TABLE {}".format(td) in query:
                    queries_list.pop(queries_list.index(query))

        for elc in tables_crt:
            ct_tnames_set.add(elc)

        for eld in tables_drp:
            dt_tnames_set.add(eld)

        file_name = "{}{}_mod.sql".format("schema_0", i)
        mod_file = io.open("{}/{}".format(os.getcwd(), file_name), mode="w", encoding="utf-8")
        for query in queries_list:
            mod_file.write("{};\n\n".format(query))

        mod_file.close()

    print("Extraction and transformation of database schemas completed!")


if __name__ == "__main__":
    main()

