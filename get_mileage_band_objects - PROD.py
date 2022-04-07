import requests
import json
import pandas as pd


click_url = "https://fse-na-int01.cloud.clicksoftware.com/SO/api"
creds = "YXdzLWludGVncmF0aW9uc0BNYXJhdGhvblA6WXVHazh1Rlc2SGNlYXgh"

new_ca_list = []
full_ca_list = []
new_swd_list = []
full_swd_list = []
new_asset_list = []
full_asset_list = []
mileage_bands_list = []
distance_list = []
distance_calc_list = []


############### Get ID of Bakken region ##################

url = click_url + "/objects/Region?$filter=Name eq 'Bakken'"

post_payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Authorization': 'Basic ' + creds,
    'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
}

response = requests.request("GET", url, headers=headers, data=post_payload, files=files)

bkn_region_id = json.loads(response.text)
bkn_region_id = bkn_region_id[0]['Key']

############### Get ID of Water Hauling ##################

url = click_url + "/objects/MROVendorType?$filter=Name eq 'Water Hauling Vendor'"

post_payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Authorization': 'Basic ' + creds,
    'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
}

response = requests.request("GET", url, headers=headers, data=post_payload, files=files)

water_hauling_id = json.loads(response.text)
water_hauling_id = water_hauling_id[0]['Key']

###### GATHER CUSTOMER ACCOUNT, ASSET, AND SWD ITEMS ##########################

# Gather data and split out new items - Customer Account 

# create new customer account list

url = click_url + "/objects/CustomerAccount?$filter=AWS_MileageBand eq -1 and Region/Key eq " + str(bkn_region_id) + "and Active eq true and VendorType/Key eq " + str(water_hauling_id)

post_payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Authorization': 'Basic ' + creds,
    'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
}

response = requests.request("GET", url, headers=headers, data=post_payload, files=files)

#print(response.text)
customer_account_list = json.loads(response.text)


for customer_account in customer_account_list:
    ca_item = {
        "ca_name": customer_account['Name'],
        "ca_key": customer_account['Key'],
        "ca_region": customer_account['Region'],
        "ca_id": customer_account['CustomerID'],
        'key': customer_account['Key']
    }

    new_ca_list.append(ca_item)


# create full customer account list
url = click_url + "/objects/CustomerAccount?$filter=AWS_MileageBand ne -1 and Region/Key eq " + str(bkn_region_id) + "and Active eq true and VendorType/Key eq " + str(water_hauling_id)

post_payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Authorization': 'Basic ' + creds,
    'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
}

response = requests.request("GET", url, headers=headers, data=post_payload, files=files)
#print(response.text)

customer_account_list = json.loads(response.text)

for customer_account in customer_account_list:
    ca_item = {
        "ca_name": customer_account['Name'],
        "ca_key": customer_account['Key'],
        "ca_region": customer_account['Region'],
        "ca_id": customer_account['CustomerID']
    }

    full_ca_list.append(ca_item)

# Gather data and split out new items - SWD

url = click_url + "/objects/MROSWD?$filter=AWS_MileageBand eq -1 and Region/Key eq " + str(bkn_region_id) + "and Active eq true"

post_payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Authorization': 'Basic ' + creds,
    'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
}

response = requests.request("GET", url, headers=headers, data=post_payload, files=files)

#print(response.text)
swd_list = json.loads(response.text)

for swd in swd_list:
    swd_item = {
        "swd_name": swd['Name'],
        "swd_key": swd['Key'],
        "swd_district_key": swd['WorkingArea']["Key"],
        "swd_district": swd['WorkingArea']["@DisplayString"],
        "swd_lat": swd['Latitude'],
        "swd_long": swd['Longitude'],
        "key": swd['Key']
    }

    new_swd_list.append(swd_item)

url = click_url + "/objects/MROSWD?$filter=AWS_MileageBand ne -1 and Region/Key eq " + str(bkn_region_id) + "and Active eq true"

post_payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Authorization': 'Basic ' + creds,
    'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
}

response = requests.request("GET", url, headers=headers, data=post_payload, files=files)
#print(response.text)

swd_list = json.loads(response.text)

for swd in swd_list:
    swd_item = {
        "swd_name": swd['Name'],
        "swd_key": swd['Key'],
        "swd_region": swd['Region'],
        "swd_district_key": swd['WorkingArea']['Key'],
        "swd_district": swd['WorkingArea']["@DisplayString"],
        "swd_lat": swd['Latitude'],
        "swd_long": swd['Longitude']
    }

    full_swd_list.append(swd_item)

# Gather data and split out new items - Asset

url = click_url + "/objects/Asset?$filter=AWS_MileageBand eq -1 and Region/Key eq " + str(bkn_region_id) + "and MROWorkingArea/Key ne -1"

post_payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Authorization': 'Basic ' + creds,
    'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
}

response = requests.request("GET", url, headers=headers, data=post_payload, files=files)


asset_list = json.loads(response.text)

