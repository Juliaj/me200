from utils import *
import math
def sp11():
    print("HW5 - SP11")
    df_liquid_vapor, table_number, page_number = extract_table("thermo.pdf", r134a_pressure_liquid_vapor_table)

    print("========== Question 1: =========")
    initial_bar_pressure = convert_pressure_to_bar(1)
    print("Initial state with bar_pressure: ", initial_bar_pressure)
    interpolated_df = interpolate_data_by_pressure(df_liquid_vapor, initial_bar_pressure, table_number, page_number)

    
    quality = 0.5
    print("quality: ", quality)

    # initial state
    # rigid container
    rigid_t1 = interpolated_df["Temp.°C"].values[0]
    rigid_v1 = specific_volume(interpolated_df["Liquid v_f"], interpolated_df["Vapor v_g"], quality)
    rigid_u1 = internal_energy(interpolated_df["Liquid u_f"], interpolated_df["Vapor u_g"], quality)
    rigid_h1 = enthalpy(interpolated_df["Liquid h_f"], interpolated_df["Vapor h_g"], quality)
    rigid_s1 = entropy(interpolated_df["Liquid s_f"], interpolated_df["Vapor s_g"], quality)

    # membrane container
    membrane_t1 = rigid_t1
    membrane_v1 = rigid_v1
    membrane_u1 = rigid_u1
    membrane_h1 = rigid_h1
    membrane_s1 = rigid_s1


    print("\n========== Question 2: =========")
    print("Heat up until it becomes saturated vapor")
    print("** rigid container -> the specific volume stays constant")
    quality = 1
    rigid_v2 = rigid_v1
    print("v2 (from previous step): ", rigid_v2)
    print("Based on Table A-12, Page 619: p2 = 2.0 bar")
    rigid_t2 = -10.09
    print("T2 = ", rigid_t2, "C")
    rigid_u2 = 221.43
    print("u2: ", rigid_u2)
    rigid_heat_transfer = round(rigid_u2 - rigid_u1, 4)
    print("heat transfer Q = dU = u2 - u1: ", rigid_heat_transfer)
    
    print("** membrane container -> the pressure is constant")
    membrane_p2 = initial_bar_pressure
    print("p2 (from input): ", membrane_p2)
    membrane_t2 = interpolated_df["Temp.°C"].values[0]
    print("T2 (from previous step, interpolated): ", f"{membrane_t2} C")
    membrane_v2 = quality * interpolated_df["Vapor v_g"].values[0]
    print("v2=vg (from previous step, interpolated): ", membrane_v2)
    membrane_u2 = quality * interpolated_df["Vapor u_g"].values[0]
    print("u2=ug (from previous step, interpolated): ", membrane_u2)
    membrane_heat_transfer = round(membrane_u2 - rigid_u2, 4)
    print("heat transfer Q = dU = u2 - u1: ", membrane_heat_transfer)

    print("\n========== Question 3: =========")
    print("Increase temperature by 6 C starting from initial state")
    

    print("** rigid container -> the specific volume stays constant")
    rigid_v3 = rigid_v1
    print("specific volume stays constant which is the same as in question 1): ", rigid_v3, "we'll use it to calculate the quality")
    df_temperature_liquid_vapor, table_number, page_number = extract_table("thermo.pdf", r134a_temperature_liquid_vapor_table)

    # increase temperature by 6 C
    rigid_t3 = rigid_t1 + 6
    print("T3 = T1 + 6 C: ", rigid_t3, "C")
    # find the properties at the new temperature
    interpolated_df_by_temperature = interpolate_data_by_temperature(df_temperature_liquid_vapor, rigid_t3, table_number, page_number)

    rigid_vf3 = interpolated_df_by_temperature["Liquid v_f"].values[0]  
    print("vf3 (interpolated): ", rigid_vf3)
    rigid_vg3 = interpolated_df_by_temperature["Vapor v_g"].values[0]
    print("vg3 (interpolated): ", rigid_vg3)

    # calculate the quality
    rigid_quality = round((rigid_v3 - rigid_vf3) / (rigid_vg3 - rigid_vf3), 4)
    print("new quality= (v3 - vf3) / (vg3 - vf3): ", rigid_quality)

    # calculate the enthalpy
    rigid_u3 = internal_energy(interpolated_df["Liquid u_f"], interpolated_df["Vapor u_g"], rigid_quality)
    print("u3: ", rigid_u3)

    # delta of the enthalpy
    rigid_delta_u = round(rigid_u3 - rigid_u1, 4)
    print("delta_u_rigid: ", rigid_delta_u)
    print("state: saturated liquid and vapor")


    print("** membrane container, constant pressure")
    print("pressure stays constant: ", initial_bar_pressure, "we'll use it to look up the superheated vapor table")
    membrane_t3 = rigid_t3
    print("T3: ", membrane_t3, "C")
    print("Based on Table A-12, Page p619: p2 = {} bar at {} C".format(initial_bar_pressure, membrane_t3))

    # temperature is -20.1604 C
    membrane_u3 = 216.77
    print("u3: ", membrane_u3)

    # delta of the enthalpy
    membrane_delta_u = round(membrane_u3 - membrane_u1, 4)
    print("delta_u_membrane: ", membrane_delta_u)
    print("state: saturated liquid and vapor")

    # finally the ratio of enthalpy transfer of membrane container to rigid container
    ratio = round(membrane_delta_u / rigid_delta_u, 4)
    print("delta_u_membrane / delta_u_rigid ratio: ", ratio)


