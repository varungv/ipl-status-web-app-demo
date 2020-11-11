from django.shortcuts import render
from django.views.generic import View
from django.db.models import Count, Max, Sum, F
from .models import Matches, Deliveries


class HomePage(View):
    """
        Class Based view for loading the homepage
    """

    def get(self, request):
        seasons = self.get_list_of_seasons()
        return render(request, 'ShowStats/HomePage.html', {'seasons': seasons})

    def post(self, request):
        season = request.POST['season']

        # Top 4 teams in terms of wins
        # No need to worry about index slicing as the data will surely be available for this query
        top_4_winners = Matches.objects.values('winner').annotate(count=Count('winner')).order_by('-count')[:4]

        # Which team won the most number of tosses in the season
        top_toss_winners = Matches.objects.filter(season=season).values('toss_winner').annotate(count=Count('toss_winner')).order_by('-count')[0]

        # Which player won the maximum number of Player of the Match awards in the whole season
        max_man_of_the_match = Matches.objects.filter(season=season).values('player_of_match').annotate(count=Count('player_of_match')).order_by('-count')[0]

        # Which team won max matches in the whole season
        max_winning_team = Matches.objects.filter(season=season).values('winner').annotate(count=Count('winner')).order_by('-count')[0]

        # Which location has the most number of wins for the top team
        top_team_name = top_4_winners[0]['winner']
        location_most_wins_for_top_team = Matches.objects.filter(winner=top_team_name).values('venue').annotate(count=Count('venue')).order_by('-count')[0]

        # Which % of teams decided to bat when they won the toss
        total_count = Matches.objects.count()
        batting_chosen_count = Matches.objects.filter(toss_decision='bat').count()
        batting_chosen_perc = batting_chosen_count * 100 / total_count

        # Which location hosted most number of matches
        max_matches_location = Matches.objects.values('venue').annotate(count=Count('venue')).order_by('-count')[0]

        # Which team won by the highest margin of runs  for the season
        max_run_win = Matches.objects.filter(season=season).aggregate(Max('win_by_runs'))['win_by_runs__max']
        won_by_highest_run_margin = Matches.objects.filter(season=season, win_by_runs=max_run_win)[0]

        # Which team won by the highest number of wickets for the season
        max_wickets_win = Matches.objects.filter(season=season).aggregate(Max('win_by_wickets'))['win_by_wickets__max']
        won_by_highest_wicket_margin = Matches.objects.filter(season=season, win_by_wickets=max_wickets_win)[0]

        # How many times has a team won the toss and the match
        count_of_won_toss_match = Matches.objects.filter(toss_winner__exact=F('winner')).count()

        # Season matches
        season_match_ids = Matches.objects.filter(season=season).values('match_id')

        # Which Bowler gave away the most number of runs in a match for the selected season
        worst_economy_bowler = Deliveries.objects.filter(match_id__in=season_match_ids).values('bowler').annotate(runs_sum=Sum('total_runs')).order_by('-runs_sum')[:5]

        return render(request, 'ShowStats/HomePage.html', {
            'selected_season': int(season),
            'seasons': self.get_list_of_seasons(),
            'top_4_winners': top_4_winners,
            'top_toss_winners': top_toss_winners,
            'max_man_of_the_match': max_man_of_the_match,
            'max_winning_team': max_winning_team,
            'location_most_wins_for_top_team': location_most_wins_for_top_team,
            'top_team_name': top_team_name,
            'batting_chosen_perc': int(batting_chosen_perc),
            'max_matches_location': max_matches_location,
            'won_by_highest_run_margin': won_by_highest_run_margin,
            'won_by_highest_wicket_margin': won_by_highest_wicket_margin,
            'count_of_won_toss_match': count_of_won_toss_match,
            'worst_economy_bowler': worst_economy_bowler
        })

    @staticmethod
    def get_list_of_seasons():
        return Matches.objects.values('season').distinct().order_by('season')
