# root_hist_comparer

This is a short python script to compare the directory structure and histograms within two ROOT files. It was implemented to be used for the validation of ATHENA pixel monitoring output.

It basically does the following steps:
1. Read the directory structures of both files.
2. Compare the directory structures and output any differences.
3. Read the histograms stored in both files.
4. Compare these two lists of histograms and output any differences.
5. Start a thorough comparison of _common_ histograms between the two files, using the following criteria:
   - title
   - class
   - number of bins (in x, y, z)
   - axis titles (for x, y, z axes)
   - effective number of entries
6. If option `--detailed` is given, perform a bin-by-bin comparison for all common histograms, i.e. check whether the bin contents are identical.

Important messages are outputted into the standard output, more detailed info is stored in the log file `compare.log`.

## How to run the script

Ensure that ROOT libraries are accessible for python. Then call
```
python hist_comparer.py file1 file2
```

## Additional options

The script currently has two options:
1. `--ignore`: this ignores any differences found between the two input files and performs all actions nonetheless. This is helpful to use if you _expect_ certain differences, e.g. because you applied certain changes, but you want to make sure that nothing else is affected.
2. `--detailed`: run a bin-by-bin comparison as described above.
