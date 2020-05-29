# Reproduction of the Study "Schema Evolution Analysis for Embedded Databases"
Reproduction of the study was carried out on Linux OS, so the configuration is designed for this OS.

## Table of Contents

1. [Getting Started](#getting-started)
2. [Structure](#structure)
3. [How to Use](#how-to-use)


## Getting Started

* **Install programs**:
   * python 2.* and 3.*<br/>
Version 2 is only needed for the project "Vienna".
   * DBMS MySQL<br/>
Can be installed using the following command: `sudo apt-get install mysql-server`
   * mysqldiff 0.30 or 0.60<br/>
Various versions of the program can be downloaded from this site: https://metacpan.org/release/MySQL-Diff<br/>
(In the reproduction the default version is 0.60).


* **Install python-modules**:
   * pandas


* **Configure MySQL**<br/>

In case of problems with the password for this DBMS, the information on this sites may be useful:<br/>
https://linuxconfig.org/how-to-reset-root-mysql-password-on-ubuntu-18-04-bionic-beaver-linux ,<br/>
https://dev.mysql.com/doc/refman/8.0/en/resetting-permissions.html

The program "mysqldiff" requires connection to MySQL.<br/>
Currently, the script "proc.py" uses a connection to MySQL without using the login and password parameters.<br/>
If you do not want to make changes to the code, you must create a ~/.my.cnf file with the following contents:
```
[client]
user = root
password = passwd
```
This solution was copied from: https://medium.com/@benmorel/remove-the-mysql-root-password-ba3fcbe29870<br/>

Alternatively, you can make a change in the "make_comp" function, replacing the line with one of the following:
```python
proc = subprocess.Popen("mysqldiff --user=root --password=passwd {} {}".format(file_1, file_2), shell=True,
```
or
```python
proc = subprocess.Popen(["mysqldiff", "--user=root", "--password=passwd", file_1, file_2],
```

**Important!** 
If you plan to use version 0.30, then in the script "proc.py", in the "make_comp" function, you must specify the path to the file "mysqldiff.pl".


## Structure

The current directory contains the python script "proc.py".<br/>
This script is responsible for comparing schemas, parsing the result of the “mysqldiff” program, as well as for saving log information and counting the number of SMOs.<br/>
(This file should be used after all the schemas were extracted.)

Each project, Monotone, Vienna and BiblioteQ, has its own folder<sup>1</sup>. 
Each projects folder consist of __input__ and __output__ directories.

Directory __input__ contains:
   * Raw data files, already extracted from the project of specific version or revision.
   * Python-script, which is responsible for schema extraction and transformation.
   * Input files (SQL-files with the postfix **_mod** in the name), which contain extracted and tranformed (into MySQL syntax) SQL statements<sup>2</sup>.

Directory __output__ contains:
   * Log files for specific mysqldiff version (0.30 or 0.60), which containt the full program output<sup>3</sup>.
   * t_info_[0.30 | 0.60].csv file that contains information of founded table names in versions and revisions.
   * <project_name>_cmp_[0.30 | 0.60].csv file that contains the number of table and attribute changes (SMOs).

The current directory also contains the __archives__ folder, with the archives of source files, scripts, some of which were used in the work, as well as cloned repositories.

## How to Use

Raw data, input and output data along with the logs are already in this repository.<br/>
To repeat our steps, do the following:<br/>
   1. We have already found and extracted the source files from certain versions and revisions (described in more detail in our paper), so the first step is to extract and transform the database schemas from raw files.
This can be done using the "schema_extractor.py" script in the input directory of each project<sup>4</sup>. 
   2. The next step is to run the "proc.py" script: 
```bash
python3 proc.py
```
is the same as
```bash
python3 proc.py -v 0.60 -p vienna monotone biblioteq
```
The parameter `-v` or `--version` allows you to specify the version of the program "mysqldiff", and the `-p` or `--projects` parameter allows you to select projects and their order.


__Footnotes__
1. For the project "Firefox" the folder was not created for the reasons specified in the paper.
2. The input files for the project "Vienna" are in the subfolder __refine__.
3. The files of the "Monotone" project will also contain either "sql" or "cc" in the name, indicating one or another approach (see the paper for details).
4. For the project "Vienna", use the original scripts and the original instructions (Steps 3-9).

