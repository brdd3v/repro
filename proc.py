#!/usr/bin/env python

####################################################################################
#
# proc.py - script for comparing database schemas and counting changes
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
import csv
import subprocess
import psutil
import pandas as pd
import argparse
import logging


def parse_cli_arguments():
    
    parser = argparse.ArgumentParser()    
    parser.add_argument("-v", "--version",
                        default="0.60",
                        choices=["0.30", "0.60"],
                        help="mysqldiff version: 0.60 by default")

    parser.add_argument("-p", "--projects",
                        nargs="*",
                        default=["vienna", "monotone", "biblioteq"],
                        choices={"vienna", "monotone", "biblioteq"},
                        help="project names: vienna monotone biblioteq")

    args = parser.parse_args()
    arg_params = {"version": args.version, "projects": args.projects}
    return arg_params


def setup_logger(name, log_file, level=logging.INFO):

    formatter = logging.Formatter('%(levelname)5s %(message)s')

    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    return logger


def convert_dct_df(dct):

    indexes = [key for key in dct.keys()]
    columns = get_cmp_dct().keys()
    df = pd.DataFrame(index=indexes, columns=columns)

    for idx in indexes:
        if any(dct[idx].values()) is True:
            df.at[idx] = [val for val in dct[idx].values()]

    df.fillna(0, inplace=True)
    df.loc['Total', :] = df.sum(axis=0)  # row (dtype: float64)
    df.loc[:, 'Total'] = df.sum(axis=1)  # column (dtype: float64)
    df = df.astype('int64')
    return df


def get_cmp_dct():

    cmp_dct = dict()
    cmp_dct["ct_num"] = 0  # CREATE TABLE
    cmp_dct["dt_num"] = 0  # DROP TABLE
    # cmp_dct["cc_num"] = 0  # ALTER TABLE
    cmp_dct["cc_t_num"] = 0  # CHANGE TYPE
    cmp_dct["cc_i_num"] = 0  # CHANGE INIT
    cmp_dct["ac_num"] = 0  # ADD COLUMN
    cmp_dct["dc_num"] = 0  # DROP COLUMN
    cmp_dct["apk_num"] = 0  # ADD PRIMARY KEY
    cmp_dct["dpk_num"] = 0  # DROP PRIMARY KEY
    return cmp_dct


def get_write_tables_info(file_name, version, output_f_name, add_header=False):

    with io.open(file_name, mode="r", encoding="utf-8") as f:
        text = f.read()
        tables = text.split("CREATE TABLE")

        tables_num = len([t for t in tables if t.strip() != ""])
        table_names = list()

        for t in tables:
            if (t.strip() == "") or (t.find("(") == -1):
                continue

            t_name = t[:t.find("(")].strip()
            table_names.append(t_name)

        with io.open(output_f_name, mode="a", encoding="utf=8") as csv_file:
            writer = csv.writer(csv_file)
            if add_header is True:
                writer.writerow(["version", "num_of_tables", "table_names"])
            writer.writerow([version, tables_num, table_names])


def parse_output(cmp_dct, output):

    lines = output.split("\n")

    for line in lines:

        if line.find("CREATE TABLE") is not -1:
            cmp_dct["ct_num"] += 1

        # Version 0.30 has two types: DROP TABLE and DROP TABLE IF EXISTS
        # Version 0.60 - DROP TABLE only
        elif line.find("DROP TABLE") is not -1:
            if line.find("DROP TABLE IF EXISTS") is -1:
                cmp_dct["dt_num"] += 1

        elif line.find("ALTER TABLE") is not -1:
            #cmp_dct["cc_num"] += 1

            if line.find("CHANGE COLUMN") is not -1:
                # Type change
                ori_type = line.split(";")[0].split()[7]
                che_type = line.split(";")[1].split()[2]
                if ori_type != che_type:
                    cmp_dct["cc_t_num"] += 1

                # Init change (~Firefox only; Recheck needed)
                """
                try:
                    ori_ini = line.split(";")[0].split()[8] + " " + line.split(";")[0].split()[9]
                except:
                    ori_ini = ""
                try:
                    che_ini = line.split(";")[1].split()[3] + " " + line.split(";")[1].split()[4]
                except:
                    che_ini = ""
                if ori_ini != che_ini:
                    cmp_dct["cc_i_num"] += 1
                """

            elif line.find("ADD COLUMN") is not -1:
                cmp_dct["ac_num"] += 1

            elif line.find("DROP COLUMN") is not -1:
                cmp_dct["dc_num"] += 1

            elif line.find("ADD PRIMARY KEY") is not -1:
                cmp_dct["apk_num"] += 1

            elif line.find("DROP PRIMARY KEY") is not -1:
                cmp_dct["dpk_num"] += 1