for asset in asset_list:
    asset_item = {
        "asset_name": asset['Name'],
        "asset_key": asset['Key'],
        "asset_id": asset['AssetID'],
        "asset_region": asset['Region'],
        "asset_lat": asset['MROLatitude'],
        "asset_long": asset['MROLongitude'],
        "asset_district": asset['MROWorkingArea']['@DisplayString'],
        "asset_district_key": asset['MROWorkingArea']['Key'],
        "asset_phase": asset['WellPhases'][0]['@DisplayString'],
        "asset_phase_key": asset['WellPhases'][0]['Key'],
        'asset_route': asset['MRORoute'],
        "key": asset['Key']
    }

    new_asset_list.append(asset_item)


url = click_url + "/objects/Asset?$filter=AWS_MileageBand ne -1 and Region/Key eq " + str(bkn_region_id) + "and MROWorkingArea/Key ne -1"

post_payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Authorization': 'Basic ' + creds,
    'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
}

response = requests.request("GET", url, headers=headers, data=post_payload, files=files)

asset_list = json.loads(response.text)

for asset in asset_list:
    asset_item = {
        "asset_name": asset['Name'],
        "asset_key": asset['Key'],
        "asset_id": asset['AssetID'],
        "asset_region": asset['Region'],
        "asset_lat": asset['MROLatitude'],
        "asset_long": asset['MROLongitude'],
        "asset_district": asset['MROWorkingArea']['@DisplayString'],
        "asset_district_key": asset['MROWorkingArea']['Key'],
        "asset_phase": asset['WellPhases'][0]['@DisplayString'],
        "asset_phase_key": asset['WellPhases'][0]['Key'],
        'asset_route': asset['MRORoute']
    }

    full_asset_list.append(asset_item)


########### GENERATE COMBINATIONS OF BANDS #####################

def assetAssign():
    if asset['asset_district_key'] == swd['swd_district_key']:
        asset_item = {
            "asset_name": asset['asset_name'],
            "asset_key": asset['asset_key'],
            "asset_id": asset['asset_id'],
            "asset_lat": asset['asset_lat'],
            "asset_long": asset['asset_long'],
            "asset_district": asset['asset_district'],
            "asset_district_key": asset['asset_district_key'],
            "asset_phase": asset['asset_phase'],
            "asset_phase_key": asset['asset_phase_key'],
            'asset_route': asset['asset_route'],
            "ca_name": ca['ca_name'],
            "ca_key": ca['ca_key'],
            "ca_id": ca['ca_id'],
            "swd_name": swd['swd_name'],
            "swd_key": swd['swd_key'],
            "swd_lat": swd['swd_lat'],
            "swd_long": swd['swd_long'],
            "swd_district": swd['swd_district'],
            "swd_district_key": swd['swd_district_key'],
            'distance': 0,
            'calculated_miles': 0,
            "mb_key": ""
        }
        distance_list.append(asset_item)

for asset in new_asset_list:
    for swd in full_swd_list:
        for ca in full_ca_list:
            assetAssign()

for swd in new_swd_list:
    for asset in full_asset_list:
        for ca in full_ca_list:
            assetAssign()

for ca in new_ca_list:
    for asset in full_asset_list:
        for swd in full_swd_list:
            assetAssign()


############## CALCULATE DISTANCES ############################


batch = []
batch_list = []
increment = 0

for item in distance_list:
    a_lat = item['asset_lat'] / 1000000
    a_long = item['asset_long'] / 1000000
    s_lat = item['swd_lat'] / 1000000
    s_long = item['swd_long'] / 1000000
    query_string = "?query=" + str(a_lat) + "," + str(a_long) + ":" + str(s_lat) + "," + str(s_long) + "&routeType=shortest"
    query = {
        "query": query_string
    }
    batch.append(query)
    increment = increment + 1

    if increment == 100:
        batch_list.append(batch)
        batch = []
        increment = 0

batch_list.append(batch)

for batch in batch_list:
    payload = {
    "batchItems": batch
    }
    url = "https://atlas.microsoft.com/route/directions/batch/sync/json?api-version=1.0&subscription-key=t_rz7yuKfHqX75sCCCJqYduDnV4Ln1Tzdh5iNum8bCU"

    post_payload = json.dumps(payload)
    files = {}
    headers = {
        'Content-Type': 'application/json',
        'Cache-Control': 'no-cache',
        'Connection': 'keep-alive',
        'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
    }

    response = requests.request("POST", url, headers=headers, data=post_payload, files=files)

    distance_test = json.loads(response.text)
    distance_test = distance_test['batchItems']
    distance_calc_list.append(distance_test)


iteration = 0


for list in distance_calc_list:
    for calc in list:
        distance = calc['response']['routes'][0]['summary']['lengthInMeters'] / 1000 / 1.609
        distance_list[iteration]['distance'] = round(distance)
        distance_list[iteration]['calculated_miles'] = round(distance, 2)
        iteration += 1


######### GET MILEAGE BANDS ####################################

url = click_url + "/objects/MROMileageBands"

post_payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Authorization': 'Basic ' + creds,
    'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
}

response = requests.request("GET", url, headers=headers, data=post_payload, files=files)
mileage_bands = json.loads(response.text)


