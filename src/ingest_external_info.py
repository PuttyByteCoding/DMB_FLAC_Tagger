import json
import requests
import config
from loguru import logger

def main():
    with open("/Volumes/RAID/Code/Python3/DMB_FLAC_Tagger/ExternalData/results_1989-2019.txt", "rb") as f:
        logger.info("Reading show data from JSON file")
        show_list = json.load(f)
        shows_processed = 0
        shows_count = len(show_list)
        for show in show_list:
            shows_processed += 1

            # Process Venue Info
            logger.info(f"Processing show {shows_processed} of {shows_count}")
            try:
                venue_dict = {
                    'name': show['venue']['venue_name'],
                    'city': show['venue']['city'],
                    'state': show['venue']['state'],
                    'country': show['venue']['venue_name'],
                }
                if show['venue']['state'] in us_states_list:
                    venue_dict['country'] = "USA"
                else:
                    venue_dict['country'] = "Need to determine, and update venue. Not in USA"
            except:
                logger.error(f"Could not parse show {show['venue'][1]}")
            add_venue_to_database(venue_dict)

            # Process Guest Info

            # Process Songs From Antsmarching
            try:
                songs_list = []
                for song in show['setlist']:
                    song_dict = {'name': song['song_name']}
                    songs_list.append(song_dict)
                if len(songs_list) > 0:
                    add_songs_to_database(songs_list)
                else:
                    logger.warning(f"No songs in this setlist: {show['setlist']}")
            except:
                logger.error(f"Could not parse songs from setlist. {show['setlist']}")


def add_songs_to_database(songs_list):
    session = requests.Session()
    request = session.post(f'{config.webserver_for_api}/songs/',
                           headers={
                               'Content-type': 'application/json',
                               'Accept': 'text/plain'},
                           data=json.dumps(songs_list))
    if request.status_code == 200:
        logger.info(f"Added Songs to database,")
        return True
    else:
        logger.warning(f"Failed to add Songs to database.")
        return False

def add_venue_to_database(venue_dict):
    session = requests.Session()
    request = session.post(f'{config.webserver_for_api}/venues/',
                           headers={
                               'Content-type': 'application/json',
                               'Accept': 'text/plain'},
                           data=json.dumps(venue_dict))
    if request.status_code == 200:
        logger.info(f"Added Venue to database: {venue_dict['name']}")
        return True
    else:
        logger.warning(f"Failed to add Venue to database: {venue_dict['name']}")
        return False




if __name__ == '__main__':
    us_states_list = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DE", "FL", "GA", "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC", "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]
    main()