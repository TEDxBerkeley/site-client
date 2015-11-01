from client.libs.base import Entity


class Conference(Entity):
    """Conference object"""

    def fetch_staff(self):
        """Fetches list of all staff for given conference"""
        return self.call('get', func='fetch_staff')

    def fetch_speakers(self):
        """Fetches list of all speakers for given conference"""
        return self.call('get', func='fetch_speakers')


class Speaker(Entity):
    """Speaker object"""


class Engagement(Entity):
    """Connection between speaker and conference objects"""


class Nomination(Entity):
    """Nomination object"""


class Staff(Entity):
    """Staff object"""


class Membership(Entity):
    """Connection between staff and conference objects"""