for band in mileage_bands:
    item = {
        "mb_name": band['Name'],
        "mb_key": band['Key'],
        "mb_phase_key": band['MROWellPhase']["Key"],
        "min_dist": ''.join([ele for ele in band['Name'][0:2] if ele.isdigit()]),
        "max_dist": ''.join([ele for ele in band['Name'][2:5] if ele.isdigit()])

    }

    mileage_bands_list.append(item)

for band in mileage_bands_list:
    if band['max_dist'] == '':
        band['max_dist'] = 1000

mileage_band_df = pd.DataFrame(mileage_bands_list)


#### ASSIGN MILEAGE BANDS

def assignMileageBand(list, mblist):
    for i in range(len(list)):
        for j in range(len(mblist)):
            if list[i]['asset_phase_key'] == mblist[j]['mb_phase_key'] and list[i]['distance'] <= int(mblist[j]['max_dist']) and list[i]['distance'] >= int(mblist[j]['min_dist']):
                list[i]['mb_key'] = mblist[j]['mb_key']



assignMileageBand(distance_list, mileage_bands_list)
distance_list_df = pd.DataFrame(distance_list)


distance_list_df['ca_key']=distance_list_df['ca_key'].astype(str)
distance_list_df['mb_key']=distance_list_df['mb_key'].astype(str)


################# ASSIGN UNIT RATE #################################

# Get Unit Rate
url = click_url + "/objects/MROTMSMileageBands?$filter=MROMileageBandRateForCreation eq true"

post_payload = {}
files = {}
headers = {
    'Content-Type': 'application/json',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Authorization': 'Basic ' + creds,
    'Cookie': 'lang=en-US; mxp=52964abf804784edde0723a90214f150'
}

response = requests.request("GET", url, headers=headers, data=post_payload, files=files)


unit_rate_table = json.loads(response.text)
unit_rate_list=[]

for rate in unit_rate_table:
    item = {
        "unit_rate": rate['UnitRate'],
        "ca_key": rate['CustomerAccount']['Key'],
        "ca_name": rate['CustomerAccount']['@DisplayString'],
        "mb_key": rate['MROMileageBands']['Key'],
        "mro_mb": rate['MROMileageBands']['@DisplayString'],
        "start_date":rate['MRORateStartDate'],
        "end_date":rate['MRORateEndDate'],
        "unit_of_measure": rate['UnitOfMeasure']['Key']

    }

    unit_rate_list.append(item)

unit_rate_df = pd.DataFrame(unit_rate_list)

unit_rate_df['ca_key']=unit_rate_df['ca_key'].astype(str)
unit_rate_df['mb_key']=unit_rate_df['mb_key'].astype(str)

complete_df = pd.merge(distance_list_df, unit_rate_df, how='left', on=['ca_key', 'mb_key'])
complete_df = complete_df.dropna(how='any', axis=0)

# export to csv
complete_df.to_csv('complete_df.csv', index= False)

complete_dict = complete_df.to_dict('records')



############### EXPORT #####################################

url = click_url + '/objects/MROTMSMileageBands'

for item in complete_dict:
    name = item['asset_name'] + item['swd_name'] + item['ca_name_x']
    payload = json.dumps({
        "@objectType": "MROTMSMileageBands",
        "@createOrUpdate": True,
        "Name": name,
        "WellSite": item['asset_key'],
        "SWD": item['swd_key'],
        "UnitRate": item['unit_rate'],
        "UnitOfMeasure": item['unit_of_measure'],
        "MROMileageBands": item['mb_key'],
        "MRORateStartDate": item['start_date'],
        "MRORateEndDate": item['end_date'],
        "CustomerAccount": item['ca_key'],
        "MROWellPhase": item['asset_phase_key'],
        "MRORoute": item['asset_route'],
        "CustomerID": item['ca_id'],
        "AssetID": item['asset_id'],
        "MROMileageBandRateForCreation": False,
        "MROCalculatedMiles": item['calculated_miles']
    })
    
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)



#### NEW ASSETS UPDATE AWS_MILEAGEBAND FLAG

url = click_url + '/objects/Asset'

# for asset in new_asset_list change AWS_MileageBand to False
for asset in new_asset_list:

    payload = json.dumps({
        "@objectType": "Asset",
        "@createOrUpdate": True,
        "Key": asset['key'],
        "AWS_MileageBand": False,
    })

    response = requests.request("POST", url, data=payload, headers=headers)
    print(response)


#### NEW CA UPDATE AWS_MILEAGEBAND FLAG

url = click_url + '/objects/CustomerAccount'

for ca in new_ca_list:
    payload = json.dumps({
        "@objectType": "CustomerAccount",
        "@createOrUpdate": True,
        "Key": ca['key'],
        "AWS_MileageBand": False,
    })
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)

#### NEW SWD UPDATE AWS_MILEAGEBAND FLAG

url = click_url + '/objects/MROSWD'

for swd in new_swd_list:
    payload = json.dumps({
        "@objectType": "MROSWD",
        "@createOrUpdate": True,
        "Key": swd['key'],
        "AWS_MileageBand": False,
    })

    response = requests.request("POST", url, headers=headers, data=payload)
    print(response)
