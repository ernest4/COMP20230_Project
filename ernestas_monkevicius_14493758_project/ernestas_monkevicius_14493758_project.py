"""Main module."""

import sys
import optparse

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
        
    #argument error handling
    #if len(argv) < 1 or argv[0] != '--input':
    #    print("Usage: -i, --input <input.csv>")
    #    sys.exit(2)
    
    #parsing command line arguments
    parser = optparse.OptionParser(usage="Usage: %prog [-i input_file][-c currency_file][-C country_currency_file][-a airports_file][-A aircraft_file][-o output_file]")
    parser.add_option('-i', '--input', dest="inputFile", help="The input .csv file which will be processed.")
    parser.add_option('-o', '--output', dest="outputFile", help="the output .csv file where the answer will be written. If none is provided, a default bestroutes.csv will be created.")
    parser.add_option('-c', '--currency', dest="currencyFile", help="The input .csv file which contains currency exchange rate information. If none is provided a default one will be used, however, this will not be the latest up to date information.")
    parser.add_option('-C', '--country', dest="countryCurrencyFile", help="The input .csv file which contains countries and their currencies. If none is provided a default one will be used, however, this will not be the latest up to date information.")
    parser.add_option('-a', '--airports', dest="airportsFile", help="The input .csv file which contains airports. If none is provided a default one will be used, however, this will not be the latest up to date information.")
    parser.add_option('-A', '--aircraft', dest="aircraftFile", help="The input .csv file which contains aircraft. If none is provided a default one will be used, however, this will not be the latest up to date information.")
    
    opts, args = parser.parse_args(argv)
    #argument error handling
    if opts.inputFile is None:
        parser.error("Inputs required. For more help use -h or --help.")
        
        
        
    
    print(opts) #Testing...
    
if __name__ == "__main__":
    main()