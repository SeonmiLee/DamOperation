#%% Importing fucntion
import numpy as np
import pandas as pd
from reservior_system_operation import *

start_day = "1998-10-01"
end_day = "2024-09-30"
file_path = 'C:/Python/DamOperation/'

#mode = 0 : JA+SJG, mode = 1 : JA+SJG+DH
mode = 1

mode_JA = 2
mode_DH = 1
mode_SJG = 1
Max_DA = 4.6


#%% Importing Data(SJG)
RawInflow_SJG = pd.read_excel(file_path + 'InputData/Inflow_Daily/Inflow_Daily_SJG.xlsx')
WLSTO_SJG = pd.read_excel(file_path + 'InputData/WLSTO/WLSTO_SJG.xlsx')
MonthlyIntake_SJG = pd.read_excel(file_path + 'InputData/Demand/Demand_Monthly_SJG_Intake.xlsx')
MonthlyStream_SJG = pd.read_excel(file_path + 'InputData/Demand/Demand_Monthly_SJG_Stream.xlsx')
Char_SJG = pd.read_excel(file_path + 'InputData/DamCharacter/DamCharacter_SJG.xlsx')

#%% Importing Data(JA, JJ)
RawInflow_JA = pd.read_excel(file_path + 'InputData/Inflow_Daily/Inflow_Daily_JA.xlsx')
WLSTO_JA = pd.read_excel(file_path + 'InputData/WLSTO/WLSTO_JA.xlsx')
MonthlyIntake_JA = pd.read_excel(file_path + 'InputData/Demand/Demand_Monthly_JA_Intake.xlsx')
MonthlyStream_JA = pd.read_excel(file_path + 'InputData/Demand/Demand_Monthly_JA_Stream.xlsx')
Char_JA = pd.read_excel(file_path + 'InputData/DamCharacter/DamCharacter_JA.xlsx')

RawInflow_JJ = pd.read_excel(file_path + 'InputData/Inflow_Daily/Inflow_Daily_JJ.xlsx')
WLSTO_JJ = pd.read_excel(file_path + 'InputData/WLSTO/WLSTO_JJ.xlsx')
MonthlyDemand_JJ = pd.read_excel(file_path + 'InputData/Demand/Demand_Monthly_JJ.xlsx')
Char_JJ = pd.read_excel(file_path + 'InputData/DamCharacter/DamCharacter_JJ.xlsx')

#%% Importing Data(DH)
RawInflow_DH = pd.read_excel(file_path + 'InputData/Inflow_Daily/Inflow_Daily_DH.xlsx')
WLSTO_DH = pd.read_excel(file_path + 'InputData/WLSTO/WLSTO_DH.xlsx')
MonthlyDemand_DH = pd.read_excel(file_path + 'InputData/Demand/Demand_Monthly_DH_95%.xlsx')
Char_DH = pd.read_excel(file_path + 'InputData/DamCharacter/DamCharacter_DH.xlsx')

#%%Rule Curve(Daily)
RuleCurve_DH = pd.DataFrame()
RuleCurve_SJG = pd.DataFrame()
RuleCurve_JAJJ = pd.read_excel(file_path + 'InputData/RuleCurve_Daily/RuleCurve_JA.xlsx')

#%% Lateral Inflow(Daily)
LateralInflow = pd.read_excel(file_path + 'InputData/Inflow_Daily/Lateral_Inflow_Daily.xlsx')

#%% Operation
[result_JAJJ, result_DH, result_SJG, result_Stream, days] = reservior_system_operation(start_day, end_day, mode, mode_JA, mode_DH, mode_SJG, 
                                                                  RawInflow_JA, RawInflow_JJ, RawInflow_DH, RawInflow_SJG,
                                                                  WLSTO_JA, WLSTO_JJ, WLSTO_DH, WLSTO_SJG,
                                                                  Char_JA, Char_JJ, Char_DH, Char_SJG,
                                                                  MonthlyIntake_JA, MonthlyStream_JA, MonthlyDemand_JJ, MonthlyDemand_DH, MonthlyIntake_SJG, MonthlyStream_SJG,
                                                                  RuleCurve_JAJJ, RuleCurve_DH, RuleCurve_SJG,
                                                                  LateralInflow, Max_DA)


# 엑셀 파일로 저장
df_JAJJ = pd.DataFrame({key: result_JAJJ[key][:days] for key in result_JAJJ})
df_DH = pd.DataFrame({key: result_DH[key][:days] for key in result_DH})
df_SJG = pd.DataFrame({key: result_SJG[key][:days] for key in result_SJG})
df_Stream = pd.DataFrame({key: result_Stream[key][:days] for key in result_Stream})

output_path = "C:/Python/DamOperation/Result/"
df_JAJJ.to_excel(output_path + "result_JAJJ.xlsx", index=False)
df_DH.to_excel(output_path + "result_DH.xlsx", index=False)
df_SJG.to_excel(output_path + "result_SJG.xlsx", index=False)
df_Stream.to_excel(output_path + "result_Stream.xlsx", index=False)

print("결과 파일이 저장되었습니다!")
