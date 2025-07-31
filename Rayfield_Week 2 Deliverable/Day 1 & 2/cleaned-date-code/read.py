#!/usr/bin/env python3.11
import matplotlib.pyplot as plt
import pandas as pd
from pathlib import Path

from sklearn.ensemble import IsolationForest

root = Path('data/fpv')

column_mapping = {
	"FSBATT":  "FPV DAS Battery Volts",
	"FSTEMP":  "FPV DAS Panel Temp C",
	"NWPTMA":  "NW A PANEL TEMP C",
	"NWPTMB":  "NW B PANEL TEMP C",
	"NWPTMC":  "NW C PANEL TEMP C",
	"NOPTMA":  "North A PANEL TEMP C",
	"NOPTMB":  "North B PANEL TEMP C",
	"NOPTMC":  "North C PANEL TEMP C",
	"NEPTMA":  "NE A PANEL TEMP C",
	"NEPTMB":  "NE B PANEL TEMP C",
	"NEPTMC":  "NE C PANEL TEMP C",
	"MDPTMA":  "Middle A PANEL TEMP C",
	"MDPTMB":  "Middle B PANEL TEMP C",
	"MDPTMC":  "Middle C PANEL TEMP C",
	"SOPTMA":  "South A PANEL TEMP C",
	"SOPTMB":  "South B PANEL TEMP C",
	"SOPTMC":  "South C PANEL TEMP C",
	"FHZIRR":  "FPV Epp Horiz Irradiance W/m2",
	"FPAIRR":  "FPV RT1 POA Irradiance W/m2",
	"FPNLTC":  "RT1 Add'l PANEL TEMP C",
	"WTM1_0":  "WATER TEMP 1.0ft C",
	"WTM275":  "WATER TEMP 2.75ft C",
	"WTM4_5":  "WATER TEMP 4.5ft C",
	"FPVDBT":  "FPV DryBulb Temp C",
	"FPV_RH":  "FPV Relative Humidity %",
	"FRAIRP":  "FPV Relative Air Pressure hPa",
	"FWINDA":  "FPV Wind Speed Avg m/s",
	"FWINDM":  "FPV Wind Speed Max m/s",
	"FWINDV":  "FPV Wind Direction vct Deg",
	"FRSRVD":  "FPV WS601 Wx Stn Reserved Chan",
	"FPRECT":  "FPV Precipitation Type",
	"FPRECI":  "FPV Precipitation Intensity mm/h",
	"FDPTMP":  "FPV Dew Point Temp C",
	"FWCTMP":  "FPV Wind Chill Temp C",
	"FPRECD":  "FPV Precipitation Diff mm",
	"FWNDAC":  "FPV Wind Speed Actual m/s",
	"FWNDMN":  "FPV Wind Speed Minimum m/s",
	"FWNDVT":  "FPV Wind Speed Vector m/s",
	"FPVWBT":  "FPV Wet Bulb Temp C",
	"FWDIRA":  "FPV Wind Direction Act Deg",
	"FWDIRN":  "FPV Wind Direction Min Deg",
	"FWDIRX":  "FPV Wind Direction Max Deg",
	"FENTHP":  "FPV Specific Enthalpy kJ/kg",
	"LSBATT":  "LPV DAS Battery Volts",
	"LSTEMP":  "LPV DAS Panel Temp C",
	"LPVDBT":  "LPV Vaisala DryBulb Temp C",
	"LPV_RH":  "LPV Vaisala Relative Humidity %",
	"LPVDB2":  "LPV Vaisala bkup DryBulb Temp C",
	"LPVRH2":  "LPV Vaisala bkup Relative Humidity %",
	"LWINDA":  "LPV Wind Speed Avg m/s",
	"LPAIRR":  "LPV Epp POA Irradiance W/m2",
	"INVACP":  "Inverter AC Power Output (kW)",
	"INVACE":  "Inverter DC Energy Output (kWh)",
	"INVDCI":  "Inverter DC Current (Amps)",
}


if __name__ == '__main__':
  # ents = list(map(lambda x:root/x, root.iterdir()))
  ents = list(root.iterdir())
  # df = pd.read_csv(ents[2])
  df = pd.read_csv(root / 'FPV_Windsor_CA_data.csv', na_values=[32767])

  #    this snippet of code computes the distribution of data. 32767 (see line 12) shows up the most and is an anomaly

  #for col in df.columns:
  #  top,cnt = df[col].value_counts().idxmax(), df[col].value_counts().max()
  #  if cnt > len(df)*.1:
  #    print(f"{col}: {cnt} rows = {top!r}")

  #    plots the thing (just replace the string between the quotes with the param you want e.g. FSBATT)

  #plt.plot(df['NWPTMA'])
  #plt.show()


  # print(df.describe())

  #    spot them sparse outliers that exist other than 32767 for single columns
  Q1 = df['NWPTMA'].quantile(0.25)
  Q3 = df['NWPTMA'].quantile(0.75)
  IQR = Q3 - Q1

  lower, upper = Q1 - 1.5*IQR, Q3 + 1.5*IQR
  outliers = (df['NWPTMA'] < lower) | (df['NWPTMA'] > upper)

  print(df.loc[outliers, 'NWPTMA'])

  #    fancy thing for multivariate outliers (expects 5% outliers)
  iso = IsolationForest(contamination=.005)
  df['anomaly'] = iso.fit_predict(df[column_mapping.keys()])
  outliers = df[df['anomaly'] == -1]

  #    renames the columns into descriptions

  df.rename(columns=column_mapping, inplace=True)

  df.to_csv('formatted.csv', index=False)
