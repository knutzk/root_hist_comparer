#!/usr/bin/python

if __name__ == "__main__":
    # Set up the logging package (logging to file and streaming to console)
    import logging
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

# end of file
