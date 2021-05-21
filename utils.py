import requests
from typing import Union
from fake_useragent import UserAgent
from requests.exceptions import HTTPError

def _callAPI( url) -> Union[HTTPError, dict]:
    userAgent = UserAgent()
    header = {'User-Agent': 'Mozilla/5.0 (X11; CrOS i686 4319.74.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/29.0.1547.57 Safari/537.36'}
    response = requests.get(url, headers=header)
    try:
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:
        return e
    return response.json()

def fetchAllStates(primitiveInput):
    return _callAPI(primitiveInput.cowinAllStatesURL)

def fetchAllDistricts(primitiveInput):
    if not isinstance(primitiveInput.stateID, int):
        return _callAPI(primitiveInput.cowinAllDistrictsURL)
    else:
        return 'No/Incorrect StateId Passed'

def filter_center_by_age(primitiveInput):
    original_centers = primitiveInput.searchResult.get('centers')
    filtered_centers = {'centers': []}
    print(original_centers)
    for index, center in enumerate(original_centers):
        filtered_sessions = []
        for session in center.get('sessions'):
            if session.get('min_age_limit') == int(primitiveInput.minAgeLimit) and session.get('available_capacity') > 0:
                filtered_sessions.append(session)
        if len(filtered_sessions) > 0:
            center['sessions'] = filtered_sessions
            filtered_centers['centers'].append(center)
    print(filtered_centers)
    return filtered_centers

def updatedOutputFormat(primitiveInput):
    primitiveInput.slots = 0
    formatted_output = []
    output_to_format = primitiveInput.searchResult
    if isinstance(primitiveInput.filteredOutputByAge, dict):
        output_to_format = primitiveInput.filteredOutputByAge
    filteredCenters = output_to_format.get('centers')
    for center in range(len(filteredCenters)):
        for session in range(len(filteredCenters[center]["sessions"])):
            formatted_output.append(f'There is/are {filteredCenters[center]["sessions"][session]["available_capacity"]} '
                                      f'slots available in {filteredCenters[center]["name"]} at {filteredCenters[center]["district_name"]},{filteredCenters[center]["state_name"]} on '
                                      f'{filteredCenters[center]["sessions"][session]["date"]} for {filteredCenters[center]["sessions"][session]["vaccine"]}')
            primitiveInput.slots += filteredCenters[center]["sessions"][session]["available_capacity"]
    primitiveInput.formattedResult = formatted_output
    # For Desktop notification
    # if len(filteredOutput) > 0:
    #     notification.notify(title='Slots Available',
    #                         message=f'{slots} slots available in {filteredCenters[center]["district_name"]}')
    # else:
    #     pass


def get_availability_by_district(primitiveInput):
    primitiveInput.searchResult = _callAPI(primitiveInput.cowinSearchByDistrictURL)
    if not isinstance(primitiveInput.minAgeLimit, int) and isinstance(primitiveInput.searchResult, dict):
        primitiveInput.filteredOutputByAge = filter_center_by_age(primitiveInput)
        if len(primitiveInput.filteredOutputByAge['centers']) > 0:
            updatedOutputFormat(primitiveInput)
            return primitiveInput.formattedResult
        else:
            return None

def setAttributes(primitiveInput, stateID, districtID, ageFilter, date):
    primitiveInput.stateID = stateID
    primitiveInput.districtID = districtID
    primitiveInput.minAgeLimit = ageFilter
    primitiveInput.searchDate = date

    primitiveInput.cowinAllStatesURL = 'https://cdn-api.co-vin.in/api/v2/admin/location/states'
    primitiveInput.cowinAllDistrictsURL = f"https://cdn-api.co-vin.in/api/v2/admin/location/districts/{primitiveInput.stateID}"
    primitiveInput.cowinSearchByDistrictURL = f'https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict?district_id={primitiveInput.districtID}&date={primitiveInput.searchDate}'

