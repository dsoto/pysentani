import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_survey():
    return pd.read_excel('../../../data-clean/sentani-merged-cleaned-2015-06-10.xlsx',
                         na_values=[''])
def find_survey(dirt):
    paths = []
    for (dir, _, files) in os.walk(dirt):
        for f in files:
            path = os.path.join(dir, f)       
            if ".xlsx" in path:
                paths.append(path)
    timestamps = []
    for i in paths:
        captured = re.search("([0-9]{4}\-[0-9]{2}\-[0-9]{2})", i)
        timestamps.append(captured)
    xx = 0 
    ind = 0
    rec_tstamp = datetime.strptime(timestamps[0].group(1), '%Y-%m-%d')
    for i in timestamps:
        temp = datetime.strptime(i.group(1), '%Y-%m-%d')
        if rec_tstamp < temp:
            rec_tstamp = datetime.strptime(i.group(1), '%Y-%m-%d')
            ind = xx;
        xx+=1
    print (paths[ind])
    return pd.read_excel((paths[ind]), na_values=[''])

def strip_chart(column):
    #plt.plot(survey[column], np.ones(len(survey)), 'ko')
    #plt.semilogx(survey[column], np.zeros(len(survey)), 'ko')
    plt.semilogx(column, np.random.random(len(column)), 'ko')
    #plt.title(column)
    plt.show()

# def show_outliers(column, low_threshold, high_threshold):
#     mask = (survey[column]>=high_threshold) | (survey[column]<=low_threshold)
#     return survey[mask][['village_name',
#                          'demand_point',
#                          'demand_point_other',
#                          '_uuid',
#                          column]]

# def strip_chart(column):
#     #plt.plot(survey[column], np.ones(len(survey)), 'ko')
#     plt.semilogx(survey[column], np.random.random(len(survey)), 'ko')
#     plt.title(column)
#     plt.ylim((-2,2))
#     plt.show()

def strip_chart_log(column):
    pass

# def strip_chart_outliers_removed(column, threshold):
#     winnowed = survey[survey[column]<threshold][column]
#     plt.semilogx(winnowed, np.zeros(len(winnowed)), 'ko')
#     plt.show()
#     # todo make more like a strip and shrink vertical direction

def similar_columns(survey, searchstring):
    for c in survey.columns:
        if searchstring in c:
            print(c)

def contingency_table(survey, column1, column2):
        print(pd.crosstab(survey[column1], survey[column2]))

def contingency_table_normed(survey, column1, column2):
        print(pd.crosstab(survey[column1],
                          survey[column2]).apply(lambda r: r/r.sum(), axis=1))

def response_rate(survey, column):
    survey['power_supply/PLN_grid'].value_counts(dropna=False)

access_map = {'Abar': 'no_access',
              'Ajau': 'PLN_grid',
              'Asei': 'PLN_grid',
              'Atamali': 'community_microgrid',
              'Ayapo': 'PLN_microgrid',
              'Babrongko': 'PLN_grid',
              'Burawai': 'PLN_grid',
              'Donday': 'PLN_microgrid',
              'Ebunfauw': 'no_access',
              'Evale': 'PLN_grid',
              'Flafow': 'PLN_grid',
              'Hobong': 'PLN_grid',
              'Kalio': 'no_access',
              'Kampung_Baru': 'no_access',
              'Kensio': 'community_microgrid',
              'Khageuw': 'no_access',
              'Khamayakha': 'PLN_grid',
              'Kheleubulow': 'PLN_grid',
              'Kwadeware': 'PLN_grid',
              'Obolyo': 'no_access',
              'Pantai_Yahim': 'PLN_grid',
              'Puai': 'no_access',
              'Simporo': 'PLN_grid',
              'Sosiri': 'PLN_grid',
              'Yakonde': 'PLN_grid',
              'Yobeh': 'PLN_grid',
              'Yoboi': 'no_access',
              'Yoka': 'PLN_grid',
              'Yokiwa': 'no_access'}

