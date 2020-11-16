from django.urls import path

from .views import HomePage, get_facts, team_ranking
from .ChartJSViews import ChartJSView


app_name = 'ShowStats'
urlpatterns = [
    path('', HomePage.as_view(), name='HomePage'),

    # Rest APIs

    path('facts', get_facts, name='factsAPI'),
    path('team_ranking', team_ranking, name='team_ranking'),
    path('chartsJS', ChartJSView.as_view(), name='chartsJSView')
]