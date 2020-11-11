import pandas as pd
from ShowStats import models

match_data = pd.read_csv('../ipl/matches.csv', parse_dates=['date'])
deliveries_data = pd.read_csv('../ipl/deliveries.csv')


def replace_with_mapping(x, mapping):
    return dict(mapping)[x]


match_instances = [models.Matches(**r) for r in match_data.to_dict(orient='records')]
match_id_mapping = dict(zip(match_data['match_id'], match_instances))

models.Matches.objects.bulk_create(
    match_instances
)
deliveries_data['match_id'] = deliveries_data['match_id'].apply(lambda x: replace_with_mapping(x, match_id_mapping))
deliveries_data = deliveries_data.to_dict(orient='records')
models.Deliveries.objects.bulk_create(
    [models.Deliveries(**r) for r in deliveries_data]
)

