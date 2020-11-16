from django.shortcuts import render
from django.views.generic import View
from django.db.models import Count, Max, Sum, F
from .models import Matches, Deliveries
from rest_framework.response import Response
from rest_framework.decorators import api_view


class HomePage(View):
    """
        View for loading the homepage
    """

    def get(self, request):
        seasons = Matches.get_list_of_seasons()
        return render(request, 'ShowStats/HomePage.html', {'seasons': seasons})


@api_view(['GET'])
def get_facts(request):
    """
        View to get a response of with either generic or season wise facts
    :param request:
    :return:
    """

    season = request.query_params.get('season', None)
    if season:
        # Get fact of that particular season
        # Which team won the most number of tosses in the season
        top_toss_winners = Matches.objects.filter(season=season).values('toss_winner').annotate(count=Count('toss_winner')).order_by('-count')[0]

        # Which player won the maximum number of Player of the Match awards in the whole season
        max_man_of_the_match = Matches.objects.filter(season=season).values('player_of_match').annotate(count=Count('player_of_match')).order_by('-count')[0]

        # Which team won max matches in the whole season
        max_winning_team = Matches.objects.filter(season=season).values('winner').annotate(count=Count('winner')).order_by('-count')[0]

        # Which team won by the highest margin of runs  for the season
        max_run_win = Matches.objects.filter(season=season).aggregate(Max('win_by_runs'))['win_by_runs__max']
        won_by_highest_run_margin = Matches.objects.filter(season=season, win_by_runs=max_run_win)[0]

        # Which team won by the highest number of wickets for the season
        max_wickets_win = Matches.objects.filter(season=season).aggregate(Max('win_by_wickets'))['win_by_wickets__max']
        won_by_highest_wicket_margin = Matches.objects.filter(season=season, win_by_wickets=max_wickets_win)[0]

        facts = [
            f"<b>{top_toss_winners['toss_winner']}</b> have won the highest number of tosses in the entire season. A total of {top_toss_winners['count']} times",
            f"<b>{max_man_of_the_match['player_of_match']}</b> was awarded a highest number of player of the match award ({max_man_of_the_match['count']} times)",
            f"Maximum number of matches was won by <b>{max_winning_team['winner']}</b>",
            f"<b>{won_by_highest_run_margin.winner}</b> had won by the highest run margin of {won_by_highest_run_margin.win_by_runs} runs. <b>{won_by_highest_run_margin.player_of_match}</b> was awarded the player of the match.",
            f"<b>{won_by_highest_wicket_margin.winner}</b> had won by the highest wicket margin of {won_by_highest_wicket_margin.win_by_runs} wickets. <b>{won_by_highest_wicket_margin.player_of_match}</b> was awarded the player of the match.",
        ]

        response = {
            'heading': f'IPL Facts for {season} Season',
            'list': facts
        }
    else:
        # Get Generic Facts

        # Top 4 teams in terms of wins
        # No need to worry about index slicing as the data will surely be available for this query
        top_4_winners = Matches.objects.values('winner').annotate(count=Count('winner')).order_by('-count')[:4]

        # Which location has the most number of wins for the top team
        top_team_name = top_4_winners[0]['winner']

        location_most_wins_for_top_team = Matches.objects.filter(winner=top_team_name).values('venue').annotate(count=Count('venue')).order_by('-count')[0]

        # Which % of teams decided to bat when they won the toss
        batting_chosen_perc = Matches.objects.filter(toss_decision='bat').count() * 100 / Matches.objects.count()

        # Which location hosted most number of matches
        max_matches_location = Matches.objects.values('venue').annotate(count=Count('venue')).order_by('-count')[0]

        # How many times has a team won the toss and the match
        count_of_won_toss_match = Matches.objects.filter(toss_winner__exact=F('winner')).count()

        facts = [
            f"<b>{top_team_name}</b> have had their maximum wins in <b>{location_most_wins_for_top_team['venue']}</b>.",
            f"<b>{int(batting_chosen_perc)}%</b> of the time teams choose batting when they won the toss.",
            f"<b>{max_matches_location['count']}</b> matches is played in {max_matches_location['venue']}</b> which makes it the venue where highest number of matches are played in IPL history.",
            f"<b>{count_of_won_toss_match} instances where teams who have won the toss have also won the match.</b>"
        ]

        response = {
            'heading': 'IPL Generic Facts',
            'list': facts
        }

    return Response(response)


@api_view(['GET'])
def team_ranking(request):
    # team_ranking in terms of wins
    season = request.query_params.get('season', None)
    if not season:
        # No need to worry about index slicing as the data will surely be available for this query
        ranked_teams = Matches.objects.values('winner').annotate(count=Count('winner')).order_by('-count')
        return Response({
            'heading': 'Overall Teams Ranks based on # of wins',
            'list': [row['winner'] for row in ranked_teams]
        })
    else:
        ranked_teams = Matches.objects.filter(season=season).values('winner').annotate(count=Count('winner')).order_by('-count')
        return Response({
            'heading': f'{season} Season Teams rankings based on # of wins',
            'list': [row['winner'] for row in ranked_teams]
        })
