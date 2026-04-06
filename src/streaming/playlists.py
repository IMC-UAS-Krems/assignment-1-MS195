"""
playlists.py
------------
Implement playlist classes for organizing tracks.

Classes to implement:
  - Playlist
    - CollaborativePlaylist
"""
class Playlist:
    def __init__(self, playlist_id, name, owner):
        self.playlist_id = playlist_id
        self.name = name
        self.owner = owner
        self.tracks = []

    def add_track(self, track):
        if track not in self.tracks: # only add the track if it is not already in the list
            self.tracks.append(track)

    def remove_track(self, track_id):
        for track in self.tracks:
            if track.track_id == track_id: # if the track id matches the one we  want to remove
                self.tracks.remove(track)  # remove the track from the list
                break                      # the loop is stopped, we found it and remove the track

    def total_duration_seconds(self):
        total = 0
        for track in self.tracks:
            total += track.duration_seconds
        return total


class CollaborativePlaylist(Playlist):
    def __init__(self, playlist_id, name, owner):
        super().__init__ (playlist_id, name, owner)
        self.contributors= [owner]  # must start with owner, not []

    def add_contributor(self, user):
        if user not in self.contributors: # this is for no duplicate check
            self.contributors.append(user)

    def remove_contributor(self, user):
        if user is not self.owner: # we never remove the
            self.contributors.remove(user)
