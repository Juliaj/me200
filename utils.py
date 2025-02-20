import pandas as pd
import pdfplumber  # You'll need to: pip install pdfplumber


VF_COLUMN_INDEX = 2

r134a_pressure_liquid_vapor_table = {"csv": "r134_liquid_vapor_pressure.csv", "page": [617], "table_number": "A-11",
                        "subject_name": "Properties of Saturated Refrigerant 134a", "table_type": "Pressure",
                        "units": "Specific Volume m3/kg Internal Energy kJ/kg Enthalpy kJ/kg Entropy kJ/kg · K", 
                        "columns": ["Press.bar", "Temp.°C", "Liquid v_f", "Vapor v_g", "Liquid u_f", "Vapor u_g", "Liquid h_f", "Evap. h_fg", "Vapor h_g", "Liquid s_f", "Vapor s_g"],
                        "data_start_line_number": 8,
                        "data_stop_line_number": -2,
                        "vf_div_1000": 1000}

r134a_temperature_liquid_vapor_table = {"csv": "r134_temperature_liquid_vapor.csv", "page": [616], "table_number": "A-10",
                        "subject_name": "Properties of Saturated Refrigerant 134a", "table_type": "Temperature",
                        "units": "Specific Volume m3/kg Internal Energy kJ/kg Enthalpy kJ/kg Entropy kJ/kg · K", 
                        "columns": ["Temp.°C", "Press.bar",  "Liquid v_f", "Vapor v_g", "Liquid u_f", "Vapor u_g", "Liquid h_f", "Evap. h_fg", "Vapor h_g", "Liquid s_f", "Vapor s_g"],
                        "data_start_line_number": 8,
                        "data_stop_line_number": -2,
                        "vf_div_1000": 1000}

water_pressure_liquid_vapor_table = {"csv": "water_pressure_liquid_vapor.csv", "page": [602, 603], "table_number": "A-3",
                        "subject_name": "Properties of Saturated Water", "table_type": "Pressure",
                        "units": "Specific Volume m3/kg Internal Energy kJ/kg Enthalpy kJ/kg Entropy kJ/kg · K", 
                        "columns": ["Press.bar", "Temp.°C", "Liquid v_f", "Vapor v_g", "Liquid u_f", "Vapor u_g", "Liquid h_f", "Evap. h_fg", "Vapor h_g", "Liquid s_f", "Vapor s_g"],
                        "data_start_line_number": 9,
                        "data_stop_line_number": -3,
                        "vf_div_1000": 1000}

water_temperature_liquid_vapor_table = {"csv": "water_temperature_liquid_vapor.csv", "page": [600, 601], "table_number": "A-2",
                        "subject_name": "Properties of Saturated Water", "table_type": "Temperature",
                        "units": "Specific Volume m3/kg Internal Energy kJ/kg Enthalpy kJ/kg Entropy kJ/kg · K", 
                        "columns": ["Temp.°C", "Press.bar", "Liquid v_f", "Vapor v_g", "Liquid u_f", "Vapor u_g", "Liquid h_f", "Evap. h_fg", "Vapor h_g", "Liquid s_f", "Vapor s_g"],
                        "data_start_line_number": 9,
                        "data_stop_line_number": -3,
                        "vf_div_1000": 1000}

propane_pressure_liquid_vapor_table = {"csv": "propane_pressure_liquid_vapor.csv", "page": [628], "table_number": "A-17",
                        "subject_name": "Properties of Saturated Propane", "table_type": "Pressure",
                        "units": "Specific Volume m3/kg Internal Energy kJ/kg Enthalpy kJ/kg Entropy kJ/kg · K", 
                        "columns": ["Press.bar", "Temp.°C", "Liquid v_f", "Vapor v_g", "Liquid u_f", "Vapor u_g", "Liquid h_f", "Evap. h_fg", "Vapor h_g", "Liquid s_f", "Vapor s_g"],
                        "data_start_line_number": 8,
                        "data_stop_line_number": -2,
                        "vf_div_1000": 1000}

