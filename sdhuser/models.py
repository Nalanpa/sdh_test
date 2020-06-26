"""
Models for SDHUSER app
"""

from django.db import models
from django.contrib.auth.models import AbstractUser


class SDHuser(AbstractUser):
    """
    SDH user
    """
    email_confirmed = models.BooleanField(default=False)
    invitation_code = models.CharField(max_length=10, blank=True)
    invited = models.ForeignKey(
        'self', blank=True, null=True, on_delete=models.PROTECT)
    points = models.PositiveIntegerField(default=0)

    @classmethod
    def not_invited_users_count(cls):
        """
        Users who was not invited (registered without invitation code)
        """
        return cls.objects.filter(invited__isnull=True).count()

    def fond(self):
        """
        Calculate prize fond
        """
        return SDHuser.objects.filter(invited=self).count() + 1

    def accrue_points(self, points):
        """
        Accrue points per new registered user
        """
        if points > 0:
            if not self.invited:
                self.points += points
            else:
                self.points += 1
                # pylint: disable=E1101
                self.invited.accrue_points(points-1)
            self.save()
