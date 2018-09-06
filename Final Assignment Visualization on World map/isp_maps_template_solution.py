# -*- coding: utf-8 -*-
"""
Created on Wed Sep  5 20:22:07 2018

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
        
               
def build_country_code_converter(codeinfo):
    """
    Inputs:
      codeinfo      - A country code information dictionary

    Output:
      A dictionary whose keys are plot country codes and values
      are world bank country codes, where the code fields in the
      code file are specified in codeinfo.
    """
    
    plot_data_code = {}
    isp_country_codes = read_csv_as_nested_dict(codeinfo["codefile"], 
                                                codeinfo["plot_codes"],
                                                codeinfo["separator"], 
                                                codeinfo["quote"])
    
    for plot_code, row in isp_country_codes.items():
        plot_data_code[plot_code] = row[codeinfo["data_codes"]]

    return plot_data_code

def reconcile_countries_by_code(codeinfo, plot_countries, gdp_countries):
    """
    Inputs:
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary whose keys are plot library country codes
                       and values are the corresponding country name
      gdp_countries  - Dictionary whose keys are country codes used in GDP data

    Output:
      A tuple containing a dictionary and a set.  The dictionary maps
      country codes from plot_countries to country codes from
      gdp_countries.  The set contains the country codes from
      plot_countries that did not have a country with a corresponding
      code in gdp_countries.

      Note that all codes should be compared in a case-insensitive
      way.  However, the returned dictionary and set should include
      the codes with the exact same case as they have in
      plot_countries and gdp_countries.
    """
    converter = build_country_code_converter(codeinfo)
    
    lower_converter = {}
    for key, value in converter.items():
        lower_converter[key.lower()] = value.lower()
        
    lower_gdp = {}
    for key in gdp_countries.keys():
        lower_gdp[key.lower()] = key
                  
    output = {}
    not_found = set()
    for code in plot_countries:
        if code.lower() in lower_converter:
            if lower_converter[code.lower()] in lower_gdp:
                output[code] = lower_converter[code.lower()].upper()
            else:
                not_found.add(code)
        else:
            not_found.add(code)
    return (output, not_found)

def build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year for which to create GDP mapping

    Output:
      A tuple containing a dictionary and two sets.  The dictionary
      maps country codes from plot_countries to the log (base 10) of
      the GDP value for that country in the specified year.  The first
      set contains the country codes from plot_countries that were not
      found in the GDP data file.  The second set contains the country
      codes from plot_countries that were found in the GDP data file, but
      have no GDP data for the specified year.
    """
    
    country_year_gdp = {}
    country_year_not_in_gdp = set()
    
    gdp_data = read_csv_as_nested_dict(gdpinfo["gdpfile"], 
                                                gdpinfo["country_code"],
                                                gdpinfo["separator"], 
                                                gdpinfo["quote"])
    
    reconcile_data = reconcile_countries_by_code(codeinfo, plot_countries, gdp_data)
    countries_in_gdp = reconcile_data[0]
    countries_not_in_gdp = reconcile_data[1]
    
    lower_gdp = {}
    for key,row in gdp_data.items():
        lower_gdp[key.lower()] = row
                  
    lower_countries_in_gdp = {}
    for key in countries_in_gdp:
        lower_countries_in_gdp[key] = countries_in_gdp[key].lower()
                  
    for country_code in lower_countries_in_gdp:
        for gdp_country_code, row in lower_gdp.items():
            if lower_countries_in_gdp[country_code] == gdp_country_code:
                if len(row[year]) != 0:
                    country_year_gdp[country_code] = math.log10(float(row[year]))
                else:
                    country_year_not_in_gdp.add(country_code)
    
    return (country_year_gdp, countries_not_in_gdp, country_year_not_in_gdp)

def render_world_map(gdpinfo, codeinfo, plot_countries, year, map_file):
    """
    Inputs:
      gdpinfo        - A GDP information dictionary
      codeinfo       - A country code information dictionary
      plot_countries - Dictionary mapping plot library country codes to country names
      year           - String year of data
      map_file       - String that is the output map file name

    Output:
      Returns None.

    Action:
      Creates a world map plot of the GDP data in gdp_mapping and outputs
      it to a file named by svg_filename.
    """
    
    countries_tuple = build_map_dict_by_code(gdpinfo, codeinfo, plot_countries, year)
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
    Test the project code for several years
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

    codeinfo = {
        "codefile": "isp_country_codes.csv",
        "separator": ",",
        "quote": '"',
        "plot_codes": "ISO3166-1-Alpha-2",
        "data_codes": "ISO3166-1-Alpha-3"
    }

    # Get pygal country code map
    pygal_countries = pygal.maps.world.COUNTRIES

    # 1960
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1960", "isp_gdp_world_code_1960.svg")

    # 1980
    render_world_map(gdpinfo, codeinfo, pygal_countries, "1980", "isp_gdp_world_code_1980.svg")

    # 2000
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2000", "isp_gdp_world_code_2000.svg")

    # 2010
    render_world_map(gdpinfo, codeinfo, pygal_countries, "2010", "isp_gdp_world_code_2010.svg")


# Make sure the following call to test_render_world_map is commented
# out when submitting to OwlTest/CourseraTest.

#test_render_world_map()




