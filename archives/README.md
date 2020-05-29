## Archives

This catalog contains 3 archives, each of which corresponds to the investigated project:

   * The __Vienna__ project archive contains two following directories:
       1. __Vienna_original_study__ contains raw project files, instruction, scripts, etc., received from the authors of the original work.
       2. __Vienna_reproduction__ contains a cloned [Git-Hub repository](https://github.com/ViennaRSS/vienna-rss), as well as a script with which you can get the necessary files from the cloned repository.
   * The __Monotone__ project archive contains 41 archives of versions 0.1, 0.2, 0.10-0.48 inclusive, downloaded from [this](https://www.monotone.ca/downloads.php?type=Tarball) site.

   * The __BiblioteQ__ project archive contains a 'cloned' [repository](https://sourceforge.net/p/biblioteq/code/HEAD/tree/).


**Important!**
The "Vienna_original_study" folder in the "Vienna" archive contains the original scripts of authors in which errors were not fixed.
Corrected work files can be found in [this](https://github.com/brdd3v/repro/tree/master/vienna/input) folder.


If you plan to use the raw files for the "Vienna" project received from the authors, you can find them in the following way:<br/>
`Vienna.zip -> Vienna_original_study -> vienna-rss.tgz`.

If you want to use the raw files for the "Vienna" project that we obtained during the reproduction of the study, then do the following:
   1. Open the "Vienna.zip" file. 
   2. Unzip the "Vienna_reproduction" folder.
   3. Run the "get_vienna_files.py" script: `python3 get_vienna_files.py`.

Alternatively, you can only unpack the script and run it, then it will conduct the cloning of the repository itself.

After the script is finished, the folder __vienna-rss-study__ will be created (in the directory where the script is located, and the repository clone) with subfolders and necessary files. Then you can extract the database schemas and transform them using original scripts and instructions from [this](https://github.com/brdd3v/repro/tree/master/vienna/input) folder.