def calculate_energy_transfer(mass, specific_heat, initial_temperature, final_temperature):
    return mass * specific_heat * (final_temperature - initial_temperature)

def sp12():
    print("HW5 - SP12")
    metal_weight_kg = 2.2
    metal_temperature_kevin = 600
    water_temperature_celsius = 25
    water_temperature_kelvin = water_temperature_celsius + 273.15
    volume_tank_m3 = 0.125
    metals = ["aluminum", "cast iron", "copper", "lead"]

    print("Given: ")
    print("\tweight of the metal: ", metal_weight_kg, "kg")
    print("\ttemperature of the metal: ", metal_temperature_kevin, "K")
    print("\ttemperature of the water: ", water_temperature_celsius, "C")
    print("\tvolume of the tank: ", volume_tank_m3, "m^3")

    # using SI units j/kg*K
    C_aluminum = 900
    C_cast_iron = 450
    C_copper = 385
    C_lead = 128
    C_water = 4186
    
   # Use Cp or Cv to calculate the energy transfer ?
    print("** Question 1: Use Cp or Cv to calculate the energy transfer ? ")
    print("Answer: ")
    print("\tfind the specific heat of each metal from internet (j/kg*K): ", "aluminum: ", C_aluminum, "cast iron: ", C_cast_iron, "copper: ", C_copper, "lead: ", C_lead)
    print("""\tUse Cp (constant pressure) to calculate the energy transfer because the tank is open to the atmosphere and the process 
          \tis at atmospheric pressure. In addition, we are deal with solid metal and liquid water.""")
    print("""\tUse Cv (constant volume) for closed system in rigid container.""")

    # Use Cp to calculate the energy transfer because 
    print("\n** Question 2: Final temperature for all blocks and water ")
    
    print("Answer: ")
    water_density = 1000
    print("\twater_density = 1000 kg/m^3")
    water_mass = water_density * volume_tank_m3
    print("\twater_mass = water_density * volume_tank_m3: ", water_mass)

    metal_initial_energy_sum = 0
    for cp in [C_aluminum, C_cast_iron, C_copper, C_lead]:
        metal_initial_energy_sum += metal_weight_kg * metal_temperature_kevin * cp
    
    water_initial_energy_sum = water_mass * water_temperature_kelvin * C_water

    metal_mass_cp_sum = 0
    for cp in [C_aluminum, C_cast_iron, C_copper, C_lead]:
        metal_mass_cp_sum += metal_weight_kg * cp

    print("\tmetal_initial_energy_sum (add up the energy of each metal): ", metal_initial_energy_sum)
    print("\twater_initial_energy_sum = water_mass * water_temperature_kelvin * C_water: ", water_initial_energy_sum)
    print("\tmetal_mass_cp_sum: ", metal_mass_cp_sum)
    print("\twater_mass_cp = water_mass*C_water: ", water_mass*C_water)

    T_final = round((metal_initial_energy_sum + water_initial_energy_sum) / (metal_mass_cp_sum + water_mass*C_water), 1)
    print("\tT_final = (metal_initial_energy_sum + water_initial_energy_sum) / (metal_mass_cp_sum + water_mass*C_water): ", T_final)
    print("\tfinal temperature: ", T_final, "K")

    print("\ttempurate change for each metal:   ", T_final - metal_temperature_kevin)
    print("\ttempurate change for water:       ", round(T_final - water_temperature_kelvin, 1))

    print("""\n** Question 3: If the mass of the block would double, would the change in temperature double as
        well? Alternatively, if the volume of water were to half what e ect would that have. Justify your answer""")
    print("Answer: ")
    print("""\tif the mass of the block would double, the change in temperature would NOT double as well.
        \tInstead, the final temperature will be higher, and the temperature change will be less than double 
        \tdue to the increased heat capacity of the blocks.""")
    print("""\tif the volume of water were to half, the change in temperature would NOT be half.
        \tThe blocks will experience a smaller temperature change compared to the original scenario because the water's reduced 
        \theat capacity means it cannot absorb as much heat.""")
    print("""\tJustification: Because the energy transfer is determined by the temperature difference between the metal and water.""")
    print("""\tT_final = (metal_initial_energy_sum + water_initial_energy_sum) / (metal_mass_cp_sum + water_mass*C_water)""")

