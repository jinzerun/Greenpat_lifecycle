# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 10:15:53 2021

@author: bill xu
"""

import pandas as pd
import re 
import numpy as np
import math
import openpyxl;
from openpyxl.workbook import Workbook
from tqdm import tqdm
import math

#%%将已经完成地址查询的专利数据，去除重复，只保留第一作者；导入IPC数据；进行merge
import pandas as pd
import re 

patent = pd.read_excel(r'C:\Users\dell\Desktop\所有专利数据\地级市匹配结果_原始_无外国等.xlsx')
#这个原始数据是已经去除了无法匹配的、非中国大陆的
patent_drop = patent.drop_duplicates(subset='pct_nbr', keep='first')
patent_drop.to_excel(r'C:\Users\dell\Desktop\所有专利数据\地级市匹配结果_无外国等_保留第一作者.xlsx',index=False)

PCT_ipc = pd.read_csv(r'C:\Users\dell\Desktop\21挑战杯\202001_PCT_IPC.txt', sep='|')
#从txt文件中读取IPC分类号；原来的PCT_ipc的txt文件里有一个错误，ctrl+F 查询“2006|1999”，有一个分类号的prio_year为2006年，但是app_year写成了9999年；需要进行改正（正巧会对应一条西安的专利信息，如果不改正最后算出来会有“西安-9999年”的值
#这里读取的IPC文件是已经更正后的
patent_matchIPC = pd.merge(patent_drop,PCT_ipc,on = 'pct_nbr',  how = 'left')
#这次merge后同一条专利会连续出现在多行中（由于同一项专利可以对应多个IPC分类号），但是这样对于分组计数会比较方便

#%%提取每条IPC分类号的前3位、前4位和全部（全部就相当于前8位）
import pandas as pd
import re 

patent_matchIPC['IPC'] = patent_matchIPC['IPC'].astype(str)
patent_matchIPC['IPC'].str.replace(' ','')
patent_matchIPC['IPC_3digit'] = patent_matchIPC['IPC'].apply(lambda x:x[0:3]).tolist()
patent_matchIPC['IPC_4digit'] = patent_matchIPC['IPC'].apply(lambda x:x[0:4]).tolist()
patent_matchIPC.to_excel(r'C:\Users\dell\Desktop\所有专利数据\地级市匹配结果_无外国等_保留第一作者_IPC.xlsx',index=False)

#%%计算3、4、8位数的熵
import pandas as pd
import re 
import numpy as np
import math

#三位数熵
pat_dig3 = patent_matchIPC.groupby(['match_final','app_year','IPC_3digit'])['IPC_3digit'].count()
pat_dig3 = pd.DataFrame({'count_3':pat_dig3})
pat_dig3.reset_index(inplace=True)

sum3 = patent_matchIPC.groupby(['app_year','match_final'])['match_final'].count()
sum3 = pd.DataFrame({'sum3':sum3})
sum3.reset_index(inplace=True)

dig3 = pd.merge(pat_dig3,sum3, on=['app_year','match_final'])
dig3['pf_3'] = dig3['count_3']/dig3['sum3']
dig3['entropy_3'] = dig3['pf_3'].apply(lambda x:x*math.log(1/x))

dig3_V_3 = dig3.groupby(['app_year','match_final'])['entropy_3'].sum()
dig3_V_3 = pd.DataFrame({'sum_entropy_3':dig3_V_3})
dig3_V_3.reset_index(inplace=True)


#4位数熵
pat_dig4 = patent_matchIPC.groupby(['match_final','app_year','IPC_4digit'])['IPC_4digit'].count()
pat_dig4=pd.DataFrame({'count_4':pat_dig4})
pat_dig4.reset_index(inplace=True)

sum4 = patent_matchIPC.groupby(['app_year','match_final'])['match_final'].count()
sum4 = pd.DataFrame({'sum4':sum4})
sum4.reset_index(inplace=True)

dig4 = pd.merge(pat_dig4,sum4, on=['app_year','match_final'])
dig4['pf_4'] = dig4['count_4']/dig4['sum4']
dig4['entropy_4'] = dig4['pf_4'].apply(lambda x:x*math.log(1/x))

dig4_V_4 = dig4.groupby(['app_year','match_final'])['entropy_4'].sum()
dig4_V_4 = pd.DataFrame({'sum_entropy_4':dig4_V_4})
dig4_V_4.reset_index(inplace=True)


#8位数熵
pat_dig8 = patent_matchIPC.groupby(['match_final','app_year','IPC'])['IPC'].count()
pat_dig8=pd.DataFrame({'count_8':pat_dig8})
pat_dig8.reset_index(inplace=True)

sum8 = patent_matchIPC.groupby(['app_year','match_final'])['match_final'].count()
sum8 = pd.DataFrame({'sum8':sum8})
sum8.reset_index(inplace=True)

dig8 = pd.merge(pat_dig8,sum8, on=['app_year','match_final'])
dig8['pf_8'] = dig8['count_8']/dig8['sum8']
dig8['entropy_8'] = dig8['pf_8'].apply(lambda x:x*math.log(1/x))

dig8_V_8 = dig8.groupby(['app_year','match_final'])['entropy_8'].sum()
dig8_V_8 = pd.DataFrame({'sum_entropy_8':dig8_V_8})
dig8_V_8.reset_index(inplace=True)


#%%merge后相加减计算UV RV SRV
import pandas as pd
import numpy as np
import math

dig_variety_34 = pd.merge(dig3_V_3,dig4_V_4,on=['app_year','match_final'],how='left')
dig_variety_all = pd.merge(dig_variety_34,dig8_V_8,on=['app_year','match_final'],how='left')
dig_variety_all['UV'] = dig_variety_all['sum_entropy_3'] 
dig_variety_all['SRV'] = dig_variety_all['sum_entropy_4'] -  dig_variety_all['sum_entropy_3']
dig_variety_all['RV'] = dig_variety_all['sum_entropy_8'] -  dig_variety_all['sum_entropy_4']
dig_variety_all.to_excel(r'C:\Users\dell\Desktop\所有专利数据\entropy_and_variety.xlsx',index=False)

