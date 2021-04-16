# The necessary import statements
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'

class DeDupe:

    # Constructor, takes a dataframe as an input
    def __init__(self, dataframe):
        self.data = dataframe
        self.duplicates = pd.DataFrame(columns=list(dataframe.columns))
        self.deDupedData = pd.DataFrame(columns=list(dataframe.columns))

    # This whole method removes the duplicates in the data
    def remove_dupes(self):

        # Putting entries with no date in badData dataframe
        self.badData = self.data.loc[self.data['pl_pubdate'].isna()]

        # Removing entries with no dates
        self.data.dropna(how='any', subset=['pl_pubdate'], inplace=True)

        # Removing entries with bad dates from data and putting it in badData
        for index, row in self.data.iterrows():
            date = self.data['pl_pubdate'][index]
            try:
                if len(date) < 8:
                    self.data['pl_pubdate'][index] = date + '-01'
                self.data['pl_pubdate'][index] = pd.to_datetime(self.data['pl_pubdate'][index])
            except:
                self.data.drop([index], inplace=True)
                self.data.reset_index(drop=True)

        # Converting dates to datetime objects
        self.data['pl_pubdate'] = pd.to_datetime(self.data['pl_pubdate'])

        # Sorting the data
        sortedData = self.data.sort_values(by=['pl_name', 'pl_pubdate'], ascending=[1, 0], inplace=False, na_position='last')

        # Store the duplicates in duplicates dataframe
        self.duplicates = pd.DataFrame(columns=list(self.data.columns))
        mask = sortedData.duplicated(subset='pl_name', keep='first')
        df_keep = sortedData.loc[~mask]
        self.duplicates = self.duplicates.append(sortedData.loc[mask])

        # Dropping the duplicates and storing the remaining in deDuped
        self.deDupedData = sortedData.drop_duplicates(subset='pl_name', keep='first', inplace=False, ignore_index=True)

        self.deDupedData.reset_index(inplace=True)

        return self.deDupedData
