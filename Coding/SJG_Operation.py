import numpy as np
import pandas as pd

def SJG_Operation(WLSTO_SJG, Inflow_SJG, STO_SJG, NHSTO_SJG, LSTO_SJG, Intake_SJG, Stream_SJG):
    
# SJG Operation
    if STO_SJG + Inflow_SJG - (Intake_SJG + Stream_SJG) >= LSTO_SJG:
        Supply_SJGStream = Stream_SJG
        Supply_SJGIntake = Intake_SJG
        Sp_SJG = 0
        if STO_SJG + Inflow_SJG - (Intake_SJG + Stream_SJG)  >= NHSTO_SJG:
            Sp_SJG = STO_SJG + Inflow_SJG - (Intake_SJG + Stream_SJG)  - NHSTO_SJG
    else:
        Supply_SJGStream = (STO_SJG + Inflow_SJG - LSTO_SJG)*(Stream_SJG / (Intake_SJG + Stream_SJG))
        Supply_SJGIntake = (STO_SJG + Inflow_SJG - LSTO_SJG)*(Intake_SJG / (Intake_SJG + Stream_SJG))
        Sp_SJG = 0
# 다음 타임 저류량 저장
    STO_SJG = STO_SJG + Inflow_SJG - Supply_SJGStream - Supply_SJGIntake - Sp_SJG
    WL_SJG = np.interp(STO_SJG, WLSTO_SJG['STO'], WLSTO_SJG['WL'])

    return STO_SJG, WL_SJG, Supply_SJGStream, Supply_SJGIntake, Sp_SJG