def sp13():
    print("HW5 - SP13")
    """
    A piston ﬁlled with air is used in a power cycle. The temperature of air starts at 600 R and 2
    bar (State 1). The following processes are done in the piston to get work out of the system,
    Process 1-2 Constant volume heating to 4 bar
    Process 2-3 Constant temperature expansion
    Process 3-1 Constant pressure compression back to state 1
    You may assume an ideal gas model for the air in the piston. Answer the following about
    1. What is the pressure, speciﬁc volume, and temperature, p , v , T at all the states?
    Graph on a p-v and a T-v diagram. Clearly label your states.
    2. What is the net work of the system? What processes produce work? What
    processes required energy from outside?
    3. Now consider the assumption of an ideal gas? What is the compressibility factor for
    air at these temperatures and pressure? Was your ideal gas assumption ok?
    4. Now swap out the air with a lighter gas, such as pure helium gas. What would
    happen to the cycle? Would there be more work? Less? You may justify your answer
    with either calculations or with reasonable thinking.
    """
    # given
    print("Given: ")
    temperature_1_R = 600
    print("\ttemperature_1_R: ", temperature_1_R)
    temperature_1_kelvin = round(temperature_1_R * 5/9, 2)
    print("\ttemperature_1_kelvin: ", temperature_1_kelvin)
    # process 1-2
    pressure_1_bar = 2
    print("\tpressure_1_bar: ", pressure_1_bar)
    pressure_1_kpa = pressure_1_bar * 100
    print("\tpressure_1_kpa: ", pressure_1_kpa)
    pressure_2_bar = 4
    print("\tpressure_2_bar: ", pressure_2_bar)
    pressure_2_kpa = pressure_2_bar * 100
    print("\tpressure_2_kpa: ", pressure_2_kpa)

    # process 2-3
    temperature_3_R = temperature_1_R
    print("\ttemperature_3_R(same as temperature_1_R): ", temperature_3_R)
    # process 3-1
    pressure_3_bar = pressure_1_bar
    print("\tpressure_3_bar: ", pressure_3_bar)
    pressure_3_kpa = pressure_3_bar * 100
    print("\tpressure_3_kpa: ", pressure_3_kpa)
    # ideal gas constant in kJ/kg*K
    R_air = 0.287
    print("\tR_air: ", R_air)

    print("Convertion: ")
    print("\ttemperature_1_kelvin: ", temperature_1_kelvin)
    print("\tpressure_1_kpa: ", pressure_1_kpa)
    print("\tpressure_2_kpa: ", pressure_2_kpa)
    print("\tpressure_3_kpa: ", pressure_3_kpa)

    print("Answer: ")
    # 1. What is the pressure, speciﬁc volume, and temperature, p , v , T at all the states?
    # Graph on a p-v and a T-v diagram. Clearly label your states.
    # state 1
    print("\nstate 1: Constant volume heating")
    volume_1_m3 = round(R_air * temperature_1_kelvin / (pressure_1_kpa), 2)
    
    print("\tpressure_1: ", pressure_1_kpa, "kPa")
    print("\ttemperature_1: ", temperature_1_kelvin, "K")
    print("\tvolume_1: ", volume_1_m3, "m^3")

    # state 2
    print("\nstate 2: Constant temperature expansion")
    volume_2_m3 = volume_1_m3   
    print("\tpressure_2: ", pressure_2_kpa, "kPa")
    temperature_2_kelvin = round(pressure_2_kpa * volume_2_m3 / R_air, 2)
    print("\ttemperature_2: ", temperature_2_kelvin, "K")
    print("\tvolume_2: ", volume_2_m3, "m^3")

    # state 3
    print("\nstate 3: Constant pressure compression")
    
    print("\tpressure_3: ", pressure_3_kpa, "kPa")
    temperature_3_kelvin = temperature_2_kelvin       
    print("\ttemperature_3: ", temperature_3_kelvin, "K")
    volume_3_m3 = round(R_air * temperature_3_kelvin / (pressure_3_kpa), 2)
    print("\tvolume_3: ", volume_3_m3, "m^3")

    # 2. What is the net work of the system? What processes produce work? What
    # processes required energy from outside?
    print("\n** Question 2: What is the net work of the system? What processes produce work? What processes required energy from outside?")
    # process 1-2: Constant volume heating
    print("\nprocess 1-2: Constant volume heating")
    Cv_air = 0.718
    print("\tCv_air: ", Cv_air)
    Cp_air = 1.005
    print("\tCp_air: ", Cp_air)
    mass_air = 1
    print("\tmass_air: ", mass_air)
    W12 = 0
    Q12 = round( mass_air * Cv_air * (temperature_2_kelvin - temperature_1_kelvin), 2)
    print("\tWork done by the air: W12: ", W12, "kJ")
    print("\tHeat added to the air: Q12 =  mass_air * Cv_air * (temperature_2_kelvin - temperature_1_kelvin)")
    print(f"\tHeat added to the air: Q12 = {mass_air} * {Cv_air} * ({temperature_2_kelvin} - {temperature_1_kelvin}) = {Q12} kJ")

    # process 2-3: Constant temperature expansion
    print("\nprocess 2-3: Constant temperature expansion, isothermal process")
    Q23 = round(mass_air * R_air * temperature_2_kelvin * math.log(pressure_2_kpa / pressure_3_kpa), 2)
    w23 = Q23
    print("\tWork done by the air: W23: ", w23, "kJ")
    print("\tHeat added to the air: Q23 = mass_air * R_air * temperature_2_kelvin * math.log(pressure_2_kpa / pressure_3_kpa)")
    print(f"\tHeat added to the air: Q23 = {mass_air} * {R_air} * {temperature_2_kelvin} * math.log({pressure_2_kpa} / {pressure_3_kpa}) = {Q23} kJ")

    # process 3-1: Constant pressure compression
    print("\nprocess 3-1: Constant pressure compression")
    Q31 = round(mass_air * Cp_air * (temperature_1_kelvin - temperature_3_kelvin), 2)
    W31 = pressure_3_kpa * (volume_3_m3 - volume_1_m3)
    W_net = W12 + w23 + W31
    print("\tWork done by the air: W31: ", W31, "kJ")
    print("\tHeat added to the air: Q31: ", Q31, "kJ")
    print("\tNet work: W_net: ", W_net, "kJ")


    # 3. Now consider the assumption of an ideal gas? What is the compressibility factor for
    # air at these temperatures and pressure? Was your ideal gas assumption ok?
    print("\n** Question 3: Now consider the assumption of an ideal gas? What is the compressibility factor for air at these temperatures and pressure? Was your ideal gas assumption ok?")
    print("\tcompressibility factor: Z = p * v / (R * T)")
    Z = pressure_1_kpa * volume_1_m3 / (R_air * temperature_1_kelvin)
    print("\tcompressibility factor: Z = ", Z)
    print("\tThe ideal gas assumption is valid because the compressibility factor is around 1.")

    # 4. Now swap out the air with a lighter gas, such as pure helium gas. What would
    # happen to the cycle? Would there be more work? Less? You may justify your answer
    # with either calculations or with reasonable thinking.
    print("\n** Question 4: Now swap out the air with a lighter gas, such as pure helium gas. What would happen to the cycle? Would there be more work? Less? You may justify your answer with either calculations or with reasonable thinking.")
    R_helium = 2.0769
    Cv_helium = 3.1156
    print("\tcompressibility factor: Z = p * v / (R * T)")
    Z = pressure_1_kpa * volume_1_m3 / (R_helium * temperature_1_kelvin)
    print("\tcompressibility factor: Z = ", Z)
    print("\tThe cycle would be more efficient because the lighter gas has a lower specific heat capacity.")
    print("\tThere would be more work because the lighter gas has a lower specific heat capacity.")
    print("\tThere would be less energy required from outside because the lighter gas has a lower specific heat capacity.")
    print("\tThe temperature ratio would be the same because they depend on pressure ratio and the gas constant.")

if __name__ == "__main__":
    sp11()
    print("--------------------------------")
    sp12()
    print("--------------------------------")
    sp13()

   


