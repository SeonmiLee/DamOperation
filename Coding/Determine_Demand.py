import numpy as np
import pandas as pd
from datetime import datetime, timedelta

#mode 1 : Non Rule Curve, mode 2 : Rule Curve
def Determine_Demand(mode, MonthlyDemand, month, day, STO, Inflow, RuleCurve_Daily, prev_State):

    timecon = 24*3600/1000000    


    if mode == 1:
        State = 'None'
        Demand = MonthlyDemand[MonthlyDemand['Month'] == month]['Normal']

        
    elif mode == 2:

        RuleCurve_Daily['Date'] = pd.to_datetime(RuleCurve_Daily['Date'])

        Filter_RuleCurve = RuleCurve_Daily[(RuleCurve_Daily['Date'].dt.month == month) & (RuleCurve_Daily['Date'].dt.day == day)]
        Normal = Filter_RuleCurve['Normal'].iloc[0]
        Attention = Filter_RuleCurve['Attention'].iloc[0]
        Caution = Filter_RuleCurve['Caution'].iloc[0]
        Alert = Filter_RuleCurve['Alert'].iloc[0]
        Serious = Filter_RuleCurve['Serious'].iloc[0]

        Demand_Normal = MonthlyDemand[MonthlyDemand['Month'] == month]['Normal'].iloc[0]
        Demand_Attention = MonthlyDemand[MonthlyDemand['Month'] == month]['Caution'].iloc[0]
        Demand_Caution = MonthlyDemand[MonthlyDemand['Month'] == month]['Normal'].iloc[0]
        Demand_Alert = MonthlyDemand[MonthlyDemand['Month'] == month]['Alert'].iloc[0]
        Demand_Serious = MonthlyDemand[MonthlyDemand['Month'] == month]['Serious'].iloc[0]

 
        total_water = STO + Inflow

        # 1. 첫 번째 타임이라면, `STO + Inflow`를 기준으로 상태 결정
        if prev_State is None :
            if total_water >= Attention:
                State = 'Normal'
            elif total_water <= Serious:
                State = 'Serious'
            elif total_water <= Alert:
                State = 'Alert'
            elif total_water <= Caution:
                State = 'Caution'
            elif total_water <= Attention:
                State = 'Attention'
        
        else:
            # 2. 이전 상태가 존재하는 경우
            if total_water >= Normal:
                State = 'Normal'
            elif total_water < Serious:
                State = 'Serious' 
            elif total_water < Alert and prev_State in ['Attention', 'Caution', 'Alert', 'Serious']:
                State = 'Alert'
            elif total_water < Caution and prev_State in ['Attention', 'Caution']:
                State = 'Caution'
            elif total_water < Attention and prev_State == 'Attention':
                State = 'Attention'
            else:
                State = prev_State  # Normal이 아니고 이전 상태보다 낮아지지 않았다면 그대로 유지

        # 3. 현재 State에 따라 Demand 결정
        Demand = {
            'Normal': Demand_Normal,
            'Attention': Demand_Attention,
            'Caution': Demand_Caution,
            'Alert': Demand_Alert,
            'Serious': Demand_Serious
        }[State]

    Demand = Demand * timecon

    return Demand, State

