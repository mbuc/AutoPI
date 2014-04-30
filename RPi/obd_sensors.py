 #!/usr/bin/env python
###########################################################################
# obd_sensors.py
#
# Copyright 2004 Donour Sizemore (donour@uchicago.edu)
# Copyright 2009 Secons Ltd. (www.obdtester.com)
#
# This file is part of pyOBD.
#
# pyOBD is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# pyOBD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyOBD; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###########################################################################

def hex_to_int(str):
    i = eval("0x" + str, {}, {})
    return i

def maf(code):
    #currently converting to lb/min. needs to be grams/sec......
    code = hex_to_int(code)
    return code * 0.00132276

def throttle_pos(code):
    code = hex_to_int(code)
    return code * 100.0 / 255.0

def intake_m_pres(code): # in kPa
    code = hex_to_int(code)
    return code / 0.14504
    
def rpm(code):
    code = hex_to_int(code)
    return code / 4

def speed(code):
    code = hex_to_int(code)
    return code / 1.609

def percent_scale(code):
    code = hex_to_int(code)
    return code * 100.0 / 255.0

def timing_advance(code):
    code = hex_to_int(code)
    return (code - 128) / 2.0

def sec_to_min(code):
    code = hex_to_int(code)
    return code / 60

def temp(code):
    code = hex_to_int(code)
    return code - 40 

def cpass(code):
    #fixme
    return code

def fuel_trim_percent(code):
    code = hex_to_int(code)
    return (code - 128.0) * 100.0 / 128

def dtc_decrypt(code):
    #first byte is byte after PID and without spaces
    num = hex_to_int(code[:2]) #A byte
    res = []

    if num & 0x80: # is mil light on
        mil = 1
    else:
        mil = 0
        
    # bit 0-6 are the number of dtc's. 
    num = num & 0x7f
    
    res.append(num)
    res.append(mil)
    
    numB = hex_to_int(code[2:4]) #B byte
      
    for i in range(0,3):
        res.append(((numB>>i)&0x01)+((numB>>(3+i))&0x02))
    
    numC = hex_to_int(code[4:6]) #C byte
    numD = hex_to_int(code[6:8]) #D byte
       
    for i in range(0,7):
        res.append(((numC>>i)&0x01)+(((numD>>i)&0x01)<<1))
    
    res.append(((numD>>7)&0x01)) #EGR SystemC7  bit of different 
    
    return res

def hex_to_bitstring(str):
    bitstring = ""
    for i in str:
        # silly type safety, we don't want to eval random stuff
        if type(i) == type(''): 
            v = eval("0x%s" % i)
            if v & 8 :
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 4:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 2:
                bitstring += '1'
            else:
                bitstring += '0'
            if v & 1:
                bitstring += '1'
            else:
                bitstring += '0'                
    return bitstring

class Sensor:
    def __init__(self, shortName, sensorName, sensorcommand, sensorValueFunction, u):
        self.shortname = shortName
        self.name = sensorName
        self.cmd  = sensorcommand
        self.value= sensorValueFunction
        self.unit = u

