'''
Created on 15 Apr 2018

@author: ernest
'''

def cleanUp(df):
    '''Drops duplicate rows and rows with NaN values in argument dataframe'''
    return df.dropna().drop_duplicates()
    