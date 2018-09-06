# -*- coding: utf-8 -*-
"""
Created on Tue Sep  4 00:46:48 2018

@author: ARMS COMPUTERS
"""

import csv
import math
import pygal



def read_csv_as_nested_dict(filename, keyfield, separator, quote):
    """
    Inputs:
      filename  - Name of CSV file
      keyfield  - Field to use as key for rows
      separator - Character that separates fields
      quote     - Character used to optionally quote fields

    Output:
      Returns a dictionary of dictionaries where the outer dictionary
      maps the value in the key_field to the corresponding row in the
      CSV file.  The inner dictionaries map the field names to the
      field values for that row.
    """
    
    gdp_dict = {}
    
    try:
        with open(filename, "r", newline = "") as csvfile:
            csvreader = csv.DictReader(csvfile, delimiter = separator, quotechar = quote, 
                                       quoting = csv.QUOTE_MINIMAL)
            for row in csvreader:
                gdp_dict[row[keyfield]] = row
        return gdp_dict
    
    except IOError as my_io:
        print(my_io)

read_csv_as_nested_dict()

def reconcile_countries_by_name(plot_countries, gdp_countries):
    """
    Inputs:
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country names used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country names from
      gdp_countries The set contains the country codes from
      plot_countries that were not found in gdp_countries.
    """
    countries_in_gdp = {}
    countries_not_in_gdp= set()
    
    for country_code in plot_countries:
        if plot_countries[country_code] in gdp_countries:
            countries_in_gdp[country_code] = plot_countries[country_code]
        else:
            countries_not_in_gdp.add(country_code)    
    
    return (countries_in_gdp, countries_not_in_gdp)

def build_map_dict_by_name(gdpinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    year_country_gdp = {}
    empty_year_gdp = set()
    
    gdp_data = read_csv_as_nested_dict(gdpinfo["gdpfile"],
                                       gdpinfo["country_name"],
                                       gdpinfo["separator"],
                                       gdpinfo["quote"])
    
    countries_in_gdp, countries_not_in_gdp = reconcile_countries_by_name(plot_countries, 
                                                                         gdp_data)
    
    for country_code in countries_in_gdp:
        for gdp_country, row in gdp_data.items():
            if plot_countries[country_code] == gdp_country:
                if len(row[year]) != 0:
                    year_country_gdp[country_code] = math.log10(float(row[year]))
                else:
                    empty_year_gdp.add(country_code)
    
#    for country_code in plot_countries:
#        if plot_countries[country_code] in gdp_data:
#            for gdp_country, row in gdp_data.items():
#                if plot_countries[country_code] == gdp_country:
#                    if len(row[year]) != 0:
#                        year_country_gdp[country_code] = math.log10(float(row[year]))
#                    else:
#                        empty_year_gdp.add(country_code)
#        else:
#             country_not_in_GDP.add(country_code)  
             
  
    return (year_country_gdp, countries_not_in_gdp, empty_year_gdp)


def render_world_map(gdpinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      year           - String year to create GDP mapping for
      map_file       - Name of output file to create

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data for the given year and
      writes it to a file named by map_file.
    """
    countries_tuple = build_map_dict_by_name(gdpinfo, plot_countries, year)
    year_country_gdp = countries_tuple[0]
    countries_not_in_gdp = countries_tuple[1]
    empty_year_gdp = countries_tuple[2]
    
    worldmap_chart = pygal.maps.world.World()
    worldmap_chart.title = "GDP by country for {} (log scale), \
                            unified by common country NAME".format(year) 
            
    worldmap_chart.add("GDP for {}".format(year), year_country_gdp)
    worldmap_chart.add("Missing from World", countries_not_in_gdp)
    worldmap_chart.add("No GDP data", empty_year_gdp)
    worldmap_chart.render_to_file(map_file)
    
    return
        
        
def test_render_world_map():
    """
    Test the project code for several years.
    """
    gdpinfo = {
        "gdpfile": "isp_gdp.csv",
        "separator": ",",
        "quote": '"',
        "min_year": 1960,
        "max_year": 2015,
        "country_name": "Country Name",
        "country_code": "Country Code"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, pygal_countries, "1960", "isp_gdp_world_name_1960.svg")

    # 1980
    render_world_map(gdpinfo, pygal_countries, "1980", "isp_gdp_world_name_1980.svg")

    # 2000
    render_world_map(gdpinfo, pygal_countries, "2000", "isp_gdp_world_name_2000.svg")

    # 2010
    render_world_map(gdpinfo, pygal_countries, "2010", "isp_gdp_world_name_2010.svg")
    

# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

#test_render_world_map()