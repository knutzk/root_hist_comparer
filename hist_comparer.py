#!/usr/bin/python
import logging
import sys

def GetRunNumber(file1, file2):
    run_nr1 = ""
    run_nr2 = ""

    objects = file1.GetListOfKeys()
    for entry in objects:
        run_nr1 = entry.GetName()
        break
    objects = file2.GetListOfKeys()
    for entry in objects:
        run_nr2 = entry.GetName()
        break
    if run_nr1 == run_nr2:
        return run_nr1
    logging.error("could not detect run number")
    sys.exit(-1)


# Go through all directories recursively, starting from run_[number]/Pixel.
# The function returns a list of all TDirectory/TDirectoryFile objects.
def GetDirectories(file, run):
    directories = [run + "/Pixel"]

    for dir in directories:
        keys = file.Get(dir).GetListOfKeys()
        itr = iter(keys)
        for i in itr:
            path = dir + "/" + i.GetName()
            if not file.Get(path):
                logging.warning("Cannot retrieve %s in directory %s. Pointer points nowhere" % (path, dir))
                continue
            if file.Get(path).ClassName() == "TDirectoryFile":
                directories.append(path)
            if file.Get(path).ClassName() == "TDirectory":
                directories.append(path)
    return directories


# Get a list of all histograms, given a list of directories to search trough.
def GetHistograms(file, directories):
    histograms = []
    for dir in directories:
        if not file.Get(dir):
            continue
        keys = file.Get(dir).GetListOfKeys()
        itr = iter(keys)
        for i in itr:
            path = dir + "/" + i.GetName()
            if not file.Get(path):
                continue
            if file.Get(path).ClassName() == "TDirectory":
                continue
            if file.Get(path).ClassName() == "TDirectoryFile":
                continue
            if file.Get(path).ClassName() == "TTree":
                continue
            histograms.append(path)
    return histograms


# Compare two lists (either of histograms or directories).
def CompareLists(list1, list2):
    # Create intersection and complementary sets
    intersect = set(list1).intersection(list2)
    compl1 = set(list1) - intersect
    compl2 = set(list2) - intersect

    comparison_ok = True
    if len(compl1) > 0 or len(compl2) > 0:
        logging.warning("Files do not have identical structure (directories, histograms)!")
        comparison_ok = False
        if len(compl1) > 0:
            logging.warning("Only found in input file 1 (%s):" % len(compl1))
            for dir in sorted(compl1):
                logging.warning("\t--> " + dir)
        if len(compl2) > 0:
            logging.warning("Only found in input file 2 (%s):" % len(compl2))
            for dir in sorted(compl2):
                logging.warning("\t--> " + dir)
    if comparison_ok:
        logging.debug("Files have identical structure. Continue with next step ...")
        return True
    return False


# Make a basic comparison of two histogram objects. This checks the following
# criteria: histogram title, axis titles (X, Y, Z), number of bins (X, Y, Z),
# number of total entries.
def CompareHistograms(file1, file2, histname):
    hist1 = file1.Get(histname)
    hist2 = file2.Get(histname)
    if not hist1:
        return
    if not hist2:
        return
    found_error = False
    if hist1.GetName() != hist2.GetName():
        if not found_error:
            logging.warning("Differences found in: " + histname)
            found_error = True
        logging.debug("\t--> Objects names differ: %s | %s" % (hist1.GetName(), hist1.GetName()))
    if hist1.GetTitle() != hist2.GetTitle():
        if not found_error:
            logging.warning("Differences found in: " + histname)
            found_error = True
        logging.debug("\t--> Histogram titles differ: %s | %s" % (hist1.GetTitle(), hist2.GetTitle()))
    if hist1.ClassName() != hist2.ClassName():
        if not found_error:
            logging.warning("Differences found in: " + histname)
            found_error = True
        logging.debug("\t--> Class names differ: %s | %s" % (hist1.ClassName(), hist2.ClassName()))
    if hist1.GetNbinsX() != hist2.GetNbinsX():
        if not found_error:
            logging.warning("Differences found in: " + histname)
            found_error = True
        logging.debug("\t--> Value for NbinsX differ: %s | %s" % (hist1.GetNbinsX(), hist2.GetNbinsX()))
    if hist1.GetNbinsY() != hist2.GetNbinsY():
        if not found_error:
            logging.warning("Differences found in: " + histname)
            found_error = True
        logging.debug("\t--> Value for NbinsY differ: %s | %s" % (hist1.GetNbinsY(), hist2.GetNbinsY()))
    if hist1.GetNbinsZ() != hist2.GetNbinsZ():
        if not found_error:
            logging.warning("Differences found in: " + histname)
            found_error = True
        logging.debug("\t--> Value for NbinsZ differ: %s | %s" % (hist1.GetNbinsZ(), hist2.GetNbinsZ()))
    if hist1.GetXaxis().GetTitle() != hist2.GetXaxis().GetTitle():
        if not found_error:
            logging.warning("Differences found in: " + histname)
            found_error = True
        logging.debug("\t--> X axis titles differ: %s | %s" % (hist1.GetXaxis().GetTitle(), hist2.GetXaxis().GetTitle()))
    if hist1.GetYaxis().GetTitle() != hist2.GetYaxis().GetTitle():
        if not found_error:
            logging.warning("Differences found in: " + histname)
            found_error = True
        logging.debug("\t--> Y axis titles differ: %s | %s" % (hist1.GetYaxis().GetTitle(), hist2.GetYaxis().GetTitle()))
    if hist1.GetZaxis().GetTitle() != hist2.GetZaxis().GetTitle():
        if not found_error:
            logging.warning("Differences found in: " + histname)
            found_error = True
        logging.debug("\t--> Z axis titles differ: %s | %s" % (hist1.GetZaxis().GetTitle(), hist2.GetZaxis().GetTitle()))
    if hist1.GetEffectiveEntries() != hist2.GetEffectiveEntries():
        if not found_error:
            logging.warning("Differences found in: " + histname)
            found_error = True
        logging.debug("\t--> Total entries differ: %s | %s" % (hist1.GetEffectiveEntries(), hist2.GetEffectiveEntries()))
    return not found_error


