#%% Import Function
import numpy as np
import pandas as pd

from datetime import datetime, timedelta

from Determine_Demand import *
from JAJJ_Operation import *
from DH_Operation import *
from SJG_Operation import *


# 저수지 연계운영 함수
def reservior_system_operation(start_day, end_day, 
                               mode, mode_JA, mode_DH, mode_SJG, 
                               RawInflow_JA, RawInflow_JJ, RawInflow_DH, RawInflow_SJG, 
                               WLSTO_JA, WLSTO_JJ, WLSTO_DH, WLSTO_SJG,
                               Char_JA, Char_JJ, Char_DH, Char_SJG,
                               MonthlyIntake_JA, MonthlyStream_JA, MonthlyDemand_JJ, MonthlyDemand_DH, MonthlyIntake_SJG, MonthlyStream_SJG,
                               RuleCurve_JAJJ, RuleCurve_DH, RuleCurve_SJG,
                               LateralInflow, Max_DA):

    timecon = 24*3600/1000000

    start_date = datetime.strptime(start_day, "%Y-%m-%d")
    end_date = datetime.strptime(end_day, "%Y-%m-%d")
    days = (end_date - start_date).days + 1   
    print(days)

    Date = RawInflow_JA['Date']
    # 유입량 자료 단위변환
    Inflow_JA = RawInflow_JA['Inflow'] * timecon
    Inflow_JJ = RawInflow_JJ['Inflow'] * timecon
    Inflow_DH = RawInflow_DH['Inflow'] * timecon
    Inflow_SJG = RawInflow_SJG['Inflow'] * timecon
    LateralInflow = RawInflow_SJG['Inflow'] * timecon
                                 
    # 저수지 제원 입력
    NHSTO_JA = np.interp(Char_JA['NHWL'], WLSTO_JA['WL'],  WLSTO_JA['STO'])
    RSTO_JA = np.interp(Char_JA['RWL'], WLSTO_JA['WL'],  WLSTO_JA['STO'])
    LSTO_JA = np.interp(Char_JA['LWL'], WLSTO_JA['WL'],  WLSTO_JA['STO'])
    ISTO_JA = np.interp(Char_JA['IWL'], WLSTO_JA['WL'],  WLSTO_JA['STO'])

    NHSTO_JJ = np.interp(Char_JJ['NHWL'], WLSTO_JJ['WL'],  WLSTO_JJ['STO'])
    RSTO_JJ = np.interp(Char_JJ['RWL'], WLSTO_JJ['WL'],  WLSTO_JJ['STO'])
    LSTO_JJ = np.interp(Char_JJ['LWL'], WLSTO_JJ['WL'],  WLSTO_JJ['STO'])
    ISTO_JJ = np.interp(Char_JJ['IWL'], WLSTO_JJ['WL'],  WLSTO_JJ['STO'])   

    NHSTO_DH = np.interp(Char_DH['NHWL'], WLSTO_DH['WL'],  WLSTO_DH['STO'])
    RSTO1_DH = np.interp(Char_DH['RWL1'], WLSTO_DH['WL'],  WLSTO_DH['STO'])
    RSTO2_DH = np.interp(Char_DH['RWL2'], WLSTO_DH['WL'],  WLSTO_DH['STO'])
    LSTO_DH = np.interp(Char_DH['LWL'], WLSTO_DH['WL'],  WLSTO_DH['STO'])
    ISTO_DH = np.interp(Char_DH['IWL'], WLSTO_DH['WL'],  WLSTO_DH['STO'])   

    NHSTO_SJG = np.interp(Char_SJG['NHWL'], WLSTO_SJG['WL'],  WLSTO_SJG['STO'])
    RSTO_SJG = np.interp(Char_SJG['RWL'], WLSTO_SJG['WL'],  WLSTO_SJG['STO'])
    LSTO_SJG = np.interp(Char_SJG['LWL'], WLSTO_SJG['WL'],  WLSTO_SJG['STO'])
    ISTO_SJG = np.interp(Char_SJG['IWL'], WLSTO_SJG['WL'],  WLSTO_SJG['STO'])   

    result_JAJJ = {
        "Date": Date[:-1], "MAX_JA" : np.zeros(days+1), "MIN_JA" : np.zeros(days+1), "MAX_JJ" : np.zeros(days+1), "MIN_JJ" : np.zeros(days+1),
        "STO_JA": np.zeros(days+1), "WL_JA": np.zeros(days+1), "Inflow_JA": Inflow_JA,
        "Demand_JAIntake": np.zeros(days), "Demand_JAStream": np.zeros(days),
        "Supply_JAStream": np.zeros(days), "Supply_JAIntake": np.zeros(days),
        "State_JA": np.full(days, None, dtype=object), "Sp_JA": np.zeros(days),

        "STO_JJ": np.zeros(days+1), "WL_JJ": np.zeros(days+1), "Inflow_JJ": Inflow_JJ,
        "Demand_JJ": np.zeros(days), "Supply_JJ": np.zeros(days), "Sp_JJ": np.zeros(days),

        "Pipe": np.zeros(days)}
    
    result_DH = {
        "Date": Date[:-1], "MAX_DH" : np.zeros(days+1), "MIN_DH" : np.zeros(days+1),
        "STO_DH": np.zeros(days+1), "WL_DH": np.zeros(days+1), "Inflow_DH": Inflow_DH,
        "Demand_DH": np.zeros(days), "Supply_DH": np.zeros(days),
        "State_DH": np.full(days, None, dtype=object), "Sp_DH": np.zeros(days)}
    
    result_SJG = {
        "Date": Date[:-1], "MAX_SJG" : np.zeros(days+1), "MIN_SJG" : np.zeros(days+1),
        "STO_SJG": np.zeros(days+1), "WL_SJG": np.zeros(days+1), "Inflow_SJG": Inflow_SJG,
        "Demand_SJGIntake": np.zeros(days), "Demand_SJGStream": np.zeros(days),
        "Supply_SJGStream": np.zeros(days), "Supply_SJGIntake": np.zeros(days),
        "State_SJG": np.full(days, None, dtype=object), "Sp_SJG": np.zeros(days)}

    result_JAJJ["STO_JA"][0] = ISTO_JA
    result_JAJJ["WL_JA"][0] = float(Char_JA['IWL'].iloc[0])

    result_JAJJ["STO_JJ"][0] = ISTO_JJ
    result_JAJJ["WL_JJ"][0] = float(Char_JJ['IWL'].iloc[0])

    result_DH["STO_DH"][0] = ISTO_DH
    result_DH["WL_DH"][0] = float(Char_DH['IWL'].iloc[0])

    result_SJG["STO_SJG"][0] = ISTO_SJG
    result_SJG["WL_SJG"][0] = float(Char_SJG['IWL'].iloc[0])

    prev_State_JA = None
    prev_State_DH = None
    prev_State_SJG = None

    result_Stream = {"Flow_SJ" : np.zeros(days), "DA_Intake" : np.zeros(days), "Stream_flow" : np.zeros(days)}
    Max_DA = Max_DA * timecon
    

    # 저수지 운영
    for i in range(days):

        #주암, 조절지, 섬진강댐 홍수기 제한수위 설정           
        if (Date[i].month == 6 and Date[i].day >= 21) or (Date[i].month in [7, 8]) or (Date[i].month == 9 and Date[i].day <= 20):
            result_JAJJ["MAX_JA"][i] = RSTO_JA
            result_JAJJ["MAX_JJ"][i] = RSTO_JJ
            result_SJG["MAX_SJG"][i] = RSTO_SJG
        else:
            result_JAJJ["MAX_JA"][i] = NHSTO_JA
            result_JAJJ["MAX_JJ"][i] = NHSTO_JJ
            result_SJG["MAX_SJG"][i] = NHSTO_SJG
            
        #동화댐 홍수기 제한수위 설정(6/21~7/20, 8/21~9/20 : RWL1, 7/21~8/20 : RWL2 )
        if (Date[i].month == 7 and Date[i].day >= 21) or (Date[i].month == 8 and Date[i].day <= 20):
            result_DH["MAX_DH"][i] = RSTO2_DH
        elif (Date[i].month == 6 and Date[i].day >= 21) or (Date[i].month in [7, 8]) or (Date[i].month == 9 and Date[i].day <= 20):
            result_DH["MAX_DH"][i] = RSTO1_DH
        else:
            result_DH["MAX_DH"][i] = NHSTO_DH

        result_JAJJ["MIN_JA"][i] = LSTO_JA
        result_JAJJ["MIN_JJ"][i] = LSTO_JJ
        result_DH["MIN_DH"][i] = LSTO_DH
        result_SJG["MIN_SJG"][i] = LSTO_SJG


        # JA_Operation
        
        [result_JAJJ["Demand_JAIntake"][i], tmpState] = Determine_Demand(
        mode_JA, MonthlyIntake_JA, Month, Day,
        result_JAJJ["STO_JA"][i] + result_JAJJ["STO_JJ"][i], 
        Inflow_JA[i] + Inflow_JJ[i], RuleCurve_JAJJ,
        prev_State_JA)
        [result_JAJJ["Demand_JAStream"][i], tmpState] = Determine_Demand(
        mode_JA, MonthlyStream_JA, Month, Day,
        result_JAJJ["STO_JA"][i] + result_JAJJ["STO_JJ"][i], 
        Inflow_JA[i] + Inflow_JJ[i], RuleCurve_JAJJ,
        prev_State_JA)
        [result_JAJJ["Demand_JJ"][i], tmpState] = Determine_Demand(
        mode_JA, MonthlyDemand_JJ, Month, Day,
        result_JAJJ["STO_JA"][i] + result_JAJJ["STO_JJ"][i],
        Inflow_JA[i] + Inflow_JJ[i], RuleCurve_JAJJ,
        prev_State_JA)
    
        prev_State_JA = tmpState
        result_JAJJ["State_JA"][i] = tmpState

        [result_JAJJ["STO_JA"][i+1], result_JAJJ["WL_JA"][i+1], result_JAJJ["Supply_JAStream"][i], result_JAJJ["Supply_JAIntake"][i], result_JAJJ["Sp_JA"][i], result_JAJJ["STO_JJ"][i+1], result_JAJJ["WL_JJ"][i+1], result_JAJJ["Supply_JJ"][i],  result_JAJJ["Sp_JJ"][i],  result_JAJJ["Pipe"][i]] = JAJJ_Operation(WLSTO_JA, Inflow_JA[i], result_JAJJ["STO_JA"][i],result_JAJJ["MAX_JA"][i], result_JAJJ["MIN_JA"][i], 
                                                                                                                                                                 result_JAJJ["Demand_JAIntake"][i], result_JAJJ["Demand_JAStream"][i], 
                                                                                                                                                                 WLSTO_JJ, Inflow_JJ[i], result_JAJJ["STO_JJ"][i], result_JAJJ["MAX_JJ"][i], result_JAJJ["MIN_JJ"][i], result_JAJJ["Demand_JJ"][i])
        

        # DH_Operation
        [result_DH["Demand_DH"][i], tmpState] = Determine_Demand(
        mode_DH, MonthlyDemand_DH, Month, Day,
        result_DH["STO_DH"][i], Inflow_DH[i], RuleCurve_DH,
        prev_State_DH)
        prev_State_DH = tmpState
        result_DH["State_DH"][i] = tmpState
        
        [result_DH["STO_DH"][i+1], result_DH["WL_DH"][i+1], result_DH["Supply_DH"][i], result_DH["Sp_DH"][i]] = DH_Operation(WLSTO_DH, Inflow_DH[i], result_DH["STO_DH"][i], result_DH["MAX_DH"][i], result_DH["MIN_DH"][i], result_DH["Demand_DH"][i])
        
        # SJG_Operation
        [result_SJG["Demand_SJGIntake"][i], tmpState] = Determine_Demand(
        mode_SJG, MonthlyIntake_SJG, Month, Day,
        result_SJG["STO_SJG"][i], Inflow_SJG[i], RuleCurve_SJG,
        prev_State_SJG)
        [result_SJG["Demand_SJGStream"][i], tmpState] = Determine_Demand(
        mode_SJG, MonthlyStream_SJG, Month, Day,
        result_SJG["STO_SJG"][i], Inflow_SJG[i], RuleCurve_SJG,
        prev_State_SJG)
        prev_State_SJG = tmpState
        result_SJG["State_SJG"][i] = tmpState

        [result_SJG["STO_SJG"][i+1], result_SJG["WL_SJG"][i+1], result_SJG["Supply_SJGStream"][i], result_SJG["Supply_SJGIntake"][i], result_SJG["Sp_SJG"][i]] = SJG_Operation(WLSTO_SJG, Inflow_SJG[i], result_SJG["STO_SJG"][i], result_SJG["MAX_SJG"][i], result_SJG["MIN_SJG"][i], result_SJG["Demand_SJGIntake"][i], result_SJG["Demand_SJGStream"][i])

        # 하류유량, 다압취수량 모의
        if mode == 0:
            # 1. 송정관측소
            result_Stream["Flow_SJ"][i] = result_SJG["Supply_SJGStream"][i] + result_JAJJ["Supply_JAStream"][i]
            #2. 다압취수장 취수가능량 모의
            if result_Stream["Flow_SJ"][i] >= Max_DA:
                result_Stream["DA_Intake"][i] = Max_DA
            else:
                result_Stream["DA_Intake"][i] = 0
                # 3. 다압취수장 하류 유량 모의
            result_Stream["Stream_flow"][i] = result_Stream["Flow_SJ"][i] - result_Stream["DA_Intake"][i]
        elif mode == 1:
            # 1. 송정관측소
            result_Stream["Flow_SJ"][i] = result_SJG["Supply_SJGStream"][i] + result_JAJJ["Supply_JAStream"][i] + result_DH["Supply_DH"][i] + LateralInflow[i]
            # 2. 다압취수장 취수가능량 모의
            if result_Stream["Flow_SJ"][i] >= Max_DA:
                result_Stream["DA_Intake"][i] = Max_DA
            else:
                result_Stream["DA_Intake"][i] = 0
            # 3. 다압취수장 하류 유량 모의
            result_Stream["Stream_flow"][i] = result_Stream["Flow_SJ"][i] - result_Stream["DA_Intake"][i]    


    return result_JAJJ, result_DH, result_SJG, result_Stream, days



