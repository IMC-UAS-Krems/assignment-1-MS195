"""
platform.py
-----------
Implement the central StreamingPlatform class that orchestrates all domain entities
and provides query methods for analytics.

Classes to implement:
  - StreamingPlatform
"""
from pygments.lexers import q

from streaming.playlists import CollaborativePlaylist
from streaming.users import FamilyMember
from streaming.users import PremiumUser
from datetime import datetime, timedelta
from streaming.tracks import Song


class StreamingPlatform:
    def __init__(self, name):
        self.name = name
        self.catalogue = {}
        self.users = {}
        self.artists = {}
        self.albums = {}
        self.playlists = {}
        self.sessions = []

    def add_track(self, track):
        self.catalogue[track.track_id] = track

    def add_user(self,user):
        self.users[user.user_id] = user

    def add_artist(self, artist):
        self.artists[artist.artist_id] = artist

    def add_album(self, album):
        self.albums[album.album_id] = album

    def add_playlist(self, playlist):
        self.playlists[playlist.playlist_id] = playlist

    def record_session(self, session):
        self.sessions.append(session)

    def get_track(self, track_id):
        return self.catalogue[track_id]

    def get_user(self, user_id):
        return self.users.get(user_id) #get() search id and give the object or None

    def get_artist(self, artist_id):
        return self.artists.get(artist_id)

    def get_album(self, album_id):
        return self.albums.get(album_id)

    def all_users(self):
        return list(self.users.values()) # return the list of users

    def all_tracks(self):
        return list(self.catalogue.values()) #return all tracks



    #   Q1: Total Cumulative Listening Time
    #Method: total_listening_time_minutes(start: datetime, end: datetime) -> float
    def total_listening_time_minutes(self, start, end):
        total_seconds = 0

        for session in self.sessions:
            if session.timestamp >= start and session.timestamp <= end: #this verify if session is between START and END
                total_seconds += session.duration_listened_seconds
        return total_seconds / 60.0



    #   Q2: Average Unique Tracks per Premium User
    #Method: avg_unique_tracks_per_premium_user(days: int = 30) -> float
    def avg_unique_tracks_per_premium_user(self, days = 30):
        start = datetime.now() - timedelta(days = days) #calculates since when we start to count
        total_unique_tracks = 0
        nr_premium_users = 0

        for user in self.users.values():
            if isinstance(user, PremiumUser): # checks if the user is PremiumUSer
                nr_premium_users += 1

                tracks_ids_unique = set()
                for session in self.sessions:
                    if session.user == user  and session.timestamp >= start:
                        tracks_ids_unique.add(session.track.track_id)

                total_unique_tracks += len(tracks_ids_unique)


        if nr_premium_users == 0:
            return 0.0

        return total_unique_tracks / nr_premium_users



    #   Q3: Track with Most Distinct Listeners
    #Method: track_with_most_distinct_listeners() -> Track | None
    def track_with_most_distinct_listeners(self):
        if len(self.sessions) == 0: # if it does not exist sessions then return None
            return None
        # for all track_id we keep a set of users which listened
        listeners = {} # set of users_ids |track_id|

        for session in self.sessions:
            track_id = session.track.track_id

            user_id = session.user.user_id

            if track_id not in listeners: # if track is not in dictionar we add a empty set
                listeners[track_id] = set()

            listeners[track_id].add(user_id) # add the user in track set

        best_track_id = None # find the track_id with the most different users
        max_listeners = 0

        for track_id, user_set in listeners.items():
            if len(user_set) > max_listeners:
                max_listeners = len(user_set)
                best_track_id = track_id

        return self.catalogue[best_track_id] # # return the track object, not just the id




    # Q4: Average Session Duration by User Type
    #Method: avg_session_duration_by_user_type() -> list[tuple[str, float]]
    def avg_session_duration_by_user_type(self):
        #for every type of user keep the sum and the number of sessions
        sum = {} #total seconds
        counter = {} #total number of sessions

        for session in self.sessions:
            user_type = type(session.user).__name__ #get the name of the user type(for example:FreeUser,PremiumUser)

            if user_type not in sum: # if the type is not in the dictionary yet,then it initialize it
                sum[user_type] = 0
                counter[user_type] = 0
            sum[user_type] += session.duration_listened_seconds
            counter[user_type] += 1

        result_are= []
        #calculate the average for each usertype
        for user_type in sum:
            average = sum[user_type] / counter[user_type]
            result_are.append((user_type, float(average)))

        # sort from highest to lowest average duration
        result_are.sort(key = lambda x: x[1], reverse = True) # sort the list result_are then with lambda search for every element x
        # and look for x[1] which means the average and then reverse=True is from high to low

        return result_are



    # Q5: Total Listening Time for Underage Sub-Users
    #Method: total_listening_time_underage_sub_users_minutes(age_threshold: int = 18) -> float
    def total_listening_time_underage_sub_users_minutes(self, age_threshold = 18 ):
        total = 0

        for session in self.sessions:
            if isinstance(session.user, FamilyMember) and session.user.age <age_threshold:
                total += session.duration_listened_seconds

        return total / 60.0



    # Q6: Top Artists by Listening Time
    #Method : top_artists_by_listening_time(n: int = 5) -> list[tuple[Artist, float]]
    def top_artists_by_listening_time(self, n = 5):
        #for every artist_id we keep the total listening time(seconds)
        artist_seconds = {} #total seconds

        for session in self.sessions:

            track = session.track

            if isinstance(track, Song): # check and only count Song tracks and not AudiobookTrack or Podcast
                artist_id = track.artist.artist_id

                if artist_id not in artist_seconds: # if artist is not in the dictionary yet,then it initialize it
                    artist_seconds[artist_id] = 0
                artist_seconds[artist_id] += session.duration_listened_seconds


        result_are = [] # create the result list with Artist object and minutes
        for artist_id in artist_seconds:
            artist = self.artists[artist_id]
            minutes = artist_seconds[artist_id] / 60.0
            result_are.append((artist, minutes))

        result_are.sort(key = lambda x: x[1], reverse = True)  #sorting from highest to lowest
        return result_are[:n]# we return only




    # Q7: User's Top Genre
    #Method: user_top_genre(user_id: str) -> tuple[str, float] | None
    def user_top_genre(self, user_id):
        # check if the user exists
        user = self.get_user(user_id)

        if user is None:
            return None

        # for each genre we keep the total listening time(seconds)
        genre_seconds = {}  #total seconds

        for session in self.sessions:
            # count only sessions for this user
            if session.user.user_id == user_id:
                genre = session.track.genre

                if genre not in genre_seconds: # if genre is not in dictionary create it
                    genre_seconds[genre] = 0
                genre_seconds[genre] += session.duration_listened_seconds

        if len(genre_seconds) == 0: # if the user has no sessions then it returns None
            return None

        t_genre = None # we find the genre with the most listening time
        max_seconds = 0

        for genre in genre_seconds:
            if genre_seconds[genre] > max_seconds:
                max_seconds = genre_seconds[genre]
                top_genre = genre

        total_seconds = 0
        for genre in genre_seconds:
            total_seconds += genre_seconds[genre]
        percentage = (max_seconds / total_seconds) * 100

        return (top_genre, float(percentage))



    # Q8 : Collaborative Playlists with Many Artists
    #Method: collaborative_playlists_with_many_artists(threshold: int = 3) -> list[CollaborativePlaylist]
    def collaborative_playlists_with_many_artists(self, threshold = 3):
        results = []

        for playlist in self.playlists.values():
            if isinstance(playlist, CollaborativePlaylist): # check only CollaborativePlaylist for instances
                distinct_artists = set() # collect distinct artists from Song tracks only

                for track in playlist.tracks:
                    if isinstance(track, Song):# counts only Song tracks (not Podcast or AudiobookTrack)
                        distinct_artists.add(track.artist.artist_id)

                if len(distinct_artists) > threshold: # if more than threshold distinct artists then add to results
                    results.append(playlist)
        return results



    # Q9 : Average Tracks per Playlist Type
    #Method: avg_tracks_per_playlist_type() -> dict[str, float]
    def avg_tracks_per_playlist_type(self):
        playlist_tracks = 0 # total track
        playlist_count = 0 # total counts

        collaborative_tracks = 0
        collaborative_count = 0

        for playlist in self.playlists.values():
            if isinstance(playlist, CollaborativePlaylist):

                collaborative_tracks += len(playlist.tracks) #this is a CollaborativePlaylist
                collaborative_count += 1
            else:
                playlist_tracks += len(playlist.tracks) #this is standard Playlist
                playlist_count += 1

        if playlist_count == 0:  # calculates the average then return 0.0 if no instances
            playlist_average = 0.0
        else:
            playlist_average = playlist_tracks / playlist_count

        if collaborative_count == 0:
            collaborative_average = 0.0
        else:
            collaborative_average = collaborative_tracks / collaborative_count

        return {
            "Playlist": float(playlist_average),
            "CollaborativePlaylist": float(collaborative_average)
        }




    #Q10 : Users Who Completed Albums
    #Method: users_who_completed_albums() -> list[tuple[User, list[str]]]
    def users_who_completed_albums(self):
        results = []


        for user in self.users.values(): # go through users in registration order

            # then we collect all track_ids of this user that listened
            listened_track_ids = set()
            for session in self.sessions:
                if session.user.user_id == user.user_id:
                    listened_track_ids.add(session.track.track_id)

            completed_albums = [] # checking each album
            for album in self.albums.values():
                if len(album.tracks) == 0: # ignore the albums with no tracks
                    continue

                all_tracks_listened = True # check if the user listened to every track in this album
                for track in album.tracks:
                    if track.track_id not in listened_track_ids:
                        all_tracks_listened = False
                        break

                if all_tracks_listened: # if user completed the album then add the title
                    completed_albums.append(album.title)

            if len(completed_albums) > 0: # if user completed at least one album then add to results
                results.append((user, completed_albums))

        return results