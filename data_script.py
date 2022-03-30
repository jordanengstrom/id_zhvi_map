import pandas as pd
import json
from requests import Session
import re

print('\n[*] Fetching data...')
# Only need to one this once:
# # region FETCH, WRITE IDAHO ZIP CODE DATA
# s = Session()
# zip_codes_url = 'https://raw.githubusercontent.com/OpenDataDE/State-zip-code-GeoJSON/master/id_idaho_zip_codes' \
#                 '_geo.min.json'
# data = s.get(url=zip_codes_url).json()
#
# # extract zipcode for id matching
# for feature in data['features']:
#     feature['id'] = feature['properties']['ZCTA5CE10']
#
# with open('./zhvi_data/id_idaho_zip_codes_geo.min.json', 'w') as fp:
#     json.dump(data, fp)
# # endregion FETCH, WRITE IDAHO ZIP CODE DATA


# region READ IDAHO ZIP CODE DATA
with open('./zhvi_data/id_idaho_zip_codes_geo.min.json', 'r') as fp:
    zipcode_data = json.load(fp)
print('[*] Zip code geojson loaded...')
# endregion READ IDAHO ZIP CODE DATA

# region ZILLOW HOME VALUE INDEX
# Zip codes obtained from:
# https://gist.githubusercontent.com/erichurst/7882666/raw/5bdc46db47d9515269ab12ed6fb2850377fd869e/US%2520Zip%2520Codes%2520from%25202013%2520Government%2520Data
id_df = pd.read_csv('./zhvi_data/zip_zhvi_2022.csv')
id_df = id_df.query('StateName == "ID"')
id_df.reset_index(drop=True, inplace=True)
print('[*] Idaho dataframe filtered')
# endregion ZILLOW HOME VALUE INDEX

# region DATA CLEANUP
print('[*] Appending lat/lon to Idaho dataframe...')
zip_df = pd.read_csv('./zhvi_data/zipcodes.csv')
id_df = id_df.merge(right=zip_df, how='inner', left_on='RegionName', right_on='ZIP')
x = 0

# drop most columns:
cols = id_df.columns.to_list()
pattern = r'\d\d\d\d-\d\d-\d\d'
# features = ['City', 'State', 'ZIP', 'LAT', 'LNG']
months = []
for c in cols:
    match = re.search(pattern, c)
    if match:
        months.append(match.__getitem__(0))
#
# id_df = id_df.filter(features, axis=1)
# endregion DATA CLEANUP

print('[*] Data script complete!\n')