SENSORS = [
    Sensor("pids_a"                , "PIDs Supported [01 - 1F]", "0100", hex_to_bitstring ,""       ),    
    Sensor("dtc_status"            , "Status Since DTC Cleared", "0101", dtc_decrypt      ,""       ),    
    Sensor("dtc_ff"                , "DTC Causing Freeze Frame", "0102", cpass            ,""       ),    
    Sensor("fuel_status"           , "      Fuel System Status", "0103", cpass            ,""       ),
    Sensor("load"                  , "   Calculated Load Value", "0104", percent_scale    ,"%"      ),    
    Sensor("ctemp"                 , "     Coolant Temperature", "0105", temp             ,"C"      ),
    Sensor("short_term_fuel_trim_1", "    Short Term Fuel Trim", "0106", fuel_trim_percent,"%"      ),
    Sensor("long_term_fuel_trim_1" , "     Long Term Fuel Trim", "0107", fuel_trim_percent,"%"      ),
    Sensor("short_term_fuel_trim_2", "    Short Term Fuel Trim", "0108", fuel_trim_percent,"%"      ),
    Sensor("long_term_fuel_trim_2" , "     Long Term Fuel Trim", "0109", fuel_trim_percent,"%"      ),
    Sensor("fuel_pressure"         , "      Fuel Rail Pressure", "010A", cpass            ,"kPa"    ),
    Sensor("manifold_pressure"     , "Intake Manifold Pressure", "010B", intake_m_pres    ,"kPa"    ),
    Sensor("rpm"                   , "              Engine RPM", "010C", rpm              ,"RPM"    ),
    Sensor("speed"                 , "           Vehicle Speed", "010D", speed            ,"MPH"    ),
    Sensor("timing_advance"        , "          Timing Advance", "010E", timing_advance   ,"degrees"),
    Sensor("intake_air_temp"       , "  Intake Air Temperature", "010F", temp             ,"C"      ),
    Sensor("maf"                   , "     Air Flow Rate (MAF)", "0110", maf              ,"lb/min" ),
    Sensor("throttle_pos"          , "       Throttle Position", "0111", throttle_pos     ,"%"      ),
    Sensor("secondary_air_status"  , "    Secondary Air Status", "0112", cpass            ,""       ),
    Sensor("o2_sensor_positions"   , "  Location of O2 sensors", "0113", cpass            ,""       ),
    Sensor("o211"                  , "        O2 Sensor: 1 - 1", "0114", fuel_trim_percent,"Volts %"),
    Sensor("o212"                  , "        O2 Sensor: 1 - 2", "0115", fuel_trim_percent,"Volts %"),
    Sensor("o213"                  , "        O2 Sensor: 1 - 3", "0116", fuel_trim_percent,"Volts %"),
    Sensor("o214"                  , "        O2 Sensor: 1 - 4", "0117", fuel_trim_percent,"Volts %"),
    Sensor("o221"                  , "        O2 Sensor: 2 - 1", "0118", fuel_trim_percent,"Volts %"),
    Sensor("o222"                  , "        O2 Sensor: 2 - 2", "0119", fuel_trim_percent,"Volts %"),
    Sensor("o223"                  , "        O2 Sensor: 2 - 3", "011A", fuel_trim_percent,"Volts %"),
    Sensor("o224"                  , "        O2 Sensor: 2 - 4", "011B", fuel_trim_percent,"Volts %"),
    Sensor("obd_standard"          , "         OBD Designation", "011C", cpass            ,""       ),
    Sensor("o2_sensor_position_b"  ,"  Location of O2 sensors" , "011D", cpass            ,""       ),
    Sensor("aux_input"             , "        Aux input status", "011E", cpass            ,""       ),
    Sensor("engine_time"           , " Time Since Engine Start", "011F", sec_to_min       ,"min"    ),
    Sensor("engine_mil_time"       , "  Engine Run with MIL on", "014D", sec_to_min       ,"min"    ),
    Sensor("pids_b"                , "PIDs Supported [20 - 40]", "0120", hex_to_bitstring ,""       ),

    Sensor("engine_mil_dist"       , "Distance Run with MIL on", "0121", cpass            ,"km"     ),
    Sensor("fuel_rail_press_vac"   , "Fuel Rail Pressure (vac)", "0122", cpass            ,"kPa"    ),
    Sensor("fuel_rail_press_gdi"   , "Fuel Rail Pressure (gdi)", "0123", cpass            ,"kPa"    ),
    Sensor("o2s1_wr_lambda_volt"   , "O2 Sens 1 WR Lambda Volt", "0124", cpass            ,"V"      ),
    Sensor("o2s2_wr_lambda_volt"   , "O2 Sens 2 WR Lambda Volt", "0125", cpass            ,"V"      ),
    Sensor("o2s3_wr_lambda_volt"   , "O2 Sens 3 WR Lambda Volt", "0126", cpass            ,"V"      ),
    Sensor("o2s4_wr_lambda_volt"   , "O2 Sens 4 WR Lambda Volt", "0127", cpass            ,"V"      ),
    Sensor("o2s5_wr_lambda_volt"   , "O2 Sens 5 WR Lambda Volt", "0128", cpass            ,"V"      ),
    Sensor("o2s6_wr_lambda_volt"   , "O2 Sens 6 WR Lambda Volt", "0129", cpass            ,"V"      ),
    Sensor("o2s7_wr_lambda_volt"   , "O2 Sens 7 WR Lambda Volt", "012A", cpass            ,"V"      ),
    Sensor("o2s8_wr_lambda_volt"   , "O2 Sens 8 WR Lambda Volt", "012B", cpass            ,"V"      ),

    Sensor("commanded_egr"         , "           Commanded EGR", "012C", cpass            ,"%"      ),
    Sensor("egr_error"             , "               EGR Error", "012D", cpass            ,"%"      ),
    Sensor("commanded_evap_purge"  , "    Commanded Evap Purge", "012E", cpass            ,"%"      ),
    Sensor("fuel_level_input"      , "        Fuel Level Input", "012F", cpass            ,"%"      ),
    Sensor("warmups_count"         , " Warmups Since Codes Clr", "0130", hex_to_bitstring ,""       ),
    Sensor("dist_since_clr"        , "Distance Since Codes Clr", "0131", cpass            ,"km"     ),
    Sensor("evap_sys_press"        , "Evap. System Vapor Press", "0132", cpass            ,"Pa"     ),
    Sensor("barometric_pressure"   , "     Barometric Pressure", "0133", hex_to_bitstring ,"kPa"    ),
    Sensor("o2s1_wr_lambda_curr"   , "O2 Sens 1 WR Lambda Crnt", "0134", cpass            ,"mA"     ),
    Sensor("o2s2_wr_lambda_curr"   , "O2 Sens 2 WR Lambda Crnt", "0135", cpass            ,"mA"     ),
    Sensor("o2s3_wr_lambda_curr"   , "O2 Sens 3 WR Lambda Crnt", "0136", cpass            ,"mA"     ),
    Sensor("o2s4_wr_lambda_curr"   , "O2 Sens 4 WR Lambda Crnt", "0137", cpass            ,"mA"     ),
    Sensor("o2s5_wr_lambda_curr"   , "O2 Sens 5 WR Lambda Crnt", "0138", cpass            ,"mA"     ),
    Sensor("o2s6_wr_lambda_curr"   , "O2 Sens 6 WR Lambda Crnt", "0139", cpass            ,"mA"     ),
    Sensor("o2s7_wr_lambda_curr"   , "O2 Sens 7 WR Lambda Crnt", "013A", cpass            ,"mA"     ),
    Sensor("o2s8_wr_lambda_curr"   , "O2 Sens 8 WR Lambda Crnt", "013B", cpass            ,"mA"     ),
    Sensor("cat_temp_b1_s1"        , "Catalyst Temp Bank 1 S1 ", "013C", cpass            ,"C"      ),
    Sensor("cat_temp_b2_s1"        , "Catalyst Temp Bank 2 S1 ", "013D", cpass            ,"C"      ),
    Sensor("cat_temp_b1_s2"        , "Catalyst Temp Bank 1 S2 ", "013E", cpass            ,"C"      ),
    Sensor("cat_temp_b2_s2"        , "Catalyst Temp Bank 2 S2 ", "013F", cpass            ,"C"      ),

    Sensor("pids_c"                , "PIDs Supported [41 - 60]", "0140", hex_to_bitstring ,""       ),
    Sensor("mon_status"            , "Monitor Stat. This Drive", "0141", cpass            ,""       ),
    Sensor("control_mode_voltage"  , "Control Mode Voltage"    , "0142", cpass            ,"V"      ),
    Sensor("abs_load_value"        , "Absolute Load Value"     , "0143", cpass            ,"%"      ),
    Sensor("cmd_equiv_ratio"       , "Cmd Equivalence Ratio"   , "0144", cpass            ,""       ),
    Sensor("rel_throttle_pos"      , "Relative Throttle Posit.", "0145", cpass            ,"%"      ),
    Sensor("ambient_air_temp"      , "Ambient Air Temperature" , "0146", cpass            ,"C"      ),
    Sensor("abs_throttle_pos_B"    , "Absolute Throttle Pos. B", "0147", cpass            ,"%"      ),
    Sensor("abs_throttle_pos_C"    , "Absolute Throttle Pos. C", "0148", cpass            ,"%"      ),
    Sensor("abs_throttle_pos_D"    , "Absolute Throttle Pos. D", "0149", cpass            ,"%"      ),
    Sensor("abs_throttle_pos_E"    , "Absolute Throttle Pos. E", "014A", cpass            ,"%"      ),
    Sensor("abs_throttle_pos_F"    , "Absolute Throttle Pos. F", "014B", cpass            ,"%"      ),
    Sensor("cmd_throttle_actuator" , "Cmded Throttle Actuator" , "014C", cpass            ,"%"      ),
    Sensor("time_run_MIL_on"       , "Time run with MIL on"    , "014D", cpass            ,"min"    ),
    Sensor("time_since_codes_clrd" , "Time since DTCs cleared" , "014E", cpass            ,"min"    ),
    Sensor("misc"                  , "Misc"                    , "014F", cpass            ,""       ),

    Sensor("max_air_flow_MAF"      , "MAF Max Air Flow"        , "0150", cpass            ,"g/s"    ),
    Sensor("fuel_type"             , "Fuel Type"               , "0151", cpass            ,""       ),
    Sensor("ethanol_percent"       , "Ethanol Fuel Percent"    , "0152", cpass            ,"%"      ),






    ]
     
    
#___________________________________________________________

def test():
    for i in SENSORS:
        print i.name, i.value("F")

if __name__ == "__main__":
    test()
