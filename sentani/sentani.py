import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

def get_survey():
    return pd.read_excel('../../../data-clean/sentani-merged-cleaned-2015-06-10.xlsx',
                         na_values=[''])

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