def make_comp(cmp_dct, file_1, file_2, logger, msd):

    if msd == "0.60":
        proc = subprocess.Popen(['mysqldiff', file_1, file_2],
                                stdin=subprocess.PIPE,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                encoding='UTF-8')

        stdout, stderr = proc.communicate()

        proc.stdout.close()
        proc.kill()

        if psutil.pid_exists(proc.pid):
            print("Warning! Process with id {} is not closed!".format(proc.pid))

    else:  # 0.30

        input_string = "perl {} {} {}".format(os.getcwd() + '/MySQL-Diff-0.30/mysqldiff.pl', file_1, file_2).strip()
        stdout = subprocess.check_output(input_string, shell=True)
        stdout = stdout.decode("utf-8")

    start_comment = False

    new_lines = list()
    lines = stdout.split("\n")
    for line in lines:
        line = line.strip()
        if len(line) == 0 or line.startswith("Use of") or line.startswith("ERROR ") or line.startswith("/*"):
            continue
        elif line.startswith("##"):  # There might be additional output lines
            start_comment = True
            continue
        if start_comment is True:
            new_lines.append(line)

    output = "\n".join(new_lines)

    logger.info("\n{}\n{}\n{}\n".format(file_1, file_2, output))  # Full text for manual verification
    if msd == "0.60":
        logger.error("\n{}\n\n".format(stderr if stderr.strip() != "" else "No Error"))

    parse_output(cmp_dct, output)


def proc_vienna(msd):

    logger = setup_logger('vienna', "{}/vienna/output/vienna_{}.log".format(os.getcwd(), msd))
    print("\nProcessing data of the project 'Vienna'")

    # VERSION PROCESSING
    version_cmp_dct = dict()
    for i in range(7):
        curr_v_folder = "{}/vienna/input/ex_c_sql/DATABASE-2.{}.0".format(os.getcwd(), i)
        res = os.scandir("{}/refine/".format(curr_v_folder))

        ver = "2.{}.0".format(i)
        version_cmp_dct[ver] = list()

        # REVISIONS PROCESSING
        rev_num_lst = list()
        for file_dir in res:
            if os.path.isdir(file_dir.path):
                rev_num_lst.append(int(file_dir.name.split(".")[1]))  # only number

        rev_num_lst = sorted(rev_num_lst)

        print("DB version {}".format(ver))

        cmp_dct = get_cmp_dct()

        for rev_first, rev_second in zip(rev_num_lst, rev_num_lst[1:]):
            file_1 = "{}/refine/Database.{}.m/out_Database.sql".format(curr_v_folder, rev_first)
            file_2 = "{}/refine/Database.{}.m/out_Database.sql".format(curr_v_folder, rev_second)

            make_comp(cmp_dct, file_1, file_2, logger, msd)

        version_cmp_dct[ver] = cmp_dct

    df = convert_dct_df(version_cmp_dct)
    df.to_csv("{}/vienna/output/vienna_cmp_{}.csv".format(os.getcwd(), msd))


