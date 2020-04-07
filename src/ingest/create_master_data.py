import json
import requests
import config
from loguru import logger

def main():
    """
    Run this to populate Master versions of:
        - Venues
        - SongTitles
        - Guests
    This data will be used when tagging my shows
    """
    # Setup unknown entries
    unknown_venue = [{'name': 'Unknown', 'city': 'Unknown', 'state': 'Unknown'}]
    add_venue_to_database(unknown_venue, "No URL.  Adding Value for unknown")

    unknown_song = [{'name': 'Unknown'}]
    add_songs_to_database(unknown_song, "No URL.  Adding Value for unknown")

    unknown_guest = [{'name': 'Unknown', 'instrument': 'Unknown'}]
    add_guests_to_database(unknown_guest, "No URL.  Adding Value for unknown")

    with open("/Users/mark/PycharmProjects/DMB_FLAC_Tagger/ExternalData/results_1989-2019.txt", "rb") as f:
        logger.info("Reading show data from JSON file")
        show_list = json.load(f)
        shows_processed = 0
        shows_count = len(show_list)
    for show in show_list:
        shows_processed += 1

        # Process Venue Info
        logger.info(f"Processing show {shows_processed} of {shows_count}")
        try:
            # Check for "Could not parse error
            venue_dict = {
                'name': show['venue']['venue_name'],
                'city': show['venue']['city'],
                'state': show['venue']['state']
            }
        except Exception as e1:
            # I know a try catch in a try catch is a ducttape fix, but I don't want to spend too much time using pydantic right now.
            # #TODO: Do this using pydantic
            try:
                if show['venue'][0] == 'Could not parse':
                    logger.info(f"Site Scrapper failed to parse the venue info: {show['show_url']}")
            except Exception as e2:
                logger.error(f"Could not parse show.  Unknown Error {show['show_url']} {e1}")
        add_venue_to_database([venue_dict], show['show_url'])


        # Process Songs and Song Guests From Antsmarching
        songs_list = []
        guests_list = []
        try:
            for song in show['setlist']:
                song_dict = {'name': song['song_name']}
                songs_list.append(song_dict)
                if song['guests'] != "":
                    # Ants stores guests as comma separated first names
                    for g in song['guests'].split(","):
                        guest = {
                            'name': g.strip(),
                            'instrument': ''
                        }
                        guests_list.append(guest)

        except Exception as e1:
            # I know a try catch in a try catch is a ducttape fix, but I don't want to spend too much time using pydantic right now.
            # #TODO: Do this using pydantic
            try:
                if show['setlist'][0] == 'Could not parse':
                    logger.info(f"Site Scrapper failed to parse the setlist: {show['show_url']}")
            except Exception as e2:
                logger.error(f"Could not parse songs from setlist. Unknown Error {show['show_url']} {e1}")

        # Add Songs
        if len(songs_list) > 0:
            add_songs_to_database(songs_list, show['show_url'])
        else:
            logger.info(f"No songs in this setlist: {show['show_url']}")

        # Add Guests
        if len(guests_list) > 0:
            add_guests_to_database(guests_list, show['show_url'])


def add_guests_to_database(guest_list, show_url):
    session = requests.Session()
    request = session.post(f'{config.webserver_for_api}/guests/',
                           headers={
                               'Content-type': 'application/json',
                               'Accept': 'text/plain'},
                           data=json.dumps(guest_list))
    if request.status_code == 200:
        logger.info(f"Added Guests to database: {show_url}")
        return True
    else:
        logger.warning(f"Failed to add Guests to database: {guest_list} {show_url}.")
        return False

def add_songs_to_database(songs_list, show_url):
    session = requests.Session()
    request = session.post(f'{config.webserver_for_api}/songs/',
                           headers={
                               'Content-type': 'application/json',
                               'Accept': 'text/plain'},
                           data=json.dumps(songs_list))
    if request.status_code == 200:
        logger.info(f"Added Songs to database: {show_url}")
        return True
    else:
        logger.warning(f"Failed to add Songs to database: {songs_list} {show_url}.")
        return False

def add_venue_to_database(venue_dict, show_url):
    session = requests.Session()
    request = session.post(f'{config.webserver_for_api}/venues/',
                           headers={
                               'Content-type': 'application/json',
                               'Accept': 'text/plain'},
                           data=json.dumps(venue_dict))
    if request.status_code == 200:
        logger.info(f"Added Venue to database: {show_url}")
        return True
    else:
        logger.warning(f"Failed to add Venue to database: {venue_dict} {show_url}")
        return False


if __name__ == '__main__':
    main()
