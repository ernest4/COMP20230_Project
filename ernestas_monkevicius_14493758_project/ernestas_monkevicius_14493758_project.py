"""Main module."""

import sys
import optparse
from ernestas_monkevicius_14493758_project.algorithms import ItineraryOptimizer
import pandas as pd

def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]
    
    #parsing command line arguments
    parser = optparse.OptionParser(usage="Usage: %prog [-i input_file][-c currency_file][-C country_currency_file][-a airports_file][-A aircraft_file][-o output_file]")
    parser.add_option('-i', '--input', dest="inputFile", help="The input .csv file which will be processed.")
    parser.add_option('-o', '--output', dest="outputFile", help="the output .csv file where the answer will be written. If none is provided, a default bestroutes.csv will be created.")
    parser.add_option('-c', '--currency', dest="currencyFile", help="The input .csv file which contains currency exchange rate information. If none is provided a default one will be used, however, this will not be the latest up to date information.")
    parser.add_option('-C', '--country', dest="countryCurrencyFile", help="The input .csv file which contains countries and their currencies. If none is provided a default one will be used, however, this will not be the latest up to date information.")
    parser.add_option('-a', '--airports', dest="airportsFile", help="The input .csv file which contains airports. If none is provided a default one will be used, however, this will not be the latest up to date information.")
    parser.add_option('-A', '--aircraft', dest="aircraftFile", help="The input .csv file which contains aircraft. If none is provided a default one will be used, however, this will not be the latest up to date information.")
    
    opts, args = parser.parse_args(argv)
    #argument handling
    if opts.inputFile is None:
        parser.error("Argument [-i input_file] required. For more help use -h or --help.")
        
    #default files dictionary. In case input files are incorrect or not provided as they are optional.
    defaultFilesDict = { 'outputFile'  : 'bestroutes.csv',
                          'currencyFile' : 'data/currencyrates.csv',
                          'countryCurrencyFile' : 'data/countrycurrency.csv',
                          'airportsFile' : 'data/airport.csv',
                          'aircraftFile' : 'data/aircraft.csv'}
    
    #This block of code checks the command line arguments and assigns default
    #files to file options which were not provided by the user.
    inputFileOptionsDict = vars(opts) #extract the command line arguments
    for fileOption in inputFileOptionsDict: #Check if input is given, if not, provide default files.
        if inputFileOptionsDict[fileOption] is None:
            inputFileOptionsDict[fileOption] = defaultFilesDict[fileOption]
        elif not inputFileOptionsDict[fileOption].endswith('.csv'): #If file is provided, make sure it's correct type.
            parser.error("Expected .csv file, instead of "+inputFileOptionsDict[fileOption])
        
    #ItineraryOptimizer is the workhorse of this program, takes in itineraries and produces best routes
    itineraryOptimizer = ItineraryOptimizer(inputFileOptionsDict)
    
    #return all optimized itineraries
    optimizedItineraries = itineraryOptimizer.getOptimizedItinerary()
    
    #Output optimized itineraries to .csv using pandas
    pd.DataFrame(optimizedItineraries).to_csv(inputFileOptionsDict['outputFile'], header=False, index=False)
    
if __name__ == "__main__":
    main()
    