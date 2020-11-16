from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from django.db.models import Sum, Count, Avg
from .models import Matches, Deliveries
from ColorGenerator import ColorGenerator


class ChartJSDataStructure:
    """
       This is a module which helps in creating the JSON required for the ChartJS to build graphs for different datasets
    """
    def __init__(self, query_set, key_column, value_columns, chart_type, title=None, mono_chrome=False):
        """
            Object Initialization
        :param query_set:
            This is where we have the data point to build the ChartJS available.
            This should can be any iterable which should follow the below structure
            [
            {'key_column': '<key>', '*value_columns':<value>, '*value_columns':<value>},
            {'key_column': '<key>', '*value_columns':<value>, '*value_columns':<value>}
            ]
        :param key_column:
            Name of the key column
        :param value_columns:
            Name of the value columns
        :param chart_type:
            chart type for ChartJS
        :param title:
            The Title of the chart
        :param mono_chrome:
            Boolean value to return all the values of a field to be monoChromatic or not
        """
        self.query_set = query_set
        self.key_column = key_column
        self.value_columns = value_columns
        self.chart_type = chart_type
        self.Title = title
        self.mono_chrome = mono_chrome or self.chart_type in ['line']

    def to_json(self):
        """
            Function which generates the ChartJS JSON structure
        :return:
        """
        datasets = []

        for col in self.value_columns:
            cs = ColorGenerator()
            col_gen = cs.get_colors()
            colors = [col_gen.__next__() for _ in self.query_set] if not self.mono_chrome else [col_gen.__next__()]*len(self.query_set)
            data = {
                'data': [row[col] for row in self.query_set],
                'backgroundColor': colors,
                'borderColor': cs.get_solid_selected_colors(),
                'borderWidth': 1
            }
            datasets.append(data)

        return {
        'type': self.chart_type,
        'data': {
            'labels': [row[self.key_column] for row in self.query_set],
            'datasets': datasets
        },
        'options': {
            'title': {
                'display': bool(self.Title),
                'text': self.Title
            },
            'legend': {
                'display': False if self.chart_type in ['radar', 'bar', 'line'] else True,
                'position': 'right'
            },
            'scales': {
                'yAxes': [{
                    'ticks': {
                        'beginAtZero': True
                    }
                }]
            }
        }
    }


class ChartJSView(APIView):
    """
        View to query the data required for creating a chartJS graph and converting it to the required format.
    """

    def get(self, request):
        """
            Views Get method call
        :param request:
        :return:
        """
        chart_name = request.query_params.get('chart_name', None)
        chart_type = request.query_params.get('chart_type', None)
        season = request.query_params.get('season', None)
        key_column = None
        value_columns = None
        query_set = None

        # Making sure we have all the necessary parameters to create ChartJS Json
        if chart_name and chart_type and chart_type in ['bar', 'pie', 'line', 'radar', 'doughnut']:

            # New Query Sets would be added here to accomodate new graphs
            if chart_name == 'top_worst_bowlers' and season:
                # To create chart for Worst 6 bowlers of the season
                season_match_ids = Matches.objects.filter(season=season).values('match_id')
                query_set = Deliveries.objects.filter(match_id__in=season_match_ids).values('bowler').annotate(runs_sum=Sum('total_runs')).order_by('-runs_sum')[:6]
                key_column = 'bowler'
                value_columns = ['runs_sum']
                c_ds = ChartJSDataStructure(query_set, key_column, value_columns, chart_type, title=f'Top 6 Worst Bowlers of {season}')

            elif chart_name == 'team_wise_win_count' and season:
                # To create chart for number of wins by each team for season
                query_set = Matches.objects.filter(season=season).values('winner').annotate(count=Count('winner'))
                key_column = 'winner'
                value_columns = ['count']
                c_ds = ChartJSDataStructure(query_set, key_column, value_columns, chart_type, title=f'Team wise win count of {season}')

            elif chart_name == 'overall_team_wise_win_count':
                # To create chart for number of wins by each team overall
                query_set = Matches.objects.values('winner').annotate(count=Count('winner'))
                key_column = 'winner'
                value_columns = ['count']
                c_ds = ChartJSDataStructure(query_set, key_column, value_columns, chart_type, title='Overall Team wise win count')

            elif chart_name == 'over_wise_avg_run_scored':
                # To create chart for average runs scored at every over
                query_set = Deliveries.objects.values('over').annotate(runs_avg=Avg('total_runs'), run_sum=Sum('total_runs'))
                key_column = 'over'
                value_columns = ['runs_avg']
                c_ds = ChartJSDataStructure(query_set, key_column, value_columns, chart_type, title='Average runs per over')

            elif chart_name == 'avg_runs_per_over_season':
                # To create chart for average runs scored at every over
                match_ids = [row['match_id'] for row in Matches.objects.filter(season=season).values('match_id')]
                query_set = Deliveries.objects.filter(match_id__in=match_ids).values('over').annotate(runs_avg=Avg('total_runs'), run_sum=Sum('total_runs'))
                key_column = 'over'
                value_columns = ['runs_avg']
                c_ds = ChartJSDataStructure(query_set, key_column, value_columns, chart_type, title=f'Average runs per over in season {season}')

            if key_column and value_columns and query_set:
                return Response(c_ds.to_json())
            else:
                return Response(status=HTTP_404_NOT_FOUND)
        else:
            return Response(status=HTTP_404_NOT_FOUND)
