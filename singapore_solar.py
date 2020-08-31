"""
Singapore_Solar

A brief exploration of solar deployment in Singapore, which I used to explore 
the current status of PV and create some interesting geographic and web-based 
visualisations.

Copyright 2020 Philip Sandwell (philip.sandwell@gmail.com)
MIT License
"""

# =============================================================================
# Import dependencies
# =============================================================================

import pandas as pd
import geopandas as gpd
import numpy as np
import plotly.express as px
import plotly.io as pio
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
import hvplot.pandas

# =============================================================================
# Read files and import data
# =============================================================================

geo_info = gpd.read_file("zip://master-plan-2014-planning-area-boundary-web-shp.zip")
system_info = pd.read_excel("system_database.xlsx")
location_correct = pd.read_excel("location_correct.xlsx")

# =============================================================================
# Specify types of data allowable in the analysis
# =============================================================================

location_correct = location_correct.set_index('Listed')
name_correct = pd.read_excel("name_correct.xlsx")
name_correct = name_correct.set_index('System name')
disallowed_systems = list(['SolarNova2','SolarNova3',
                           'HDB Phase 1 Solar Leasing',
                           'HDB Phase 2 Solar Leasing',
                           'HDB Phase 3 Solar Leasing'])
technology_types = list(['Amorphous silicon', 'CIGS','Monocrystalline HIT',
                         'Monocrystalline all-back contact',
                         'Monocrystalline silicon',
                         'Polycrystalline silicon',
                         'multi-crystalline'])
# =============================================================================
# Process geo data
# =============================================================================

geometry = geo_info[['PLN_AREA_N','geometry','SHAPE_Area']].set_index('PLN_AREA_N')
districts = list(geo_info['PLN_AREA_N'])
regions = geo_info[['REGION_N','PLN_AREA_N']]
regions = regions.set_index('PLN_AREA_N')
geo_info = geo_info.drop(['geometry'],axis=1)
geo_info = pd.DataFrame(geo_info)

# =============================================================================
# Process system database
# =============================================================================

system_info['Commissioned'] = pd.to_datetime(system_info['Commissioned'],format='%b %y')
system_info['Location'] = system_info['Location'].replace({np.nan:'NOT SPECIFIED'})
system_info['Location'] = [system_info['Location'].iloc[i].upper() for i in range(len(system_info))]
system_info['Tilt'] = pd.DataFrame(system_info['Tilt'].replace('\u00b0','', regex=True)).astype(float)

start_date = system_info['Commissioned'].min()
end_date = system_info['Commissioned'].max()
date_list = pd.date_range(start=start_date,end=end_date,freq='MS')

system_info['PLN_AREA_N'] = [system_info['Location'].iloc[i] if system_info['Location'].iloc[i] in districts else
            'NOT SPECIFIED' for i in range(len(system_info))]
system_info['Region'] = 'NOT SPECIFIED'

for i in range(len(system_info)):
    if system_info.iloc[i]['PLN_AREA_N'] == 'NOT SPECIFIED':
        location = system_info.iloc[i]['Location']
        system_info.loc[i,'PLN_AREA_N'] = location_correct.loc[location,'Actual']
        
    if system_info.iloc[i]['PLN_AREA_N'] == 'NOT SPECIFIED':
        name = system_info.iloc[i]['System name']
        system_info.loc[i,'PLN_AREA_N'] = name_correct.loc[name,'Actual']   
        
    if system_info.loc[i,'System name'] in disallowed_systems:
        system_info.loc[i,'PLN_AREA_N'] = 'NOT SPECIFIED'    
    if system_info.loc[i,'Technology'] not in technology_types:
        system_info.loc[i,'Technology'] = 'Other'
        
    planning_area = system_info.iloc[i]['PLN_AREA_N']
    if planning_area != 'NOT SPECIFIED':
        system_info.loc[i,'Region'] = regions.loc[planning_area,'REGION_N']
        
system_info['Year'] = system_info['Commissioned'].dt.year
system_info['System size'] = system_info['System size'].round()