# Make a bin-by-bin comparison for two histogram objects.
def CompareHistogramBins(file1, file2, histname):
    hist1 = file1.Get(histname)
    hist2 = file2.Get(histname)
    if not hist1:
        return
    if not hist2:
        return
    # Make sure that bin numbers are not changed
    if hist1.GetNbinsX() != hist2.GetNbinsX() or hist1.GetNbinsY() != hist2.GetNbinsY() or hist1.GetNbinsZ() != hist2.GetNbinsZ():
        logging.debug("\t--> Bin numbers changed, skipping bin-by-bin comparison")
        return False
    # Now do the actual bin-by-bin comparison
    found_error = False
    for x in range(0, hist1.GetNbinsX() + 1):
        for y in range(0, hist1.GetNbinsY() + 1):
            for z in range(0, hist1.GetNbinsZ() + 1):
                lin_bin_number = hist1.GetBin(x, y, z)
                if hist1.GetBinContent(lin_bin_number) != hist2.GetBinContent(lin_bin_number):
                    if not found_error:
                        logging.warning("Differences found in: " + histname)
                        found_error = True
                    logging.debug("\t--> Bin contents differ for bin {0}, {1}, {2}: {3} | {4}".format(x, y, z, hist1.GetBinContent(lin_bin_number), hist2.GetBinContent(lin_bin_number)))
    return not found_error


# ==========================================================
#  M A I N   F U N C T I O N
# ==========================================================
if __name__ == "__main__":
    # Set up the logging package (logging to file and streaming to console)
    logfile = 'compare.log'
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        filename='./%s' % logfile,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input1", help="first ROOT file to compare")
    parser.add_argument("input2", help="second ROOT file to compare")
    parser.add_argument("-d", "--detailed", help="compare histograms bin by bin (takes some time)", action="store_true")
    parser.add_argument("-i", "--ignore", help="ignore all sorts of warnings and continue running", action="store_true")
    args = parser.parse_args()

    if args.ignore:
        logging.info("Option '--ignore' was given, so any warnings will be ignored.")
    if args.detailed:
        logging.info("Option '--detailed' was given, so histograms will be checked bin by bin.")

    from ROOT import TFile, TDirectory

    file1 = TFile.Open(args.input1)
    file2 = TFile.Open(args.input2)

    run = GetRunNumber(file1, file2)


    # ======================================================
    # First check if directory structure is identical
    # ======================================================
    directories1 = GetDirectories(file1, run)
    logging.info("Found %s directories in file %s" % (len(directories1), file1.GetName()))
    directories2 = GetDirectories(file2, run)
    logging.info("Found %s directories in file %s" % (len(directories2), file2.GetName()))

    if not CompareLists(directories1, directories2) and not args.ignore:
        logging.error("Found warnings. To ignore them, use option '--ignore'.")
        sys.exit(-1)


    # ======================================================
    # Then check if all histograms are found in both files.
    # ======================================================
    hists1 = GetHistograms(file1, directories1)
    logging.info("Found %s histograms in file %s" % (len(hists1), file1.GetName()))
    hists2 = GetHistograms(file2, directories2)
    logging.info("Found %s histograms in file %s" % (len(hists2), file2.GetName()))

    if not CompareLists(hists1, hists2) and not args.ignore:
        logging.error("Found warnings. To ignore them, use option '--ignore'.")
        sys.exit(-1)


    # ======================================================
    # Now make a histogram-by-histogram comparison (for the intersection).
    # ======================================================
    intersect = set(hists1).intersection(hists2)
    logging.info("The two files have %s common histograms. Comparing histograms now ..." % len(intersect))

    for histname in sorted(intersect):
        logging.debug("Checking histogram %s ..." % histname)
        found_error = False
        # Make a general comparison (titles, axes etc.).
        if not CompareHistograms(file1, file2, histname):
            found_error = True
        # Make a bin-by-bin comparison if option '--detailed' was given.
        if args.detailed and not CompareHistogramBins(file1, file2, histname):
            found_error = True
        if found_error and not args.ignore:
            logging.error("Found warnings. To ignore them, use option '--ignore'.")
            sys.exit(-1)


    if args.ignore:
        logging.info("Warnings have been ignored, please check log file '%s' for details." % logfile)
    logging.info("Exiting without errors")

# end of file
