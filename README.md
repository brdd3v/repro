# Reproduction/Replication of the Study "Schema Evolution Analysis for Embedded Databases"
Reproduction of the study was carried out on Linux OS, so the configuration is designed for this OS.

## Table of Contents

1. [Setup](#setup)
2. [Structure](#structure)
3. [How to Use](#how-to-use)


## Setup

First you need to install and configure some programs and modules.
This can be done in <u>three</u> ways:

1. **[Docker](https://www.docker.com/)**<sup>1</sup>

   To build docker image:
   ```
   docker build -t repro .
   ```
   To run docker container:
   ```
   docker run -it --rm repro
   ```
   In the docker container, start mysql service:
   ```
   service mysql start
   ```

2. **[Vagrant](https://www.vagrantup.com/)/[Ansible](https://www.ansible.com/)**<sup>1</sup>

   To create and prepare a virtual machine:
   ```
   vagrant up
   ```
   To connect to the machine:
   ```bash
   vagrant ssh
   ```
   Inside the virtual machine you have <u>two</u> options:<br/>
   The first is to go to the **/vagrant** folder and continue to work from there<br/>
   (This folder is a shared folder between a guest VM and a host. All changes in it will affect the host files).<br/>
   The second is to copy the contents of the **/vagrant** folder for example in a home catalog on a virtual machine:
   ```
   cp -r /vagrant/* /home/vagrant
   ```

3. **Manual**

   3.1. **Install programs**:
   * Python 2.* and 3.*<br/>
   (Version 2 is needed only if you are going to prepare the input data for the Vienna project using original scripts).
   * DBMS MySQL<br/>
Can be installed using the following command:
   ```bash
   sudo apt-get install mysql-server
   ```
   * MySQL-Diff 0.30 or 0.60<br/>
Various versions of the program can be installed from [CPAN](https://metacpan.org/dist/MySQL-Diff). There is also a [git repository](https://github.com/aspiers/mysqldiff).<br/>
(In the reproduction the default version is 0.60).


   3.2 **Install python-modules**:
   ```bash
   pip3 install -r requirements.txt
   ```


   3.3 **Configure MySQL**<br/>

   In case of problems with the password for this DBMS, the information on this sites may be useful:<br/>
https://linuxconfig.org/how-to-reset-root-mysql-password-on-ubuntu-18-04-bionic-beaver-linux ,<br/>
https://dev.mysql.com/doc/refman/8.0/en/resetting-permissions.html

   The program "mysqldiff" requires connection to MySQL.<br/>
Currently, the script [proc.py](/proc.py) uses a connection to MySQL without using the login and password parameters.<br/>
If you do not want to make changes to the code, you must create a ~/.my.cnf file with the following contents:
   ```
   [client]
   user = <user>
   password = <password>
   ```
   You can find out more about this file [here](https://dev.mysql.com/doc/refman/5.7/en/option-files.html).<br/>

   Alternatively, you can make a change in the "make_comp" function, replacing the line with one of the following:
   ```python
   proc = subprocess.Popen("mysqldiff --user=root --password=passwd {} {}".format(file_1, file_2), shell=True,
   ```
   or
   ```python
   proc = subprocess.Popen(["mysqldiff", "--user=root", "--password=passwd", file_1, file_2],
   ```

   **Important!**
If you plan to use version 0.30, then in the script [proc.py](/proc.py), in the "make_comp" function, you must specify the path to the file "mysqldiff.pl".


## Structure

The current directory contains the python script [proc.py](/proc.py).<br/>
This script is responsible for comparing schemas, parsing the result of the “mysqldiff” program, as well as for saving log information and counting the number of SMOs.<br/>
(This file should be used after all the schemas were extracted.)

Each project, Monotone, Vienna and BiblioteQ, has its own folder<sup>2</sup>.
Each projects folder consist of __input__ and __output__ directories.

Directory __input__ contains:
   * Raw data files, already extracted from the project of specific version or revision.
   * Python-script, which is responsible for schema extraction and transformation.
   * Input files (SQL-files with the postfix **_mod** in the name), which contain extracted and tranformed (into MySQL syntax) SQL statements<sup>3</sup>.

Directory __output__ contains:
   * Log files for specific mysqldiff version (0.30 or 0.60), which containt the full program output<sup>4</sup>.
   * t_info_[0.30 | 0.60].csv file that contains information of founded table names in versions and revisions.
   * <project_name>_cmp_[0.30 | 0.60].csv file that contains the number of table and attribute changes (SMOs).

The current directory also contains the [__archives__](/archives/) folder, with the archives of source files, scripts, some of which were used in the work, as well as cloned repositories.

## How to Use

Raw data, input and output data along with the logs are already in this repository.<br/>
To repeat our steps, do the following:
   1. We have already found and extracted the source files from certain versions and revisions (described in more detail in our paper), so the first step is to extract and transform the database schemas from raw files.
   This can be done using the "schema_extractor.py" script in the input directory of each project<sup>5</sup>.
   2. The next step is to run the [proc.py](/proc.py) script:
   
```bash
python3 proc.py
```
is the same as
```bash
python3 proc.py -v 0.60 -p vienna monotone biblioteq
```
The parameter `-v` or `--version` allows you to specify the version of the program "mysqldiff", and the `-p` or `--projects` parameter allows you to select projects and their order.


__Footnotes__
   1. The following versions of OS and programs are used in the Docker and Vagrant options:
      * ubuntu 18.04
      * mysql Ver 14.14 Distrib 5.7.42
      * python 3.6.9
      * mysqldiff 0.60
   2. For the project "Firefox" the folder was not created for the reasons specified in the paper.
   3. The input files for the project "Vienna" are in the subfolder __refine__.
   4. The files of the "Monotone" project will also contain either "sql" or "cc" in the name, indicating one or another approach (see the paper for details).
   5. For the project "Vienna", use the original scripts and the original instructions (Steps 3-9).