system_info = system_info.sort_values(by='Commissioned').reset_index(drop=True)
system_info['Cumulative'] = system_info.groupby(by = ['Region','PLN_AREA_N'])['System size'].cumsum().round()
system_info['Country'] = 'Singapore'

# =============================================================================
# Sort information about planning areas
# =============================================================================

planning_area_systems = pd.DataFrame(system_info.groupby(
        ['PLN_AREA_N'],as_index=True)['System size'].sum())

planning_area_systems.rename({'System size':'Cumulative capacity'},axis='columns',inplace=True)
planning_area_systems['Mean system size'] = pd.DataFrame(system_info.groupby(
        ['PLN_AREA_N'],as_index=True)['System size'].mean())
planning_area_systems['Number of systems'] = pd.DataFrame(system_info.groupby(
        ['PLN_AREA_N'],as_index=True)['System size'].count())

geometry = geometry.join(planning_area_systems)

# =============================================================================
# Make a cumulative tally of installations over time
# =============================================================================

def make_cumulative_by_district():
    districts.append('NOT SPECIFIED')
    base_df = pd.DataFrame({'System size':np.nan},
                           index = 
                           pd.MultiIndex.from_product(
                                   [date_list,districts]))
    annual_cumulative = pd.DataFrame(system_info.groupby(by = 
                                           ['Commissioned','PLN_AREA_N']
                                           )['System size'].sum())
    base_df.loc[:, 'System size'] = annual_cumulative['System size']
    base_df = base_df.fillna(0)
    base_df = base_df.reset_index()
    base_df = base_df.rename({'level_0':'Commissioned','level_1':'PLN_AREA_N'}, axis=1)
    base_df['Cumulative'] = base_df.groupby(by = ['PLN_AREA_N'])['System size'].cumsum()
    base_df['Region'] = 'NOT SPECIFIED'
    for i in range(len(base_df)):
        planning_area = base_df.iloc[i]['PLN_AREA_N']
        if planning_area != 'NOT SPECIFIED':
            base_df.loc[i,'Region'] = regions.loc[planning_area,'REGION_N']
    return base_df

def make_cumulative_by_technology():
    base_df = pd.DataFrame({'System size':np.nan},
                           index = 
                           pd.MultiIndex.from_product(
                                   [date_list,technology_types]))
    annual_cumulative = pd.DataFrame(system_info.groupby(by = 
                                           ['Commissioned','Technology']
                                           )['System size'].sum())
    base_df.loc[:, 'System size'] = annual_cumulative['System size']
    base_df = base_df.fillna(0)
    base_df = base_df.reset_index()
    base_df = base_df.rename({'level_0':'Commissioned','level_1':'Technology'}, axis=1)
    base_df['Cumulative'] = base_df.groupby(by = ['Technology'])['System size'].cumsum()
    return base_df

# =============================================================================
# Figures included in the analysis
# =============================================================================

def system_size_scatter():
    data = system_info[~system_info['System name'].isin(disallowed_systems)]
    fig = px.scatter(data, x="Commissioned", y="System size",
                     size='System size',
                     color="System type", marginal_y="box",
                     title='System deployment 2008-2020',
                     labels={
                             "Commissioned": "Date commissioned",
                             "System size":"System capacity (kWp)"},
                    hover_name="System name", 
                    hover_data=["System size", "PLN_AREA_N",
                                "Region","Technology"]
                     )
    fig.show()
    pio.write_html(fig, file='test_system_size_scatter.html', auto_open=True)
  
def plot_treemap():
    data = system_info[system_info['PLN_AREA_N']!='NOT SPECIFIED']
    fig = px.treemap(data, path=['Country','Region', 'PLN_AREA_N','System type'
                                        ], values='System size',
                      color='Region',
                      color_continuous_scale='Reds',
                      hover_data=["PLN_AREA_N"],
                      title='Cumulative installed capacity (kWp) by planning area')
    fig.show()
    pio.write_html(fig, file='treemap.html', auto_open=True)
  
