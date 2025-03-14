import numpy as np
import pandas as pd
from datetime import datetime, timedelta

#mode 1 : Non Rule Curve, mode 2 : Rule Curve
def Determine_Demand(mode, MonthlyDemand, month, day, STO, Inflow, RuleCurve_Daily, State):

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

        if State == 'Normal':
            Demand = Demand_Normal

        elif STO+Inflow < Attention:
            if STO+Inflow < Serious:
                Demand = Demand_Serious
                State = 'Serious'
            elif STO+Inflow < Alert:
                Demand = Demand_Alert
                State = 'Alert'
            elif STO+Inflow < Caution:
                Demand = Demand_Caution
                State = 'Caution'
            elif STO+Inflow < Attention:
                Demand = Demand_Attention
                State = 'Attention'
                
        elif State != 'Normal':
            if STO+Inflow >= Normal:            
                Demand = Demand_Normal
                State = 'Normal'
            else:
                if STO+Inflow < Serious:
                    Demand = Demand_Serious
                    State == 'Serious'
                elif STO+Inflow < Alert:
                    Demand = Demand_Alert
                    State = 'Alert'
                elif STO+Inflow < Caution:
                    Demand = Demand_Caution
                    State = 'Caution'
                elif STO+Inflow < Attention:
                    Demand = Demand_Attention
                    State = 'Attention'
    
    Demand = Demand * timecon

    return Demand, State

