import numpy as np
import pandas as pd

def DH_Operation(WLSTO_DH, Inflow_DH, STO_DH, NHSTO_DH, LSTO_DH, Demand_DH):

    if STO_DH+Inflow_DH-Demand_DH >= NHSTO_DH:
        Supply_DH = Demand_DH
        Sp_DH = STO_DH+Inflow_DH-Demand_DH-NHSTO_DH
    elif STO_DH+Inflow_DH-Demand_DH < LSTO_DH:
        Supply_DH = STO_DH + Inflow_DH - LSTO_DH
        Sp_DH = 0
    else:
        Supply_DH = Demand_DH
        Sp_DH = 0

    STO_DH = STO_DH + Inflow_DH - Supply_DH - Sp_DH
    WL_DH = np.interp(STO_DH, WLSTO_DH['STO'], WLSTO_DH['WL'])

    return STO_DH, WL_DH, Supply_DH, Sp_DH
