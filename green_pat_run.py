# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 22:54:46 2020

@author: Jzr_07
"""

import pandas as pd;
import xlrd
import numpy as np;
import csv;
import openpyxl;
from openpyxl.workbook import Workbook
from tqdm import tqdm
import math

#%%
#greentech_id
tech_id=pd.read_excel(r'C:\Users\Jzr_07\Desktop\green_pat_ID.xlsx',header=None)
id_demo=[[] for _ in range(250)]
for i in range(0,206):
    a=[]
    a=tech_id[0][i];
    id_demo[i]=a
print(id_demo)

tID=[[] for _ in range(100)]
j=0
for i in range(0,50,2):
    if i<10:tID[j]='A01N65/0'+str(i)
    else: tID[j]='A01N65/'+str(i)
    j=j+1
print(tID)


#%% extract green pat
china_pat=pd.read_csv(r'C:\Users\Jzr_07\Desktop\Evolutionary Geography Workshop\D3-中国专利数据\china_pat_clean.csv')
    
Greenpat_ID=[
'C10L5/00','C10L5/40','C10L5/42','C10L5/44','C10L5/46','C10L5/48','C10B53/02', 'C10L5/40','C10L9/00','C10L1/00','C10L1/02','C10L1/14','C10L1/02','C10L1/19',
'C07C67/00','C07C69/00','C10L1/02','C10L1/19','C11C3/10','C12P7/64','C10L1/02','C10L1/182','C12N9/24','C12P7/06','C12P7/08','C12P7/10','C12P7/12','C12P7/14',
'C02F3/28','C02F11/04','C10L3/00','C12M1/107','C12P5/02','C12N1/13','C12N1/15','C12N1/21','C12N5/10','C12N15/00', 'C10L3/00','F02C3/28','H01M4/86','H01M4/88','H01M4/90','H01M4/92','H01M4/94','H01M4/96','H01M4/98',
'H01M8/00', 'H01M8/02', 'H01M8/04', 'H01M8/06', 'H01M8/08', 'H01M8/10', 'H01M8/12', 'H01M8/14', 'H01M8/16', 'H01M8/18', 'H01M8/20', 'H01M8/22', 'H01M8/24',
'H01M12/00','H01M12/02','H01M12/04','H01M12/08','H01M2/00', 'H01M2/02','H01M2/04', 'C10B53/00', 'F23G7/00','F23G7/10', 
 'C10J3/02','C10J3/46', 'F23B90/00','F23G5/027', 'B09B3/00', 'F23G5/00', 'C21B5/06', 'D21C11/00', 'A62D3/02', 
 'C02F11/04','C02F11/14', 'B09B3/00','F23G5/00',  'E02B9/00','E02B9/02','E02B9/04','E02B9/06','E02B9/08', 'B63H19/02','B63H19/04', 'F03G7/05', 'H02K7/18', 
 'B63B35/00','E04H12/00','B60K16/00', 'B60L8/00', 'B63H13/00', 'H01G 9/20', 'H01L27/142',
 'H01L27/30','H01L51/42','H01L51/44','H01L51/46','H01L51/48', 'H01L25/00','H01L25/03','H01L25/16','H01L25/18','H01L31/042', 'C01B33/02', 'C23C14/14','C23C16/24', 'C30B29/06', 'G05F1/67', 'F21L4/00',
 'F21S9/03', 'H02J7/35', 'H01G9/20','H01M14/00', 'F24D17/00', 'F24D3/00','F24D5/00','F24D11/00','F24D19/00',
 'C02F1/14', 'F02C1/05', 'H02S40/44', 'B60K16/00', 'F03G6/00','F03G6/02','F03G6/04','F03G6/06','E04D13/00','E04D13/18', 'F22B1/00', 'F24V30/00','F25B27/00',
 'F26B3/00','F26B3/28', 'F24S23/00', 'G02B7/183','E24S10/10', 'F24F5/00' , 'H02N 10/00','F25B30/06', 'F03G4/00','F03G4/02','F03G4/04','F03G4/06','F03G7/04',
 'F24V30/00','F24V40/00','F24V40/10','F24V50/00', 'F24D11/02', 'F24D15/04','F24D17/02', 'F24H4/00', 'F25B30/00', 'F01N5/00', 'F02G5/00', 'F02G5/02','F02G5/04',
 'F25B27/02', 'F02C6/18', 'F25B27/02', 'C02F1/16','D21F5/20', 'F22B1/02', 'F23G5/46', 'F24F12/00','F27D17/00', 'F28D17/00','F28D17/04','F28D19/00','F28D19/02','F28D19/04','F28D20/00','F28D17/02','F28D20/02',
 'C10J3/86','F03G5/00','F03G5/02','F03G5/04','F03G5/06','F03G5/08',' B60K6/00','B60K6/20', 'B60W20/00', 
 'F16H3/00', 'F16H3/02', 'F16H3/04', 'F16H3/06', 'F16H3/08', 'F16H3/083', 'F16H3/085', 'F16H3/087', 'F16H3/089', 'F16H3/091','F16H3/093', 'F16H3/095', 'F16H3/097','F16H3/10', 'F16H3/12', 'F16H3/14', 'F16H3/16', 'F16H3/18', 'F16H3/20', 'F16H3/22', 'F16H3/24', 'F16H3/26', 'F16H3/28', 'F16H3/30', 'F16H3/32', 'F16H3/34', 'F16H3/36', 'F16H3/38', 'F16H3/40', 'F16H3/42', 'F16H3/44', 'F16H3/46', 'F16H3/48', 'F16H3/50', 'F16H3/52', 'F16H3/54', 'F16H3/56', 'F16H3/58', 'F16H3/60', 'F16H3/62', 'F16H3/64', 'F16H3/66', 'F16H3/68', 'F16H3/70', 'F16H3/72', 'F16H3/74', 'F16H3/76', 'F16H3/78',
 'F16H48/00', 'F16H48/02', 'F16H48/04', 'F16H48/06', 'F16H48/08', 'F16H48/10', 'F16H48/11', 'F16H48/12', 'F16H48/14', 'F16H48/16', 'F16H48/18', 'F16H48/20', 'F16H48/22', 'F16H48/24', 'F16H48/26','F16H48/27',  'F16H48/28', 'F16H48/285', 'F16H48/29', 'F16H48/295', 'F16H48/30',
 'H02K29/08', 'H02K 49/10', 'B60L7/10',  'B60L7/12', 'B60L7/14', 'B60L7/16', 'B60L7/18', 'B60L7/20', 'B60L7/22', 
 'B6OL8/00','B60L9/00','B60L50/50','B60L50/51','B60L50/52','B60L50/53','B60L50/60','B60L50/61','B60L50/62','B60L50/64','B60L50/70','B60L50/71','B60L50/72','B60L50/75','B60L50/90',
'B60L53/00', 'B60L53/10', 'B60L53/12', 'B60L53/122','B60L53/124','B60L53/126', 'B60L53/14', 'B60L53/16', 'B60L53/18', 'B60L53/20', 'B60L53/22', 'B60L53/24', 'B60L53/30', 'B60L53/302', 'B60L53/31', 'B60L53/34', 'B60L53/35','B60L53/36','B60L53/37', 'B60L53/38', 'B60L53/39', 'B60L53/50', 'B60L53/51', 'B60L53/52', 'B60L53/53' ,'B60L53/54', 'B60L53/55', 'B60L53/56', 'B60L53/57', 'B60L53/60', 'B60L53/62' ,'B60L53/63', 'B60L53/64', 'B60L53/65', 'B60L53/66', 'B60L53/67', 'B60L53/68', 'B60L53/80', 
'B60L55/00','B60L58/00', 'B60L58/10', 'B60L58/12',  'B60L58/13', 'B60L58/14',  'B60L58/15', 'B60L58/16', 'B60L58/18',  'B60L58/19', 'B60L58/20',  'B60L58/21', 'B60L58/22', 'B60L58/24',  'B60L58/25', 'B60L58/26', 'B60L58/27', 'B60L58/30', 'B60L58/31',  'B60L58/32',  'B60L58/33', 'B60L58/34', 'B60L58/40', 'B60L58/38', 'B60L58/40',
'F02B43/00', 'F02M21/02','F02M27/02', 'B60K16/00', 'H02J7/00', 'B62D35/00','B62D35/02', 'B63B1/34','B63B1/36','B63B1/38','B63B1/40',
 'B62M1/00','B62M3/00','B62M5/00','B62M6/00', 'B61D17/02', 'B63H9/00', 'B63H13/00', 'B63H19/02','B62H19/04', 'B63H16/00', 'B63H21/18','B64G1/44', 
 'B60K6/28', 'B60W10/26', 'H01M10/44','H01M10/46', 'H01G11/00', 'B60L3/00', ' C09K5/00', 'F24H7/00', 
 'F28D20/00','F28D20/02', 'F21K99/00', 'F21L4/02', 'H01L51/50', 'H05B33/00', 'E04B1/62','E04B1/88','E04B1/90', 'E04C1/40','E04C1/41', 
 'H01L33/00', 'H01L33/02', 'H01L33/04', 'H01L33/06', 'H01L33/08', 'H01L33/10', 'H01L33/12', 'H01L33/14', 'H01L33/16', 'H01L33/18', 'H01L33/20', 'H01L33/22', 'H01L33/24', 'H01L33/26', 'H01L33/28', 'H01L33/30', 'H01L33/32', 'H01L33/34', 'H01L33/36', 'H01L33/38', 'H01L33/40', 'H01L33/42', 'H01L33/44', 'H01L33/46', 'H01L33/48', 'H01L33/50', 'H01L33/52', 'H01L33/54', 'H01L33/56', 'H01L33/58', 'H01L33/60', 'H01L33/62', 'H01L33/64',
 'E04B1/74', 'E04B1/76', 'E04B1/78', 'E04B1/80','E04C2/284','E04C2/288','E04C2/292','E04C2/296','E06B3/263', 'E04B2/00', 'E04F13/08', 'E04B5/00', 'E04F15/18', 'E04B7/00', 'E04D1/28','E04D3/35','E04D13/16', 'E04B9/00', 'E04F13/08', 'F03G7/08', 
 'B60K6/10','B60K6/30', 'B60L50/30', 'A61L11/00', 'A62D3/00','A62D101/00', 'G21F9/00','B03B9/06', 'D21B1/08','D21B1/32','A43B1/12','A43B21/14', 
  'B22F8/00', 'C09K11/01', 'C11B11/00', 'C14C3/32', 'C21B3/04','C04B7/24', 'C04B7/26', 'C04B7/28', 'C04B7/30','C04B18/04','C04B18/06','C04B18/08','C04B18/10','C11B13/00','C11B13/02','C11B13/04','D01F13/00', 'D01F13/02', 'D01F13/04',
 'C25C1/00', 'B29B17/00','B62D67/00', 'C10G1/10', 'C22B7/00','C22B7/02','C22B7/04','C22B719/30','C22B25/06', 'D01G11/00', 
 'D21C5/02', 'H01J9/50','H01J9/52', 'H01M6/52','H01M10/54', 'B01D53/14','B01D53/22','B01M53/62', 'B65G5/00', 'C01B32/50', 'E21B41/00','E21B43/16', 'E21F17/16', 'F25J3/02', 
 'B01D53/92','F02B75/10', 'C21C5/38', 'C10B21/18', 'F23B80/02','F23C9/00','F23G7/06','FO1N9/00','B03C3/00','C21B7/22','C21C5/38','F27B1/18','F27B15/12', 'C10L10/02','C10L10/06', 'F23J7/00', 'F23J15/00','C09K3/22', 'G08B21/12', 'B63J4/00', 
 'C05F7/00','C09K3/32', 'B63B35/32','E02B15/04', 'E03C1/12', 'G21C13/10','A01G23/00','A01G25/00','C09K17/00', 'E02D3/00', 'E04H1/00','F02C1/05',
 'B01D53/00','B01D53/02', 'B01D53/04', 'B01D53/047','B01D53/053','B01D53/06', 'B01D53/08', 'B01D53/10', 'B01D53/12', 'B01D53/14', 'B01D53/16', 'B01D53/18', 'B01D53/22', 'B01D53/24', 'B01D53/26', 'B01D53/28', 'B01D53/30', 'B01D53/32', 'B01D53/34', 'B01D53/36', 'B01D53/38', 'B01D53/40', 'B01D53/42', 'B01D53/44', 'B01D53/46', 'B01D53/48', 'B01D53/50', 'B01D53/52', 'B01D53/54', 'B01D53/56', 'B01D53/58', 'B01D53/60', 'B01D53/62', 'B01D53/64', 'B01D53/66', 'B01D53/68', 'B01D53/70', 'B01D53/72', 'B01D53/73','B01D53/74', 'B01D53/75','B01D53/76', 'B01D53/77','B01D53/78', 'B01D53/79','B01D53/80', 'B01D53/81','B01D53/82','B01D53/83', 'B01D53/84', 'B01D53/85','B01D53/86', 'B01D53/88', 'B01D53/90', 'B01D53/92', 'B01D53/94', 'B01D53/96', 
 'F01N3/00', 'F01N3/01','F01N3/02', 'F01N3/021','F01N3/022','F01N3/023','F01N3/025','F01N3/027','F01N3/028','F01N3/029','F01N3/031','F01N3/032','F01N3/033','F01N3/035','F01N3/037','F01N3/038','F01N3/04', 'F01N3/05','F01N3/06', 'F01N3/08', 'F01N3/10',  'F01N3/18', 'F01N3/20', 'F01N3/22', 'F01N3/24', 'F01N3/26', 'F01N3/28', 'F01N3/30', 'F01N3/32', 'F01N3/34', 'F01N3/36', 'F01N3/38', 
 'B01D45/00','B01D45/02','B01D45/04','B01D45/06','B01D45/08','B01D45/10','B01D45/12','B01D45/14','B01D45/16','B01D45/18','B01D46/00', 'B01D46/02', 'B01D46/04', 'B01D46/06', 'B01D46/08', 'B01D46/10', 'B01D46/12', 'B01D46/14', 'B01D46/16', 'B01D46/18', 'B01D46/20', 'B01D46/22', 'B01D46/24', 'B01D46/26', 'B01D46/28', 'B01D46/30', 'B01D46/32', 'B01D46/34', 'B01D46/36', 'B01D46/38', 'B01D46/40', 'B01D46/42', 'B01D46/44', 'B01D46/46', 'B01D46/48', 'B01D46/50', 'B01D46/52', 'B01D46/54',
'B01D47/00', 'B01D47/02', 'B01D47/04', 'B01D47/06', 'B01D47/08', 'B01D47/10', 'B01D47/12', 'B01D47/14', 'B01D47/16', 'B01D47/18','B01D49/00', 'B01D49/02', 'B01D50/00', 'B01D51/00', 'B01D51/02', 'B01D51/04', 'B01D51/06', 'B01D51/08', 'B01D51/10',
'A01N25/00', 'A01N25/02', 'A01N25/04', 'A01N25/06', 'A01N25/08', 'A01N25/10', 'A01N25/12', 'A01N25/14', 'A01N25/16', 'A01N25/18', 'A01N25/20', 'A01N25/22', 'A01N25/24', 'A01N25/26', 'A01N25/28', 'A01N25/30', 'A01N25/32', 'A01N25/34',
'A01N27/00','A01N29/00', 'A01N29/02', 'A01N29/04', 'A01N29/06', 'A01N29/08', 'A01N29/10', 'A01N29/12','A01N31/00', 'A01N31/02', 'A01N31/04', 'A01N31/06', 'A01N31/08', 'A01N31/10', 'A01N31/12', 'A01N31/14', 'A01N31/16',
'A01N33/00', 'A01N33/02', 'A01N33/04', 'A01N33/06', 'A01N33/08', 'A01N33/10', 'A01N33/12', 'A01N33/14', 'A01N33/16', 'A01N33/18', 'A01N33/20', 'A01N33/22', 'A01N33/24', 'A01N33/26',
'A01N35/00', 'A01N35/02', 'A01N35/04', 'A01N35/06', 'A01N35/08', 'A01N35/10', 'A01N37/00', 'A01N37/02', 'A01N37/04', 'A01N37/06', 'A01N37/08', 'A01N37/10', 'A01N37/12', 'A01N37/14', 'A01N37/16', 'A01N37/18', 'A01N37/20', 'A01N37/22', 'A01N37/24', 'A01N37/26', 'A01N37/28', 'A01N37/30', 'A01N37/32', 'A01N37/34', 'A01N37/36', 'A01N37/38', 'A01N37/40', 'A01N37/42', 'A01N37/44', 'A01N37/46', 'A01N37/48', 'A01N37/50', 'A01N37/52',
'A01N39/00', 'A01N39/02', 'A01N39/04', 'A01N41/00', 'A01N41/02', 'A01N41/04', 'A01N41/06', 'A01N41/08', 'A01N41/10', 'A01N41/12',
'A01N43/00', 'A01N43/02', 'A01N43/04', 'A01N43/06', 'A01N43/08', 'A01N43/10', 'A01N43/12', 'A01N43/14', 'A01N43/16', 'A01N43/18', 'A01N43/20', 'A01N43/22', 'A01N43/24', 'A01N43/26', 'A01N43/28', 'A01N43/30', 'A01N43/32', 'A01N43/34', 'A01N43/36', 'A01N43/38', 'A01N43/40', 'A01N43/42', 'A01N43/44', 'A01N43/46', 'A01N43/48', 'A01N43/50', 'A01N43/52', 'A01N43/54', 'A01N43/56', 'A01N43/58', 'A01N43/60', 'A01N43/62', 'A01N43/64', 'A01N43/647', 'A01N43/653', 'A01N43/66', 'A01N43/68', 'A01N43/70','A01N43/707','A01N43/713', 'A01N43/72', 'A01N43/74', 'A01N43/76', 'A01N43/78', 'A01N43/80', 'A01N43/82','A01N43/824','A01N43/828', 'A01N43/832','A01N43/836','A01N43/84', 'A01N43/86', 'A01N43/88', 'A01N43/90', 'A01N43/92',
'A01N45/00', 'A01N45/02','A01N47/00', 'A01N47/02', 'A01N47/04', 'A01N47/06', 'A01N47/08', 'A01N47/10', 'A01N47/12', 'A01N47/14', 'A01N47/16', 'A01N47/18', 'A01N47/20', 'A01N47/22', 'A01N47/24', 'A01N47/26', 'A01N47/28', 'A01N47/30', 'A01N47/32', 'A01N47/34', 'A01N47/36', 'A01N47/38', 'A01N47/40', 'A01N47/42', 'A01N47/44', 'A01N47/46', 'A01N47/48', 'A01N47/50', 'A01N47/52', 'A01N47/54', 'A01N47/56', 'A01N47/58', 'A01N47/60', 'A01N47/62', 'A01N47/64', 'A01N47/66', 'A01N47/68', 'A01N47/70', 'A01N47/72', 'A01N47/74', 'A01N47/76', 'A01N47/78', 'A01N47/80', 'A01N47/82', 'A01N47/84', 'A01N47/86', 'A01N47/88', 'A01N47/90', 'A01N47/92',
'A01N49/00','A01N51/00','A01N53/00', 'A01N53/02', 'A01N53/04', 'A01N53/06', 'A01N53/08', 'A01N53/10', 'A01N53/12', 'A01N53/14','A01N55/00', 'A01N55/02', 'A01N55/04', 'A01N55/06', 'A01N55/08', 'A01N55/10',
'A01N57/00', 'A01N57/02', 'A01N57/04', 'A01N57/06', 'A01N57/08', 'A01N57/10', 'A01N57/12', 'A01N57/14', 'A01N57/16', 'A01N57/18', 'A01N57/20', 'A01N57/22', 'A01N57/24', 'A01N57/26', 'A01N57/28', 'A01N57/30', 'A01N57/32', 'A01N57/34', 'A01N57/36',
'A01N59/00', 'A01N59/02', 'A01N59/04', 'A01N59/06', 'A01N59/08', 'A01N59/10', 'A01N59/12', 'A01N59/14', 'A01N59/16', 'A01N59/18', 'A01N59/20', 'A01N59/22', 'A01N59/24', 'A01N59/26', 
'A01N61/00', 'A01N61/02','A01N63/00', 'A01N63/02', 'A01N63/04', 'A01N63/10', 'A01N63/12', 'A01N63/14', 'A01N63/16', 'A01N63/20', 'A01N63/22', 'A01N63/23', 'A01N63/25', 'A01N63/27',  'A01N63/28','A01N63/30', 'A01N63/32', 'A01N63/34', 'A01N63/36', 'A01N63/38', 'A01N63/40', 'A01N63/50', 'A01N63/60',
'A01N65/00', 'A01N65/03', 'A01N65/04', 'A01N65/06', 'A01N65/08', 'A01N65/10', 'A01N65/12', 'A01N65/14', 'A01N65/16', 'A01N65/18', 'A01N65/20', 'A01N65/22', 'A01N65/24', 'A01N65/26', 'A01N65/28', 'A01N65/30', 'A01N65/32', 'A01N65/34', 'A01N65/36', 'A01N65/38', 'A01N65/40', 'A01N65/42', 'A01N65/44', 'A01N65/46', 'A01N65/48',
'C08J11/00','C08J11/02','C08J11/04','C08J11/06','C08J11/08','C08J11/10','C08J11/12','C08J11/','C08J11/14','C08J11/16','C08J11/18','C08J11/20','C08J11/22','C08J11/24','C08J11/26','C08J11/28',
'H01L31/00','H01L31/0203','H01L31/0224','H01L31/0232','H01L31/0236','H01L31/024','H01L31/0248','H01L31/0256','H01L31/0264','H01L31/0272','H01L31/028','H01L31/0288','H01L31/0296',
'H01L31/0304','H01L31/0312','H01L31/032','H01L31/0328','H01L31/0336','H01L31/0352','H01L31/036','H01L31/0368','H01L31/0376','H01L31/0384','H01L31/0392',
'H01L31/04','H01L31/041','H01L31/042','H01L31/043','H01L31/044','H01L31/0443','H01L31/0445','H01L31/046','H01L31/0463','H01L31/0465','H01L31/0468',
'H01L31/047','H01L31/0475','H01L31/048','H01L31/049','H01L31/05','H01L31/052','H01L31/0525','H01L31/053','H01L31/054','H01L31/055','H01L31/056',
'H01L31/06','H01L31/061','H01L31/062','H01L31/065','H01L31/068','H01L31/0687','H01L31/0693','H01L31/07','H01L31/072','H01L31/0725','H01L31/073','H01L31/0735','H01L31/074','H01L31/0745','H01L31/0747','H01L31/0749','H01L31/075','H01L31/076','H01L31/077','H01L31/078',
]

Greenpat_ID_ex=[
'C10G','A01H','C10J','F24T','B09B','F03D','F03B','F03C','F24S','H02S','F01K','B62K','B61B','B61C','B61D','B61F','B61G','B61H','B61J','B61K','B61L','H02J','G01R','B65F','B09C','G06Q','G08G','G21B','G21C','G21D','G21F','G21G','G21H','G21J','G21K','F23G','EO3F','CO5F','C02F'
]

for i in range(0,1048):
    x=Greenpat_ID[i].replace(' ','')           
    Greenpat_ID[i]=x

#combine_dataframe_to_excel                  
gpatID=pd.concat([pd.DataFrame({'id':Greenpat_ID}),pd.DataFrame({'id_ex':Greenpat_ID_ex})],axis=1)
gpatID.to_excel(r'C:\Users\Jzr_07\Desktop\greenpat_id.xlsx',index=False)

#extract_green_pat
cont1=0
for i in range(0,china_pat.iloc[:,0].size):
    if china_pat.iloc[i,11] in Greenpat_ID:
        cont1=cont1+1;
print(cont1)

cont2=0
for i in range(0,china_pat.iloc[:,0].size):
    test=china_pat.iloc[i,11][0:4]
    if test in Greenpat_ID_ex:
        cont2=cont2+1;
print(cont2)

y=pd.DataFrame({'id':Greenpat_ID})
yy=pd.DataFrame(y['id'].apply(lambda x:x[0:4]).tolist())
rep=yy[yy[0].isin(Greenpat_ID_ex)]

x=china_pat['X2'].apply(lambda x:x[0:4]).tolist()
china_pat_ex=pd.concat([china_pat,pd.DataFrame({'dig4':x})],axis=1)
Gpat=china_pat_ex[(china_pat_ex['X2'].isin(Greenpat_ID))| (china_pat_ex['dig4'].isin(Greenpat_ID_ex))]

Gpat.to_csv(r'C:\Users\Jzr_07\Desktop\green_pat.csv',index=False)

#%%
gpat=pd.read_csv(r'C:\Users\Jzr_07\Desktop\green_pat.csv')
gpat_head=gpat.head(100)

#DEF_green_pat

green_pat = pd.concat ( [gpat['V1'], gpat['V4'],gpat['V9'], gpat['V18'],gpat['apdate'], gpat['pro'],gpat['city'], gpat['county'],gpat['address'], gpat['X2'],gpat['dig4'], gpat['X3'] ], axis=1 )
green_pat.rename (columns = {'apdate' : 'year', 'X2' : 'dig8'}, inplace=True)
col_name=green_pat.columns.values.tolist()
green_pat_head = green_pat.head(100)


#SAMPLE

gpat_2006=green_pat[green_pat['year']==2006]
for i in range(0, 6384): 
    head, sep, tail = gpat_2006.iloc[i,9].partition('(')
    if sep=='(': print(i)
    gpat_2006.iloc[i,9]= head
gpat_2016=green_pat[green_pat['year']==2016]
for i in range(0,98237): 
    head, sep, tail = gpat_2016.iloc[i,9].partition('(')
    gpat_2016.iloc[i,9]= head


#delete_(2006.01)I

for i in tqdm(range(0, 608726)):
    head, sep, tail = green_pat.iloc[i,9].partition('（') #注意括号是中文的
    green_pat.iloc[i,9]= head    

dig8=green_pat.iloc[:,9].tolist() #上一段直接用dataframe做很伤时间，要切成list

for i in tqdm(range(0, 608726)):
    head, sep, tail = dig8[i].partition('（')
    dig8[i]= head
digit_8=pd.DataFrame({'digit_8':dig8})

green_pat=pd.concat([green_pat,digit_8],axis=1)

uni_id = green_pat['digit_8'].unique().tolist()
uni_id_or=green_pat['dig8'].unique().tolist()

green_pat.to_csv(r'C:/Users/Jzr_07/Desktop/green_pat_0925.csv',index=False)

#pat_code

gpat=pd.read_csv(r'C:/Users/Jzr_07/Desktop/green_pat_0925.csv')
col_name=gpat.columns.values.tolist()
gpat_head=gpat.head(100)

gpat.rename(columns={'dig4':'digit_4'},inplace=True)

digit_3=gpat['digit_8'].apply(lambda x:x[0:3]).tolist()

gpat=pd.concat([gpat,pd.DataFrame({'digit_3': digit_3})],axis=1)

uni_id_8 = gpat['digit_8'].unique().tolist()
uni_id_4 = gpat['digit_4'].unique().tolist()
uni_id_3 = gpat['digit_3'].unique().tolist()

gpat.to_csv(r'C:/Users/Jzr_07/Desktop/green_pat_0925.csv',index= False)

#%% calculate_life_cycle
gpat = pd.read_csv(r'C:/Users/Jzr_07/Desktop/green_pat_0925.csv')

gpat_run=gpat[(gpat['year']>1997) & (gpat['year']<2018)]
uni_year=gpat_run['year'].unique().tolist()
uni_city=gpat_run['city'].unique().tolist()
uni_tech=gpat_run['digit_3'].unique().tolist()


#calculate rta
c_down=gpat_run.groupby(['year','pro','city'])['count'].sum()
c_down=pd.DataFrame({'c_down':c_down})
c_down.reset_index(inplace=True)

n_up=gpat_run.groupby(['year','digit_3'])['count'].sum()
n_up=pd.DataFrame({'n_up':n_up})
n_up.reset_index(inplace=True)

n_down=gpat_run.groupby(['year'])['count'].sum()
n_down=pd.DataFrame({'n_down':n_down})
n_down.reset_index(inplace=True)

n_rta=pd.merge(n_up,n_down, on = 'year')

rta_a=pd.merge(gpat_run,c_down,on = ['year','pro','city'])
rta_b=pd.merge(gpat,n_rta, on=['year','digit_3'])
rta=pd.merge(rta_a,rta_b, on=['year','pro','city','digit_3','count'])

rta['RTA']=(rta['count']/rta['c_down'])/(rta['n_up']/rta['n_down'])
rta['RTA_ex']=rta['RTA'].apply(lambda x:1 if x>1 else 0)


ubiq=rta.groupby(['year','digit_3'])['RTA_ex'].sum()
ubiq=pd.DataFrame({'ubiq':ubiq})
ubiq.reset_index(inplace=True)

data=[]
for i in tqdm(range(0,20)):  
    for j in range(0,58):
            read=[0,0] #ESSENTIAL
            read[0]=uni_year[i]
            read[1]=uni_tech[j]
            data.append(read)
ubiquity=pd.DataFrame(data,columns=['year','digit_3'])
ubiquity=pd.merge(ubiquity,ubiq, how='outer',on = ['year','digit_3'])
ubiquity['ubiq'].fillna(0,inplace=True)

std=ubiquity.groupby(['year'])['ubiq'].std()
mean=ubiquity.groupby(['year'])['ubiq'].mean()
cal=pd.DataFrame({'std':std, 'mean':mean})
cal.reset_index(inplace=True)
ubiquity=pd.merge(ubiquity,cal,on='year')
ubiquity['Std_ubiq']=(ubiquity['ubiq']-ubiquity['mean'])/ubiquity['std']
ubiquity.groupby(['year'])['Std_ubiq'].describe()
ubiquity.to_excel(r'C:\Users\Jzr_07\Desktop\UBIQUITY.xlsx',index=False)

ints=gpat_run.groupby(['year','digit_3'])['count'].sum()
intensity=pd.merge(pd.DataFrame(data,columns=['year','digit_3']),ints,how='outer',on=['year','digit_3'])
intensity.fillna(0,inplace=True)


std_1=intensity.groupby(['year'])['count'].std()
mean_1=intensity.groupby(['year'])['count'].mean()
cal_1=pd.DataFrame({'std':std_1,'mean':mean_1})
cal_1.reset_index(inplace=True)

intensity=pd.merge(intensity,cal_1,on = ['year'])
intensity['Std_ints']=(intensity['count']-intensity['mean'])/intensity['std']
intensity.groupby(['year'])['Std_ints'].describe()
intensity.to_excel(r'C:\Users\Jzr_07\Desktop\INTENSITY.xlsx',index=False)

Life_cycle=pd.concat([ubiquity['year'],ubiquity['digit_3'],ubiquity['Std_ubiq'],intensity['Std_ints']],axis=1)

Life_cycle.to_excel(r'C:\Users\Jzr_07\Desktop\LIFE_CYCLE.xlsx',index=False)


#%% cal Unrelated Variaty


uni_city=china_pat['city'].unique().tolist()
uni_pro=china_pat['pro'].unique().tolist()
uni_year=china_pat['year'].unique().tolist()

pat_run=china_pat[(china_pat['year']>1997) & (china_pat['year']<2018)]
uni_city=pat_run['city'].unique().tolist()
uni_pro=pat_run['pro'].unique().tolist()
uni_year=pat_run['year'].unique().tolist()

uni_dig8=pat_run['digit_8'].unique().tolist()
uni_dig4=pat_run['digit_4'].unique().tolist()
uni_dig3=pat_run['digit_3'].unique().tolist()


pat_dig3=pat_run.groupby(['year','pro','city','digit_3'])['digit_3'].count()
pat_dig3=pd.DataFrame({'count':pat_dig3})
pat_dig3.reset_index(inplace=True)

sum3=pat_run.groupby(['year','pro','city'])['city'].count()
sum3=pd.DataFrame({'sum3':sum3})
sum3.reset_index(inplace=True)

dig3=pd.merge(pat_dig3,sum3, on=['year','pro','city'])
dig3['pf']=dig3['count']/dig3['sum3']
dig3['entropy']=dig3['pf'].apply(lambda x:x*math.log(1/x))