propane_temperature_liquid_vapor_table = {"csv": "propane_temperature_liquid_vapor.csv", "page": [627], "table_number": "A-16",
                        "subject_name": "Properties of Saturated Propane", "table_type": "Temperature",
                        "units": "Specific Volume m3/kg Internal Energy kJ/kg Enthalpy kJ/kg Entropy kJ/kg · K", 
                        "columns": ["Temp.°C", "Press.bar", "Liquid v_f", "Vapor v_g", "Liquid u_f", "Vapor u_g", "Liquid h_f", "Evap. h_fg", "Vapor h_g", "Liquid s_f", "Vapor s_g"],
                        "data_start_line_number": 8,
                        "data_stop_line_number": -2,
                        "vf_div_1000": 1000}

ammonia_pressure_liquid_vapor_table = {"csv": "ammonia_pressure_liquid_vapor.csv", "page": [622], "table_number": "A-14",
                        "subject_name": "Properties of Saturated Ammonia", "table_type": "Pressure",
                        "units": "Specific Volume m3/kg Internal Energy kJ/kg Enthalpy kJ/kg Entropy kJ/kg · K", 
                        "columns": ["Press.bar", "Temp.°C", "Liquid v_f", "Vapor v_g", "Liquid u_f", "Vapor u_g", "Liquid h_f", "Evap. h_fg", "Vapor h_g", "Liquid s_f", "Vapor s_g"],
                        "data_start_line_number": 8,
                        "data_stop_line_number": -2,
                        "vf_div_1000": 1000}

ammonia_temperature_liquid_vapor_table = {"csv": "ammonia_temperature_liquid_vapor.csv", "page": [621], "table_number": "A-13",
                        "subject_name": "Properties of Saturated Ammonia", "table_type": "Temperature",
                        "units": "Specific Volume m3/kg Internal Energy kJ/kg Enthalpy kJ/kg Entropy kJ/kg · K", 
                        "columns": ["Temp.°C", "Press.bar", "Liquid v_f", "Vapor v_g", "Liquid u_f", "Vapor u_g", "Liquid h_f", "Evap. h_fg", "Vapor h_g", "Liquid s_f", "Vapor s_g"],
                        "data_start_line_number": 8,
                        "data_stop_line_number": -2,
                        "vf_div_1000": 1000}


def extract_table(file_path="thermo.pdf", table_info=r134a_pressure_liquid_vapor_table):
    tables = []
    with pdfplumber.open(file_path) as pdf:
        for page_number in table_info["page"]:
            text = pdf.pages[page_number].extract_text()
            tables.append(text)
            # print(text)

    # Initialize a list to store rows
    rows = []

    for text in tables:
        if table_info["table_number"] not in text or table_info["subject_name"] not in text or table_info["table_type"] not in text:
            print(f"Page {table_info['page']} does not contain the table {table_info['table_number']} or {table_info['subject_name']} or {table_info['table_type']}")
            return
        # Split the text into lines
        lines = text.split("\n")
        
        for line in lines[table_info["data_start_line_number"]:table_info["data_stop_line_number"]]:
            # remove the last data point
            values = line.split(" ")[:-1]
            # print(values)
            # process "'–" as negative sign
            values = [float(value.replace("–", "-")) for value in values]
            # divide the VF by 1000
            values[VF_COLUMN_INDEX] = values[VF_COLUMN_INDEX] / table_info["vf_div_1000"]

            # Append the row as a list of values, convert all values to float
            rows.append(values)
    
    # Create the DataFrame from the list of rows
    df = pd.DataFrame(rows, columns=table_info["columns"])

    # save dataframe to csv file
    df.to_csv(table_info["csv"], index=False)
    print("df.shape: ", df.shape)

    return df

