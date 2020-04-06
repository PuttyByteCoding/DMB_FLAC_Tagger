import json
import requests
import config
from loguru import logger

def main():
    """
    Run this to populate create concert info from ants:
    """
    with open("/Volumes/RAID/Code/Python3/DMB_FLAC_Tagger/ExternalData/results_1989-2019.txt", "rb") as f:
        logger.info("Reading show data from JSON file")
        show_list = json.load(f)
        shows_processed = 0
        shows_count = len(show_list)
        for show in show_list:

            show_dict = {}
            shows_processed += 1
            logger.info(f"Processing show {shows_processed} of {shows_count}")

            show_dict['band_configuration'] = show['band_configuration']
            show_dict['date'] = show['date']
            show_dict['notes'] = "\n".join(show['show_notes'])
            show_dict['taper_name'] = "Unknown"
            show_dict['recording_type'] = "Unknown"
            show_dict['info_text_file_contents'] = "N/A Ants Ingest"

            # Get Venue ID
            try:
                venue_name = show['venue']['venue_name']
                venue_city = show['venue']['city']
                venue_state = show['venue']['state']
                venue_id = get_venue_id(venue_name, venue_city, venue_state)
                show_dict['venue_id'] = venue_id
            except:
                logger.error(f"Could not locate venue_id.  Setting to 1 (unknown)")
                show_dict['venue_id'] = 1

            add_concert_to_database(show_dict, show['show_url'])

            a=1

            # Proccess Setlist


            #
            # # Process Songs and Song Guests From Antsmarching
            # try:
            #     songs_list = []
            #     guests_list = []
            #     for song in show['setlist']:
            #         song_dict = {'name': song['song_name']}
            #         songs_list.append(song_dict)
            #         if song['guests'] != "":
            #             guest = {
            #                 'name': song['guests'],
            #                 'instrument': ''
            #             }
            #             guests_list.append(guest)
            #
            #     # Add Songs
            #     if len(songs_list) > 0:
            #         add_songs_to_database(songs_list, show['show_url'])
            #     else:
            #         logger.warning(f"No songs in this setlist: {show['show_url']}")
            #
            #     # Add Guests
            #     if len(guests_list) > 0:
            #         add_guests_to_database(guests_list, show['show_url'])
            #     else:
            #         logger.warning(f"No Guests in this setlist: {show['show_url']}")
            #
            # except:
            #     logger.error(f"Could not parse songs from setlist. {show['show_url']}")

def add_concert_to_database(show_dict, show_url):
    session = requests.Session()
    request = session.post(f'{config.webserver_for_api}/concerts/',
                           headers={
                               'Content-type': 'application/json',
                               'Accept': 'text/plain'},
                           data=json.dumps(show_dict))
    if request.status_code == 200:
        logger.info(f"Added Concert to database: {show_url}")
        return True
    else:
        logger.warning(f"Failed to add Concert to database: {show_dict} {show_url}.")
        return False

def get_guest_id(guest_name):
    session = requests.Session()
    request = session.get(f'{config.webserver_for_api}/guests/{guest_name}',
                           headers={
                               'Content-type': 'application/json',
                               'Accept': 'text/plain'})
    result = request.json()
    if request.status_code == 200:
        return True
    else:
        return False


def get_song_id(song_name):
    session = requests.Session()
    request = session.get(f'{config.webserver_for_api}/songs/{song_name}',
                           headers={
                               'Content-type': 'application/json',
                               'Accept': 'text/plain'})
    result = request.json()
    if request.status_code == 200:
        return True
    else:
        return False


def get_venue_id(name, city, state):
    session = requests.Session()
    request = session.post(f'{config.webserver_for_api}/venues/get_id/',
                           headers={
                               'Content-type': 'application/json',
                               'Accept': 'text/plain'},
                           data=json.dumps({
                               'name': name,
                               'city': city,
                               'state': state
                           }))
    result = request.json()
    if request.status_code == 200:
        return result
    else:
        logger.warning(f"Could not locate Venue: {name}, {city}, {state}")
        return False




if __name__ == '__main__':
    main()