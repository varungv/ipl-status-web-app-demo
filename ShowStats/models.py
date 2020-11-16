from django.db import models


class Matches(models.Model):
    """
        Model to store details of individual matches
    """
    match_id = models.IntegerField(primary_key=True)
    season = models.IntegerField()
    city = models.CharField(max_length=255)
    date = models.DateField()
    team1 = models.CharField(max_length=255)
    team2 = models.CharField(max_length=255)
    toss_winner = models.CharField(max_length=255)
    toss_decision = models.CharField(max_length=255)
    result = models.CharField(max_length=255)
    dl_applied = models.BooleanField(default=False)
    winner = models.CharField(max_length=255)
    win_by_runs = models.IntegerField()
    win_by_wickets = models.IntegerField()

    # Below keys can be converted into foreign key if we were to implement players, umpires and venue tables
    player_of_match = models.CharField(max_length=255)
    venue = models.CharField(max_length=255)
    umpire1 = models.CharField(max_length=255)
    umpire2 = models.CharField(max_length=255)
    umpire3 = models.CharField(max_length=255)

    def __str__(self):
        return f"winner {self.winner}"

    @classmethod
    def get_list_of_seasons(cls):
        return cls.objects.values('season').distinct().order_by('season')


class Deliveries(models.Model):
    """
        Model to store every delivery made in the match
    """
    delivery_id = models.IntegerField(primary_key=True)
    match_id = models.ForeignKey(Matches, on_delete=models.CASCADE)
    inning = models.IntegerField()
    batting_team = models.CharField(max_length=255)
    bowling_team = models.CharField(max_length=255)
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=255)
    non_striker = models.CharField(max_length=255)
    bowler = models.CharField(max_length=255)
    is_super_over = models.BooleanField()
    wide_runs = models.IntegerField()
    bye_runs = models.IntegerField()
    legbye_runs = models.IntegerField()
    noball_runs = models.IntegerField()
    penalty_runs = models.IntegerField()
    batsman_runs = models.IntegerField()
    extra_runs = models.IntegerField()
    total_runs = models.IntegerField()
    player_dismissed = models.CharField(max_length=255)
    dismissal_kind = models.CharField(max_length=255)
    fielder = models.CharField(max_length=255)