def access_type(survey):
    return survey['village_name'].apply(lambda x: access_map.get(x))

def income_monthly(survey):
    multiplier = {'monthly':1,
                  'weekly':4,
                  'daily':30,
                  'not_regular':np.nan}
    return survey['group_income_reg/electric_income'] * survey[
                  'group_income_reg/electric_income_freq'].apply(
                          lambda x: multiplier.get(x))

village_map = {'Abar' : 'Abar',
               'Ajau' : 'Ajau-Evale-Hobong',
               'Asei' : 'Asei',
               'Atamali' : 'Atamali',
               'Ayapo' : 'Ayapo',
               'Babrongko' : 'Babrongko',
               'Burawai' : 'Burawai',
               'Donday' : 'Donday',
               'Ebunfauw' : 'Ebunfauw',
               'Evale' : 'Ajau-Evale-Hobong',
               'Flafow' : 'Flafow',
               'Hobong' : 'Ajau-Evale-Hobong',
               'Kalio' : 'Kalio',
               'Kampung_Baru' : 'Kampung_Baru',
               'Kensio' : 'Kensio',
               'Khageuw' : 'Khageuw',
               'Khamayakha' : 'Khamayakha',
               'Kheleubulow' : 'Kheleubulow',
               'Kwadeware' : 'Kwadeware',
               'Obolyo' : 'Obolyo',
               'Pantai_Yahim' : 'Pantai_Yahim',
               'Puai' : 'Puai',
               'Simporo' : 'Simporo',
               'Sosiri' : 'Sosiri',
               'Yakonde' : 'Yakonde',
               'Yobeh' : 'Yobeh',
               'Yoboi' : 'Yoboi',
               'Yoka' : 'Yoka',
               'Yokiwa' : 'Yokiwa'}

def meta_village(survey):
    return survey['village_name'].apply(lambda x: village_map.get(x))

import bokeh.models.glyphs as bkg
import bokeh.models as bkm
import bokeh.plotting as bkp

def create_village_name_map(survey, pie_column):

    means = survey.groupby('village_name')['_gps_point_latitude',
                                           '_gps_point_longitude',
                                           pie_column].mean()

    source = bkm.ColumnDataSource(data = dict(
            vn = means.index,
            lat = means['_gps_point_latitude'],
            lon = means['_gps_point_longitude'],
            size = [10 for x in means[pie_column]],
            angle = means[pie_column]*6.28))

    wedges = bkg.Wedge(x='lon', y='lat', radius='size',
                       start_angle=0, end_angle='angle',
                       fill_color='green', fill_alpha=0.5,
                       radius_units='screen')
    wedges2 = bkg.Wedge(x = 'lon', y = 'lat', radius = 'size',
                        start_angle='angle', end_angle=6.28,
                        fill_color='red', fill_alpha=0.5,
                        radius_units='screen')
    text = bkg.Text(x='lon', y='lat',
                    text='vn', text_color='000',
                    text_font_size = '12pt', x_offset=10)

    map_options = bkm.GMapOptions(lat=-2.588, lng=140.5170, zoom=11, map_type='terrain')
    plot = bkm.GMapPlot(x_range = bkm.Range1d(),
                        y_range = bkm.Range1d(),
                        map_options = map_options,
                        title = "Lake Sentani" + pie_column)
    plot.add_glyph(source, wedges)
    plot.add_glyph(source, wedges2)
    plot.add_glyph(source, text)

    #plot.add_tools(pan, wheel_zoom, box_zoom, resize, reset)
    plot.add_tools(bkm.BoxZoomTool(), bkm.PanTool(), bkm.ResetTool(), bkm.WheelZoomTool())
    plot.add_layout(bkm.LinearAxis(axis_label='Longitude (deg)', major_tick_in=0), 'below')
    plot.add_layout(bkm.LinearAxis(axis_label='Latitude (deg)', major_tick_in=0), 'left')
    return plot

