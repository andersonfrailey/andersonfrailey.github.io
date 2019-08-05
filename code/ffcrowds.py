"""
Code for creating plots in 'Wisdom of the Fantasy Football Crowds"
"""
import pandas as pd
import numpy as np
from pathlib import Path


CUR_PATH = Path(__file__).resolve().parent

full_data = pd.read_csv(
    Path(CUR_PATH, "data", "adp_v_points.csv")
)


print("Correlation between ADP rank and actual points rank")
np.corrcoef(full_data["adp_rank"], full_data["points_rank"])
print("Correlation between ADP rank and projected points rank")
np.corrcoef(full_data["adp_rank"], full_data["proj_pts_rank"])

# find biggest surprises and biggest disappointments
print('Biggest Surprises')
surprise = full_data.sort_values('rank_diff', ascending=False).head(10)
print(surprise)
print('Biggest Disappointments')
disappointments = full_data.sort_values('rank_diff').head(10)
print(disappointments)