def plot_cumulative_map():
    plot_map = geometry.hvplot(c='Cumulative capacity',aspect='equal',cmap='Reds',
                               title='Cumulative installed capacity (kWp) by planning area',
                               hover_cols=['PLN_AREA_N',
                                           'Mean system size',
                                           'Cumulative capacity',
                                           'Number of systems'],
                               logz=True,xaxis=None, yaxis=None)
    hvplot.save(plot_map, 'cumulative_map.html')    
    
def plot_sunburst():
    fig = px.sunburst(system_info, path=['Country','Technology', 'System integrator',
                                         ], values='System size',
                      branchvalues='total',
                      labels=system_info['System size'],
                      color='Technology',
                      color_continuous_scale='Reds',
                      title='Cumulative installed capacity (kWp) by technology type')
    fig.update_layout(hovermode="x")
    fig.show()
    pio.write_html(fig, file='test_sunburst.html', auto_open=True)


def plot_mean_map():
    plot_map = geometry.hvplot(c='Mean system size',cmap='Greens',aspect='equal',
                               title='Mean system size (kWp) by planning area',
                               hover_cols=['PLN_AREA_N','Mean system size',
                                           'Cumulative capacity',
                                           'Number of systems'],
                               logz=True,xaxis=None, yaxis=None)
    hvplot.save(plot_map, 'mean_map.html')

def plot_capacity_line():
    data = make_cumulative_by_district()
    fig = px.area(data, x="Commissioned", y="Cumulative", color="Region",
                 title='Cumulative installed capacity (kWp) over time',
                 line_group="PLN_AREA_N",
                 labels={"Commissioned": "Date",
                             "Cumulative":"Cumulative installed capacity (kWp)"},)
    fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
            buttons=list([
                dict(count=5, label="5y", step="year", stepmode="backward"),
                dict(count=2, label="2y", step="year", stepmode="backward"),
                dict(count=1, label="1y", step="year", stepmode="backward"),
                dict(count=1, label="YTD", step="year", stepmode="todate"),
                dict(step="all")
            ])
        )
    )
    fig.show()
    pio.write_html(fig, file='cumulative_installations.html', auto_open=True)

# =============================================================================
# Figures not included in the analysis
# =============================================================================
    
def plot_count_map():
    plot_map = geometry.hvplot(c='Number of systems',cmap='Blues',aspect='equal',
                               title='Number of systems by planning area',
                               hover_cols=['PLN_AREA_N','Mean system size',
                                           'Cumulative capacity',
                                           'Number of systems'],
                               logz=False,xaxis=None, yaxis=None)
    hvplot.save(plot_map, 'count_map.html')    


def plot_bar():
    data = make_cumulative_by_technology()
    fig = px.bar(data, x="Technology", y="Cumulative", color="Technology",
                 animation_frame= data['Commissioned'].astype(str),
                 range_y = [0,100000])
    fig.show()
    pio.write_html(fig, file='bar_animated.html', auto_open=True)


def plot_box():
    fig = px.box(system_info, x="Region", y="System size")
    pio.write_html(fig, file='boxplot.html', auto_open=True)
    fig.show()

def plot_tilt():
    fig = px.bar_polar(system_info, r="System size", theta="Tilt",
                       range_theta=[0,90], start_angle=0, direction="counterclockwise")
    fig.show()
    pio.write_html(fig, file='tilt.html', auto_open=True)
    
def plot_log_map():
    fig = plt.gcf()
    ax = fig.add_subplot(111)
    ax.set_aspect('equal')
    ax.set_axis_off()

    divider = make_axes_locatable(ax)
    cax = divider.append_axes("right", size="5%", pad=0.1)
    geometry.plot(ax=ax, column='Log system size',legend=True,cmap=plt.get_cmap("Reds"),
                  edgecolor='k',cax=cax,
                  legend_kwds={'label': "Cumulative installed capacity\n(kWp, log scale)",
                               'orientation': "vertical",
                               'boundaries':[0,1,2,3,4,5],
                               'ticks':[0,1,2,3,4,5]})
    plt.savefig('map_log.png',dpi=150)