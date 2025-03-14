import numpy as np
import pandas as pd

# Mode 1 : Non rule curve, Mode 2 : Rule Curve
def JAJJ_Operation(WLSTO_JA, Inflow_JA, STO_JA, NHSTO_JA, LSTO_JA , Intake_JA, Stream_JA, WLSTO_JJ, Inflow_JJ, STO_JJ, NHSTO_JJ, LSTO_JJ, Demand_JJ):

    timecon = 24*60*60/1000000

    tmpWL_JA = np.interp((STO_JA+Inflow_JA), WLSTO_JA['STO'], WLSTO_JA['WL'])
    tmpWL_JJ = np.interp((STO_JJ+Inflow_JJ), WLSTO_JJ['STO'], WLSTO_JJ['WL'])
    tmpWL = abs(tmpWL_JA-tmpWL_JJ)
    if tmpWL < 0.04 : 
        Pipe = 0
    elif tmpWL < 0.25 : 
        Pipe = (7.145 * (tmpWL-0.04)**0.5) * timecon
    else : 
        Pipe = (5.831 * (tmpWL-0.04)**0.5) * timecon

    # JA operation
    if STO_JA + Inflow_JA - Pipe - (Stream_JA + Intake_JA) >= LSTO_JA:
        Supply_JAStream = Stream_JA
        Supply_JAIntake = Intake_JA
        Sp_JA = 0
        if STO_JA + Inflow_JA- Pipe - (Stream_JA + Intake_JA) >= NHSTO_JA:
            Sp_JA = STO_JA + Inflow_JA - Pipe - (Stream_JA + Intake_JA) - NHSTO_JA
    else:
        Supply_JAStream = (STO_JA + Inflow_JA - Pipe - LSTO_JA)*(Stream_JA / (Stream_JA+Intake_JA))
        Supply_JAIntake = (STO_JA + Inflow_JA - Pipe - LSTO_JA)*(Intake_JA / (Stream_JA+Intake_JA))
        Sp_JA = 0

    STO_JA = STO_JA + Inflow_JA - Pipe - Supply_JAStream -  Supply_JAIntake - Sp_JA
    WL_JA = np.interp(STO_JA, WLSTO_JA['STO'], WLSTO_JA['WL'])

    # JJ operation
    if STO_JJ + Inflow_JJ + Pipe - Demand_JJ >= LSTO_JJ:
        Supply_JJ = Demand_JJ
        Sp_JJ = 0
        if STO_JJ + Inflow_JJ + Pipe - Demand_JJ >= NHSTO_JJ:
            Sp_JJ = STO_JJ + Inflow_JJ + Pipe - Demand_JJ - NHSTO_JJ
    else:
        Supply_JJ = STO_JJ + Inflow_JJ + Pipe - LSTO_JJ
        Sp_JJ = 0

    STO_JJ = STO_JJ + Inflow_JJ + Pipe - Supply_JJ - Sp_JJ
    WL_JJ = np.interp(STO_JJ, WLSTO_JJ['STO'], WLSTO_JJ['WL'])

    return STO_JA, WL_JA, Supply_JAStream, Supply_JAIntake, Sp_JA, STO_JJ, WL_JJ, Supply_JJ, Sp_JJ, Pipe 
        