def proc_monotone(msd):

    for f_type in ["sql", "cc"]:

        logger = setup_logger('monotone', "{}/monotone/output/monotone_{}{}.log".format(os.getcwd(), f_type, msd))
        print("\nProcessing data of the project 'Monotone': {}".format(f_type))

        vers_nums_lst = list()
        for i in range(1, 49):
            if (i > 2) and (i < 10):  # only 1,2 and 10-48 (inclusive)
                continue
            vers_nums_lst.append(i)

        vers_nums_lst = sorted(vers_nums_lst)
        version_cmp_dct = dict()

        for ver_first, ver_second in zip(vers_nums_lst, vers_nums_lst[1:]):
            print("Comparing versions {} and {}".format(ver_first, ver_second))

            file_1 = "{}/monotone/input/{}/schema_0{}_mod.sql".format(os.getcwd(), f_type, ver_first)
            file_2 = "{}/monotone/input/{}/schema_0{}_mod.sql".format(os.getcwd(), f_type, ver_second)

            output_t_info_f_name = "{}/monotone/output/t_info_{}{}.csv".format(os.getcwd(), msd, f_type)

            if ver_first == vers_nums_lst[0]:  # initial version
                version_cmp_dct[ver_first] = get_cmp_dct()

                if os.path.exists(output_t_info_f_name):
                    os.remove(output_t_info_f_name)
                get_write_tables_info(file_1, ver_first, output_t_info_f_name, True)

            cmp_dct = get_cmp_dct()
            make_comp(cmp_dct, file_1, file_2, logger, msd)

            version_cmp_dct[ver_second] = cmp_dct
            get_write_tables_info(file_2, ver_second, output_t_info_f_name)

        df = convert_dct_df(version_cmp_dct)
        df.to_csv("{}/monotone/output/monotone_cmp_{}{}.csv".format(os.getcwd(), msd, f_type))

        logger.removeHandler(logger.handlers[0])


def proc_biblioteq(msd):

    logger = setup_logger('biblioteq', "{}/biblioteq/output/biblioteq_{}.log".format(os.getcwd(), msd))
    print("\nProcessing data of the project 'BiblioteQ'")

    files_lst = list()
    files = os.scandir("{}/biblioteq/input".format(os.getcwd()))
    for file in files:
        if "db_create_schema_mod" in file.name:
            files_lst.append(int(file.name.split(".")[1].replace("r", "")))

    files_lst = sorted(files_lst)

    version_cmp_dct = dict()

    for rev_first, rev_second in zip(files_lst, files_lst[1:]):
        print("Comparing revisions {} and {}".format(rev_first, rev_second))

        file_1 = "{}/biblioteq/input/db_create_schema_mod.r{}.sql".format(os.getcwd(), rev_first)
        file_2 = "{}/biblioteq/input/db_create_schema_mod.r{}.sql".format(os.getcwd(), rev_second)

        output_t_info_f_name = "{}/biblioteq/output/t_info_{}.csv".format(os.getcwd(), msd)

        if rev_first == files_lst[0]:  # initial version
            version_cmp_dct[rev_first] = get_cmp_dct()

            if os.path.exists(output_t_info_f_name):
                os.remove(output_t_info_f_name)
            get_write_tables_info(file_1, rev_first, output_t_info_f_name, True)

        cmp_dct = get_cmp_dct()
        make_comp(cmp_dct, file_1, file_2, logger, msd)
        get_write_tables_info(file_1, rev_second, output_t_info_f_name)

        version_cmp_dct[rev_second] = cmp_dct

    df = convert_dct_df(version_cmp_dct)
    df.to_csv("{}/biblioteq/output/biblioteq_cmp_{}.csv".format(os.getcwd(), msd))


def main():

    args = parse_cli_arguments()

    msd = args["version"]
    for project in args["projects"]:
        if project == "vienna":
            proc_vienna(msd)
        if project == "monotone":
            proc_monotone(msd)
        if project == "biblioteq":
            proc_biblioteq(msd)


if __name__ == "__main__":
    main()