def convert_pressure_to_bar(pressure_in_atm):
    return pressure_in_atm * 1.01325

def convert_pressure_to_kpa(pressure_in_bar):
    return pressure_in_bar * 100

def linear_interpolation(x_star, x1, x2, y1, y2):
    """
    Linear interpolation to find y_star given x_star and two points (x1,y1) and (x2,y2)
    x_star: the x value to interpolate at
    x1, y1: coordinates of first point
    x2, y2: coordinates of second point
    """
    # round the result to 4 decimal places
    return round(y1 + (x_star - x1) * (y2 - y1) / (x2 - x1), 4)

def interpolate_data(df, value, column_name):
    # interpolate the data to get alll properties at the given pressure

    # if the pressure is in the table, return the row
    if value in df[column_name].values:   
        return df.loc[df[column_name] == value]
    
    # if the pressure is not in the table, find the two pressures in the table and interpolate
    else:
        # find the two pressures in the table
        lower_value = df[column_name][df[column_name] < value].max()
        upper_value = df[column_name][df[column_name] > value].min()
           
        lower_row = df[df[column_name] == lower_value].iloc[0]
        upper_row = df[df[column_name] == upper_value].iloc[0]
        
        print("interpolating data...\nvalue: ", value, "between: ", lower_value, "and", upper_value)
        interpolated_data = []
        interpolated_data.append(value)

        for column in df.columns:
            if column == column_name:
                continue
            value = linear_interpolation(value, lower_value, upper_value, lower_row[column], upper_row[column])
            interpolated_data.append(value)
            print(f"{column}: {value}")

        # construct a df with interpolated data
        interpolated_df = pd.DataFrame([interpolated_data], columns=df.columns)
        return interpolated_df

def interpolate_data_by_pressure(df, pressure_in_bar):
    return interpolate_data(df, pressure_in_bar, "Press.bar")

def interpolate_data_by_temperature(df, temperature):
    return interpolate_data(df, temperature, "Temp.°C")

def specific_volume(vf, vg, quality):
    val = round(vf.values[0] + quality * (vg.values[0] - vf.values[0]), 4)
    print(f"v = {vf.values[0]} + {quality} * ({vg.values[0]} - {vf.values[0]}) = {val}")
    return val

def internal_energy(uf, ug, quality):
    val = round(uf.values[0] + quality * (ug.values[0] - uf.values[0]), 4)
    print(f"u = {uf.values[0]} + {quality} * ({ug.values[0]} - {uf.values[0]}) = {val}")
    return val

def enthalpy(hf, hg, quality):
    val = round(hf.values[0] + quality * (hg.values[0] - hf.values[0]), 4)
    print(f"h = {hf.values[0]} + {quality} * ({hg.values[0]} - {hf.values[0]}) = {val}")
    return val

def entropy(sf, sg, quality):
    val = round(sf.values[0] + quality * (sg.values[0] - sf.values[0]), 4)
    print(f"s = {sf.values[0]} + {quality} * ({sg.values[0]} - {sf.values[0]}) = {val}")
    return val



if __name__ == "__main__":    
    extract_table(file_path="thermo.pdf", table_info=r134a_pressure_liquid_vapor_table)
    extract_table(file_path="thermo.pdf", table_info=r134a_temperature_liquid_vapor_table)
    extract_table(file_path="thermo.pdf", table_info=water_pressure_liquid_vapor_table)
    extract_table(file_path="thermo.pdf", table_info=water_temperature_liquid_vapor_table)
    extract_table(file_path="thermo.pdf", table_info=propane_pressure_liquid_vapor_table)
    extract_table(file_path="thermo.pdf", table_info=propane_temperature_liquid_vapor_table)
    extract_table(file_path="thermo.pdf", table_info=ammonia_pressure_liquid_vapor_table)
    extract_table(file_path="thermo.pdf", table_info=ammonia_temperature_liquid_vapor_table)

   


