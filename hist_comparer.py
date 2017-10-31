#!/usr/bin/python

if __name__ == "__main__":
    # Parse arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("input1", help="first ROOT file to compare")
    parser.add_argument("input2", help="second ROOT file to compare")
    parser.add_argument("-d", "--detailed", help="compare histograms bin by bin (takes some time)", action="store_true")
    parser.add_argument("-i", "--ignore", help="ignore all sorts of warnings and continue running", action="store_true")
    args = parser.parse_args()

    from ROOT import TFile, TDirectory

    file1 = TFile.Open(args.input1)
    file2 = TFile.Open(args.input2)

# end of file
