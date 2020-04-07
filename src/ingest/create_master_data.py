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
                venue_dict = {
                    'name': show['venue']['venue_name'],
                    'city': show['venue']['city'],
                    'state': show['venue']['state']
                }
            except:
                logger.error(f"Could not parse show {show['show_url']}")
            add_venue_to_database([venue_dict], show['show_url'])


            # Process Songs and Song Guests From Antsmarching
            try:
                songs_list = []
                guests_list = []
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

                # Add Songs
                if len(songs_list) > 0:
                    add_songs_to_database(songs_list, show['show_url'])
                else:
                    logger.warning(f"No songs in this setlist: {show['show_url']}")

                # Add Guests
                if len(guests_list) > 0:
                    add_guests_to_database(guests_list, show['show_url'])

            except:
                logger.error(f"Could not parse songs from setlist. {show['show_url']}")


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