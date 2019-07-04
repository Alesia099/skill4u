from django.db import models
from registration.models import User
from django.utils.translation import ugettext_lazy as _


class Task(models.Model):
    """"Olympiad task"""
    task = models.TextField(blank=False)
    creater = models.ForeignKey(User, verbose_name=_("creater"), on_delete=models.CASCADE)
    input_data = models.CharField(_("input data"), blank=False, max_length=250)
    answer = models.CharField(_("answer"), blank=False, max_length=250)

    objects = models.Manager()


class Team(models.Model):
    """Teams for Olympiad"""
    capitan = models.ForeignKey(User, _("capitan"),)
    invited = models.ManyToManyField(User, _("invated"),)
    max_participations = models.IntegerField(_("max participations"), blank=False)

    def __str__(self):
        return '%s %s' % (self.capitan, self.invited)


class Olympiad(models.Model):
    name = models.CharField(_(""), max_length=50)
    creater = models.ForeignKey(User, on_delete=models.CASCADE)
    task = models.ManyToManyField(Task)
    duration = models.IntegerField(_(""))  # in minutes
    start_olympiad = models.DateTimeField(_("date of the start olympiad"),
                                          auto_now=False,
                                          auto_now_add=False
                                          )
    end_olympiad = models.DateTimeField(_("date of the end olympiad"),
                                        auto_now=False,
                                        auto_now_add=False
                                        )
    participation_count = models.IntegerField(_("participation count"))
    team = models.ManyToManyField(Team, verbose_name=_("team"),)
    max_teams = models.IntegerField(_("max teams"))

    def __str__(self):
        return self.name