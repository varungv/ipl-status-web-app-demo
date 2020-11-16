# IPL Stats application
This is a IPL Stats application built using **Django, HTML and Vanilla JS.**

The application is hosted in **Heroku** at this url: https://gale-demo.herokuapp.com/ 

**Dockerfile** is available to containerize and ship the application.

**scripts/initial_data_loader.py** can be used to trigger an initial script which loads up the initial data from the CSV.

#### REST ENDPOINTS:
1. ##### /facts [GET]
    
    Used to get a list of facts 
    If we pass in the season parameter, we will get a response of facts speciffic to the season else generic facts will be returned
    
    `As a version 2 of this API, we would create a facts model and pull data from it directly. As it makes more sense to pre-analyze and save the data in batch jobs than to run long grouping queries on every users page load`
2. ##### /team_ranking [GET]
    
    Used to get the team rankings based in how many wins they have had.
    if season parameter is passed, ranking for that season will be provided.
3. ##### /chartsJS [GET]
    
    Used to return the settings JSON to display charts.
        input paramters: chart_name, chart_type
        
#### Step to add new chart to the page:
1. ##### html:

    Add div with id where the chart is required to be shown.

        <div id='chart-x'></div>
2. ##### JavaScript:

    Make below function call to make Ajax call
    
        make_ajax_get_call(charts_url, get_fill_chart_data('chart-x'), {chart_name: 'new-chart', chart_type: '<chart-type>'});
        
3. ##### Django View:

    Add the below code snippet in **ChartJSView.py** 
        
        elif chart_name == 'avg_runs_per_over_season':
            query_set = # Code to create query_set
            key_column = <key column name>
            value_columns = [<value colum names>]
            c_ds = ChartJSDataStructure(query_set, key_column, value_columns, chart_type, title=<chart-title>)
            

and Done...