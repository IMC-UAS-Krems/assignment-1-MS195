"""
users.py
--------
Implement the class hierarchy for platform users.

Classes to implement:
  - User (base class)
    - FreeUser
    - PremiumUser
    - FamilyAccountUser
    - FamilyMember
"""

class User:
    def __init__(self,user_id, name, age ):
        self.user_id = user_id
        self.name = name
        self.age = age
        self.sessions = []

    def add_session(self,session):
        self.sessions.append(session)

    def total_listening_seconds(self): #add all the sessions
        total = 0
        for session in self.sessions:
            total += session.duration_listened_seconds # duration of LISTENED second, which means a finished sessions

        return total

    def total_listening_minutes(self):
        return self.total_listening_seconds() / 60.0

    def unique_tracks_listened(self):
        track_ids = set() #create a set() of track ids
        for session in self.sessions:
            track_ids.add(session.track.track_id)
        return track_ids

class FreeUser(User):
    MAX_SKIPS_PER_HOURS = 6

    def __init__(self,users_id, name, age):
        super().__init__(users_id, name, age)


class PremiumUser(User):
    def __init__(self, user_id, name, age, subscription_start):
        super().__init__(user_id, name, age)
        self.subscription_start = subscription_start


class FamilyAccountUser(User):
    def __init__(self, user_id, name, age):
        super().__init__(user_id, name, age)
        self.sub_users = []

    def add_sub_user(self, sub_user):
        self.sub_users.append(sub_user)

    def all_members(self):
        members = [self]
        for sub_user in self.sub_users:
            members.append(sub_user)
        return members

class FamilyMember(User):
    def __init__(self,user_id, name, age, parent):
        super().__init__(user_id, name, age)
        self.parent = parent