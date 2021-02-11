# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 22:35:04 2021

@author: monsoon season Bill
"""

'''
文档目录
任务1：计算生命周期
  模块1：从CPC分类号中提取属于绿色专利的分类
  模块2：将CPC分类号中绿色专利与1.1、1.2等2digit的class进行匹配
  模块3：匹配PCT的年份数据
  模块4：计算intensity和ubiquity

任务2：计算相关&不相关多样性
'''

'''
任务1：计算生命周期
以下为模块1：从CPC分类号中提取属于绿色专利的分类
'''
#%% cell1: 导入属于绿色专利的CPC分类号的前缀
import pandas as pd;
import xlrd
import numpy as np;
import csv;
import openpyxl;
from openpyxl.workbook import Workbook
from tqdm import tqdm
import math

#4digit指的是CPC分类号中前四位，第一位是字母，第2、3位是数字，第4位是字母
Green_CPC_class_4digit = ['C02F', 'E03F', 'B65F', 'B09B', 'B09C']
#6digit指的是CPC分类号中分号前面的所有（有些是5位，有些是6位）
Green_CPC_class_6digit = ['F02M39', 'F02M41', 'F02M43', 'F02M45', 'F02M47', 'F02M49', 'F02M51', 'F02M53', 'F02M55', 'F02M57', 
                          'F02M59', 'F02M61', 'F02M63', 'F02M65', 'F02M67', 'F02M69', 'F02M71', 'F23J15', 'F23B80', 'F23C9', 
                          'F23C10', 'F02D41', 'F02D43', 'F02D45', 'F02M23', 'F02M25', 'F02M27', 'F02P5', 'B01D46', 'B01D47', 
                          'B01D49', 'B01D50', 'B01D51', 'B03C3', 'F01N3', 'F01N5', 'F01N7', 'F01N13', 'F01N9', 'F01N11', 
                          'B63J4', 'C05F7', 'E01H15', 'B22F8', 'B29B17', 'B62D67', 'B65H73', 'C08J11', 'C10M175', 'C22B7', 
                          'D01G11', 'C05F1', 'C05F5', 'C05F7', 'C05F9', 'C05F17', 'F23G5', 'F23G7', 'A61L11', 'F01N11', 
                          'F01D11', 'E03B322', 'E03B5', 'E03B9', 'E03B11', 'Y02E10', 'Y02E50', 'Y02E20', 'Y02E30', 'Y02E40', 
                          'Y02E60', 'Y02E70', 'Y02C10', 'Y02C20', 'Y02T10', 'Y02T30', 'Y02T50', 'Y02T70', 'Y02T90', 'Y02B10', 
                          'Y02B20', 'Y02B30', 'Y02B40', 'Y02B50', 'Y02B60', 'Y02B70', 'Y02B80', 'Y02B90', 'Y02W10', 'Y02W30', 
                          'Y02W90', 'Y02P10', 'Y02P20', 'Y02P30', 'Y02P40', 'Y02P60', 'Y02P70', 'Y02P80', 'Y02P90']
#8digit指的是CPC分类号中全部位数
#对于出现了and的分类号（实际上只有F17D5/02,F16L55/16,G01M3/08、G01M3/14，G01M3/18，G01M3/22，G01M3/28），对其进行special处理（相当于新提出一个special的list）,后面也单独处理（处理思路在83-85行）
Green_CPC_class_8digit = ['B01D53/34', 'B01D53/343', 'B01D53/346', 'B01D53/38', 'B01D53/40', 'B01D53/42', 'B01D53/44', 
                          'B01D53/46', 'B01D53/48', 'B01D53/485', 'B01D53/50', 'B01D53/501', 'B01D53/502', 'B01D53/504', 
                          'B01D53/505', 'B01D53/505', 'B01D53/507', 'B01D53/508', 'B01D53/52', 'B01D53/523', 'B01D53/526', 
                          'B01D53/54', 'B01D53/56', 'B01D53/565', 'B01D53/58', 'B01D53/60', 'B01D53/62', 'B01D53/64', 
                          'B01D53/66', 'B01D53/68', 'B01D53/685', 'B01D53/70', 'B01D53/72', 'B01J23/38', 'B01J23/40', 
                          'B01J23/42', 'B01J23/44', 'B01J23/46', 'B01J23/462', 'B01J23/464', 'B01J23/466', 'B01J23/468', 
                          'F01M13/02', 'F01M13/021', 'F01M13/022', 'F01M13/023', 'F01M13/025', 'F01M2013/026', 'F01M2013/027', 
                          'F01M13/028', 'F01M13/04', 'F01M13/0405', 'F01M2013/0411', 'F01M13/0416', 'F01M2013/0422', 
                          'F01M2013/0427', 'F01M2013/0433', 'F01M2013/0438', 'F01M2013/0444', 'F01M2013/045', 'F01M2013/0455', 
                          'F01M2013/0461', 'F01M2013/0466', 'F01M2013/0472', 'F01M2013/0477', 'F01M2013/0483', 'F01M2013/0488', 
                          'F01M2013/0494', 'F02B47/08', 'F02B47/10', 'F02D21/06', 'F02D21/08', 'F02D2021/083', 'F02D2021/086', 
                          'F02D21/10', 'F02M3/02', 'F02M3/04', 'F02M3/041', 'F02M3/042', 'F02M3/043', 'F02M3/045', 'F02M3/05', 
                          'F02M3/055', 'F02M31/02', 'F02M31/04', 'F02M31/042', 'F02M31/045', 'F02M31/047', 'F02M31/06', 
                          'F02M31/062', 'F02M31/064', 'F02M31/066', 'F02M31/068', 'F02M31/07', 'F02M31/08', 'F02M31/0805', 
                          'F02M31/082', 'F02M31/0825', 'F02M31/083', 'F02M31/087', 'F02M31/093', 'F02M31/10', 'F02M31/102', 
                          'F02M31/105', 'F02M31/107', 'F02M31/12', 'F02M31/125', 'F02M31/13', 'F02M31/135', 'F02M31/14', 
                          'F02M31/145', 'F02M31/16', 'F02M31/163', 'F02M31/166', 'F02M31/18', 'F02M31/183', 'F02M31/186', 
                          'F23G7/06', 'F27B1/18', 'C21B7/22', 'C21C5/38', 'B01D53/92', 'B01D53/94', 'B01D53/96', 'F02M25/07', 
                          'G01M15/10', 'F02B47/06', 'C10L10/02', 'C10L10/06', 'E02B15/04', 'E02B15/041', 'E02B15/042', 
                          'E02B15/043', 'E02B15/045', 'E02B15/046', 'E02B15/047', 'E02B15/048', 'E02B15/06', 'E02B15/08', 
                          'E02B15/0807', 'E02B15/0814', 'E02B15/0821', 'E02B15/0828', 'E02B15/0835', 'E02B15/0842', 'E02B15/085', 
                          'E02B15/0857', 'E02B15/0864', 'E02B15/0871', 'E02B15/0878', 'E02B15/0885', 'E02B15/0892', 'E02B15/10', 
                          'E02B15/101', 'E02B15/102', 'E02B15/103', 'E02B15/104', 'E02B15/105', 'E02B15/106', 'E02B15/107', 
                          'E02B15/108', 'C09K3/32', 'E03C1/12', 'B63B35/32', 'C09K3/32', 'A43B1/12', 'A43B21/14', 'B03B9/06', 
                          'B29B7/66', 'B30B9/32', 'B65D65/46', 'C03B1/02', 'C03C6/02', 'C03C6/08', 'C04B11/26', 'C04B33/132', 
                          'C09K11/01', 'C22B25/06', 'D21B1/32', 'D21C5/02', 'D21H17/01', 'H01B15/00', 'H01J9/52', 'H01M6/52', 
                          'H01M10/54', 'C10G1/10', 'G08B21/12', 'G08B21/14', 'F16K21/06', 'F16K21/08', 'F16K21/10', 'F16K21/12', 
                          'F16L55/07', 'E03C1/084', 'E03D3/12', 'E03D1/14', 'A47K11/12', 'A47K11/02', 'E03D13/007', 'E03D5/016', 
                          'E03B1/041', 'Y02B40/46', 'Y02B40/56', 'A01G25/02', 'A01G25/06', 'A01G25/16', 'C12N15/8273', 
                          'F17D5/02', 'F16L55/16', 'E03B3/06', 'E03B3/08', 'E03B3/10', 'E03B3/11', 'E03B3/12', 
                          'E03B3/14', 'E03B3/15', 'E03B3/16', 'E03B3/18', 'E03B3/20', 'E03B3/24', 'E03B3/26', 'E03B3/04', 
                          'E03B3/28', 'E03B3/30', 'E03B3/32', 'E03B3/34', 'E03B3/36', 'E03B3/38', 'E03B3/02', 'E03B3/03', 
                          'E03B3/00', 'E03B3/40']

#Green_CPC_class_special_1 = ['F17D5/02','F16L55/16','G01M3/08','G01M3/14','G01M3/18','G01M3/22','G01M3/28']
#Green_CPC_class_special_2 = ['E03']
#备注：special存在的原因在于：只有special1中的某一个和special2中的E03同时出现才能属于绿色专利，这部分的代码放在最后；当然也可以从智慧芽中直接手动提取

#%% cell2：打开全部CPC分类号，总共有4000多万条；部分专利CPC分类号中有空格，要将其去掉
#原本使用replace语句去除空格，但是不知道为什么这里用replace不行，因此换一种方法去空格
CPC_classes = pd.read_csv(r'D:\21挑战杯\202001_CPC_Classes.txt', sep='|')
CPC_classes=CPC_classes.applymap((lambda x:"".join(x.split()) if type(x) is str else x))

#%%cell3：提取每个CPC分类号的前3位、前4位、前6位（斜杠前面的所有位数），前8位（即全部位数）
CPC_classes['CPC_Class_3dig'] = CPC_classes['CPC_Class'].apply(lambda x:x[0:3])
CPC_classes['CPC_Class_4dig'] = CPC_classes['CPC_Class'].apply(lambda x:x[0:4])
CPC_classes['CPC_Class_8dig'] = CPC_classes['CPC_Class']

dig6=CPC_classes.iloc[:,1].tolist()
for i in tqdm(range(0, 41759110)):
    head, sep, tail = dig6[i].partition('/')
    dig6[i]=head
CPC_Class_6dig_1=pd.DataFrame({'CPC_Class_6dig':dig6})

CPC_classes=pd.concat([CPC_classes,CPC_Class_6dig_1],axis=1)
#在数据量比较小的时候可以采用str.split，但是数据量比较大的时候，需要先切成list，然后再跑（上面的写法），这样比DF更快


#%%cell4：用isin判断是否属于一般绿色专利的前缀，并将其全部提取出来,并保存（green_1指的是普通的CPC分类号）
CPC_classes_green_1 = CPC_classes[(CPC_classes['CPC_Class_4dig'].isin(Green_CPC_class_4digit))|(CPC_classes['CPC_Class_6dig'].isin(Green_CPC_class_6digit))|(CPC_classes['CPC_Class_8dig'].isin(Green_CPC_class_8digit))]

CPC_classes_green_1.to_csv(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\202001_CPC_Classes_green_1.txt', sep='|')

#%%cell5：提取special的专利
#对于包含and的处理是这样的，这些“特殊”的专利，如果把其所对应的所有专利号放在同一个单元格内，并用逗号空格分开，那么这个单元格的字符串必定同时包含前面要求的8位和E03
#因此，先把CPC_classes分类号按照id进行groupby，并对同一个id的专利的CPC分类号合并到同一个单元格内
#然后判断这个单元格是否同时包含，然后找出并集，形成CPC_classes_special

def gather(DF):
    return ', '.join(DF.values)
CPC_classes['CPC_Class'].astype(str)
CPC_classes_merge =  CPC_classes.groupby(['appln_id'])['CPC_Class'].apply(gather).reset_index()

#每一个spe就是一种and组合，一共有7种
CPC_classes_spe1 = CPC_classes_merge[(CPC_classes_merge['CPC_Class'].str.contains('F17D5/02')) & (CPC_classes_merge['CPC_Class'].str.contains('E03'))].reset_index()
CPC_classes_spe2 = CPC_classes_merge[(CPC_classes_merge['CPC_Class'].str.contains('F16L55/16')) & (CPC_classes_merge['CPC_Class'].str.contains('E03'))].reset_index()
CPC_classes_spe3 = CPC_classes_merge[(CPC_classes_merge['CPC_Class'].str.contains('G01M3/08')) & (CPC_classes_merge['CPC_Class'].str.contains('E03'))].reset_index()
CPC_classes_spe4 = CPC_classes_merge[(CPC_classes_merge['CPC_Class'].str.contains('G01M3/14')) & (CPC_classes_merge['CPC_Class'].str.contains('E03'))].reset_index()
CPC_classes_spe5 = CPC_classes_merge[(CPC_classes_merge['CPC_Class'].str.contains('G01M3/18')) & (CPC_classes_merge['CPC_Class'].str.contains('E03'))].reset_index()
CPC_classes_spe6 = CPC_classes_merge[(CPC_classes_merge['CPC_Class'].str.contains('G01M3/22')) & (CPC_classes_merge['CPC_Class'].str.contains('E03'))].reset_index()
CPC_classes_spe7 = CPC_classes_merge[(CPC_classes_merge['CPC_Class'].str.contains('G01M3/28')) & (CPC_classes_merge['CPC_Class'].str.contains('E03'))].reset_index()

CPC_classes_spe = pd.concat([CPC_classes_spe1,CPC_classes_spe2,CPC_classes_spe3,CPC_classes_spe4,CPC_classes_spe5,CPC_classes_spe6,CPC_classes_spe7],axis=0)

#先前的gather函数就是将同一个id所有分类号用逗号分隔放在了同一个单元格内，这里需要将其重新分开
CPC_classes_spe = CPC_classes_spe['CPC_Class'].str.split(', ', expand=True).stack().reset_index(level=0).set_index('level_0').rename(columns={0:'CPC_Class'}).join(CPC_classes_spe.drop('CPC_Class', axis=1))

#这部分是把特殊的CPC专利进行merge，找回其value以及前3、4、6、8位数，这样就找到了和CPC_classes_green_1格式一样的df，就可以后续合并
#先前的操作会把原来的index作为一个新的一列，因此要去掉（因为这一列没有任何意义）
CPC_classes_spe.drop(['index'],axis=1,inplace=True)

#这里merge的意义在于，之前的gather操作会将除了appln_id和CPC_Class以外的所有列去掉，因此merge下将其他的列补回来
CPC_classes_spe = pd.merge(CPC_classes_spe,CPC_classes,on=['appln_id','CPC_Class'],how='left')

#这里要换个顺序，appln_id为第一列，CPC——class为第二列，这样才能concat（concat必须保持每列对应）
CPC_classes_spe_applnid = CPC_classes_spe['appln_id']
CPC_classes_spe = CPC_classes_spe.drop('appln_id',axis=1)
CPC_classes_spe.insert(0,'appln_id',CPC_classes_spe_applnid)

#把特殊的CPC分类号保存
CPC_classes_spe.to_csv(r'D:\21挑战杯\生命周期：CPC绿色专利号提取\202001_CPC_Classes_green_spe.txt', sep='|')

#%%cell6：把CPC_classes_special和之前正常提取的CPC_classes_green_1合并，得到所有的greenCPC，并保存
CPC_classes_green = pd.concat([CPC_classes_green_1,CPC_classes_spe],axis=0)
CPC_classes_green = CPC_classes_green.drop_duplicates(subset=['CPC_Class','appln_id'],keep='first')
CPC_classes_green = CPC_classes_green.drop('Unnamed: 0',axis=1)
CPC_classes_green.to_csv(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\202001_CPC_Classes_green.txt', sep='|')


'''
以下为模块2：将CPC分类号中绿色专利与1.1、1.2等2digit的class进行匹配
'''
#%%cell7：读取二位数class，如1.1 1.2 等

CPC_classes_green= pd.read_csv(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\202001_CPC_Classes_green.txt', sep='|')
#“CPC专利号整理”文件的数据格式有两列，一列是1.1、1.2等2dig，一列是CPC分类号（带and的已经处理了）
CPC_green_match_4_example = pd.read_excel(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\CPC专利号整理.xlsx',sheet_name='4位')
CPC_green_match_6_example = pd.read_excel(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\CPC专利号整理.xlsx',sheet_name='6位')
CPC_green_match_8_example = pd.read_excel(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\CPC专利号整理.xlsx',sheet_name='8位')
#%%cell8:对4、6、8位数进行2digit的匹配，并得到合并结果
CPC_classes_green_match = pd.merge(CPC_classes_green,CPC_green_match_4_example,on = 'CPC_Class_4dig',how='left')
CPC_classes_green_match = pd.merge(CPC_classes_green_match,CPC_green_match_6_example,on = 'CPC_Class_6dig',how='left')
CPC_classes_green_match = pd.merge(CPC_classes_green_match,CPC_green_match_8_example,on = 'CPC_Class_8dig',how='left')
#merge函数的一个内置功能为，如果同一个CPC_Class_6dig对应两个不同的2dig(共有两个，C05F7同时属于1.2和1.3，F01N11同时属于1.1和1.5)
#那么merge后会产生两行，把两个2dig的class都包含进去，符合要求
#%%
#检验过发现，每一条专利，在'小数点一位_4'、'小数点一位_6'、'小数点一位_8'中有且只有一个会有1.1、1.2等匹配结果，因此把其他两列没有匹配的空值nan赋值为0，加起来就可以得到每一个CPC分类号对应的2dig
CPC_classes_green_match.fillna(0,inplace=True)
CPC_classes_green_match['2dig_result'] = CPC_classes_green_match['小数点一位_4']+CPC_classes_green_match['小数点一位_6']+CPC_classes_green_match['小数点一位_8']

CPC_classes_green_match.drop_duplicates(subset=['CPC_Class','appln_id','2dig_result','CPC_value'],keep='first',inplace=True)
#为了防止重复算，使用下去函数；在这个subset的筛选条件下，不会出现被错误多删的情况
#删除无法匹配的（无法匹配的因为都是0，加起来也是0）
CPC_classes_green_match = CPC_classes_green_match[CPC_classes_green_match['2dig_result']!=0]

CPC_classes_green_match.drop('Unnamed: 0',axis=1,inplace=True)
#unnamed0 列是由于之前文件保存成txt的时候，将index读取成新的一列，再一次重新打开这个文件的时候，会将这列读取成新的、没有名字的一列
CPC_classes_green_match.to_csv(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\202001_CPC_Classes_green_match.txt',sep='|')


    



#%%

'''
以下为模块3：对于全世界所有的专利，将其打开；利用匹配好的绿色专利的CPC去提取绿色专利，提取标准应该是发明家inv
'''
PCT_Inv_reg = pd.read_csv(r'D:\21挑战杯\202001_PCT_Inv_reg.txt',sep='|')
PCT_Inv_reg_merge = pd.merge(PCT_Inv_reg,CPC_classes_green_match,on='appln_id',how='left')

#提取2dig_result一列非空的为绿色专利，~为取反 
PCT_Inv_reg_green = PCT_Inv_reg_merge[~(pd.isnull(PCT_Inv_reg_merge['2dig_result']))]

#由于PCT_Inv_reg中没有包含prio_year年份的信息，需要利用202001_PCT_IPC文件merge其优先权年份
#202001_PCT_IPC中同一个pct_nbr会有不同的IPC分类号，IPC分类号对我们匹配年份没有用，直接将其去掉（减少数据量），然后去重即可
PCT_IPC = pd.read_csv(r'D:\21挑战杯\202001_PCT_IPC.txt',sep='|')

PCT_IPC.drop('IPC',axis=1,inplace=True)
PCT_IPC.drop_duplicates(subset=['pct_nbr','prio_year','app_year'],keep='first',inplace=True)
#这里去重的意义在于，同一个id的专利会对应有不同的IPC分类号（和CPC相同），去重后不会使匹配好的绿色专利在merge年份中出现重复的情况

#对提取出来的绿色专利merge其年份，并储存——这就是符合格式要求的所有绿色专利；可以算ubiquity和intensity两个指标
PCT_Inv_reg_green_0 = pd.merge(PCT_Inv_reg_green,PCT_IPC,on='pct_nbr',how='left')
#删除无法匹配的
PCT_Inv_reg_green_final = PCT_Inv_reg_green_0[~(pd.isnull(PCT_Inv_reg_green_0['prio_year']))]

PCT_Inv_reg_green_final.to_csv(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\PCT_Inv_reg_green_final_所有绿色专利.txt', sep='|')


#%%

'''
以下为模块4：计算ubiquity和intensity
'''
'''
我们这里要确认使用那些年份！
'''
import pandas as pd;
import xlrd
import numpy as np;
import csv;
import openpyxl;
from openpyxl.workbook import Workbook
from tqdm import tqdm
import math
#读取数据
PCT_Inv_reg_green_final = pd.read_csv(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\PCT_Inv_reg_green_final_所有绿色专利.txt', sep='|')
#需要确定一下使用哪些年份的数据和哪些国家（国家应该出现了就算）
#这里假设先用1991-2018年的数据，后续要改的话可以直接更改（就是后面的data模块也要相应更改）
#ps. 我个人觉得用1991-2017年的数据会比较好，2018年的专利数量出现了一个显著的下滑；另外，1977年-1990年和2019年的绿色专利总量只有两万多，1991-2018年有180万

PCT_Inv_reg_green_run = PCT_Inv_reg_green_final[(PCT_Inv_reg_green_final['prio_year']>1990) & (PCT_Inv_reg_green_final['prio_year']<2019)]

uni_year = PCT_Inv_reg_green_run['prio_year'].unique().tolist()
uni_country = PCT_Inv_reg_green_run['ctry_code'].unique().tolist()
uni_tech2 = PCT_Inv_reg_green_run['2dig_result'].unique().tolist()
#使用unique函数呈现具体有哪些年份、哪些国家、哪些2digit的class


#计算RTA
#先计算patent_cjt（也就是每个国家、每个年份、每个2dig的专利数量）
count_upup = PCT_Inv_reg_green_run.groupby(['prio_year','ctry_code','2dig_result'])['2dig_result'].count()
count_upup = pd.DataFrame({'count_upup':count_upup})
count_upup.reset_index(inplace=True)

#count_updown 指的是RTA计算中分子的分母部分；count_downup指的是RTA计算中分母的分子部分；count_downdown指的是RTA计算中分母的分母部分
count_updown = count_upup.groupby(['prio_year','ctry_code'])['count_upup'].sum()
count_updown = pd.DataFrame({'count_updown':count_updown})
count_updown.reset_index(inplace=True)

count_downup = count_upup.groupby(['prio_year','2dig_result'])['count_upup'].sum()
count_downup = pd.DataFrame({'count_downup':count_downup})
count_downup.reset_index(inplace=True)

count_downdown = count_upup.groupby(['prio_year'])['count_upup'].sum()
count_downdown = pd.DataFrame({'count_downdown':count_downdown})
count_downdown.reset_index(inplace=True)

#汇总得到计算rta所需要的所有指标
down_rta=pd.merge(count_downup,count_downdown, on = 'prio_year')
up_rta=pd.merge(count_upup,count_updown, on=['prio_year','ctry_code'])
rta = pd.merge(up_rta,down_rta,on=['prio_year','2dig_result'])

#RTA的定义进行计算
#需要的是在每一个年份、每一个2dig的专利门类中，RTA>1的国家数量
rta['RTA']=(rta['count_upup']/rta['count_updown'])/(rta['count_downup']/rta['count_downdown'])
rta['RTA_ex']=rta['RTA'].apply(lambda x:1 if x>1 else 0)

ubiq=rta.groupby(['prio_year','2dig_result'])['RTA_ex'].sum()
ubiq=pd.DataFrame({'ubiq':ubiq})
ubiq.reset_index(inplace=True)


#需要得到所有国家的所有技术（没有的用0替代），因此需要依据前面的uni_year uni_tech 进行补全;这个data在后面算intensity的时候也用得到
#28指的是年份（目前设定1991-2018）
#37指的是有37个2dig的分类
data=[]
for i in tqdm(range(0,28)):  
    for j in range(0,37):
            read=[0,0] #ESSENTIAL
            read[0]=uni_year[i]
            read[1]=uni_tech2[j]
            data.append(read)

ubiquity=pd.DataFrame(data,columns=['prio_year','2dig_result'])
ubiquity=pd.merge(ubiquity,ubiq,on = ['prio_year','2dig_result'],how='left')
ubiquity['ubiq'].fillna(0,inplace=True)

std_ubiq=ubiquity.groupby(['prio_year'])['ubiq'].std()
mean_ubiq=ubiquity.groupby(['prio_year'])['ubiq'].mean()
cal=pd.DataFrame({'std':std_ubiq, 'mean':mean_ubiq})
cal.reset_index(inplace=True)

ubiquity=pd.merge(ubiquity,cal,on='prio_year')
ubiquity['std_ubiq']=(ubiquity['ubiq']-ubiquity['mean'])/ubiquity['std']
ubiquity.groupby(['prio_year'])['std_ubiq'].describe()
ubiquity.to_excel(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\UBIQUITY(1991_2018).xlsx',index=False)

#计算intensity
#intensity的定义就是每个年份、每个2dig的技术的专利数量之和（各国求和）
ints=count_upup.groupby(['prio_year','2dig_result'])['count_upup'].sum()
ints=pd.DataFrame({'ints':ints})
ints.reset_index(inplace=True)

intensity=pd.DataFrame(data,columns=['prio_year','2dig_result'])
intensity=pd.merge(intensity,ints,on = ['prio_year','2dig_result'],how='left')
intensity['ints'].fillna(0,inplace=True)

std_ints=intensity.groupby(['prio_year'])['ints'].std()
mean_ints=intensity.groupby(['prio_year'])['ints'].mean()
cal_ints=pd.DataFrame({'std':std_ints, 'mean':mean_ints})
cal_ints.reset_index(inplace=True)

intensity = pd.merge(intensity,cal_ints,on='prio_year')
intensity['std_ints'] = (intensity['ints']-intensity['mean'])/intensity['std']
intensity.groupby(['prio_year'])['std_ints'].describe()
intensity.to_excel(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\INTENSITY(1991_2018).xlsx',index=False)
#%%
lifecycle = pd.concat([ubiquity['prio_year'],ubiquity['2dig_result'],ubiquity['std_ubiq'],intensity['std_ints']],axis=1)
#依据定义给各个阶段赋予名称
lifecycle.loc[(lifecycle['std_ubiq']<0) & (lifecycle['std_ints']<0) , 'stage'] = 'emergence'
lifecycle.loc[(lifecycle['std_ubiq']<0) & (lifecycle['std_ints']>0) , 'stage'] = 'development'
lifecycle.loc[(lifecycle['std_ubiq']>0) & (lifecycle['std_ints']<0) , 'stage'] = 'diffusion'
lifecycle.loc[(lifecycle['std_ubiq']>0) & (lifecycle['std_ints']>0) , 'stage'] = 'maturity'

lifecycle.to_excel(r'D:\21挑战杯\生命周期：CPC绿色专利号提取与PCT绿色专利提取\LIFECYCLE(1991_2018).xlsx',index=False)



#%%
'''
任务2：算相关&不相关多样性
'''
import pandas as pd
import re 
import numpy as np
import math
import openpyxl;
from openpyxl.workbook import Workbook
from tqdm import tqdm
import math

#%%只保留专利的第一作者
patent_china = pd.read_excel(r'D:\21挑战杯\多样性：中国地级市_所有专利数据\匹配结果_原始_无外国等.xlsx')
#这个原始数据是已经去除了无法匹配的、非中国大陆的（港澳台也不属于中国大陆）；保留的只有中国城市的
patent_china_firstauthor = patent_china.drop_duplicates(subset='pct_nbr', keep='first')
#相关多样性和不相关多样性的计算只用第一作者的
patent_china_firstauthor.to_excel(r'D:\21挑战杯\多样性：中国地级市_所有专利数据\匹配结果_保留第一作者.xlsx',index=False)

#%%
patent_china_firstauthor = pd.read_excel(r'D:\21挑战杯\多样性：中国地级市_所有专利数据\地级市匹配结果_无外国等_保留第一作者.xlsx')
PCT_ipc = pd.read_csv(r'D:\21挑战杯\202001_PCT_IPC.txt', sep='|')
patent_matchIPC = pd.merge(patent_china_firstauthor,PCT_ipc,on = 'pct_nbr',  how = 'left')

##%%提取每个专利IPC分类号的前三位、前4位
patent_matchIPC['IPC'] = patent_matchIPC['IPC'].astype(str)
patent_matchIPC['IPC'].str.replace(' ','')
patent_matchIPC['IPC_3digit'] = patent_matchIPC['IPC'].apply(lambda x:x[0:3]).tolist()
patent_matchIPC['IPC_4digit'] = patent_matchIPC['IPC'].apply(lambda x:x[0:4]).tolist()
patent_matchIPC.to_excel(r'D:\21挑战杯\多样性：中国地级市_所有专利数据\地级市匹配结果_无外国等_保留第一作者_IPC.xlsx',index=False)


#%%计算3位数不相关多样性

#三位数熵
pat_dig3 = patent_matchIPC.groupby(['city','prio_year','IPC_3digit'])['IPC_3digit'].count()
pat_dig3 = pd.DataFrame({'count_3':pat_dig3})
pat_dig3.reset_index(inplace=True)

sum3 = patent_matchIPC.groupby(['prio_year','city'])['city'].count()
sum3 = pd.DataFrame({'sum3':sum3})
sum3.reset_index(inplace=True)

dig3 = pd.merge(pat_dig3,sum3, on=['prio_year','city'])
dig3['pf_3'] = dig3['count_3']/dig3['sum3']
dig3['entropy_3'] = dig3['pf_3'].apply(lambda x:x*math.log(1/x))

dig3_V_3 = dig3.groupby(['prio_year','city'])['entropy_3'].sum()
dig3_V_3 = pd.DataFrame({'sum_entropy_3':dig3_V_3})
dig3_V_3.reset_index(inplace=True)


#4位数熵
pat_dig4 = patent_matchIPC.groupby(['city','prio_year','IPC_4digit'])['IPC_4digit'].count()
pat_dig4=pd.DataFrame({'count_4':pat_dig4})
pat_dig4.reset_index(inplace=True)

sum4 = patent_matchIPC.groupby(['prio_year','city'])['city'].count()
sum4 = pd.DataFrame({'sum4':sum4})
sum4.reset_index(inplace=True)

dig4 = pd.merge(pat_dig4,sum4, on=['prio_year','city'])
dig4['pf_4'] = dig4['count_4']/dig4['sum4']
dig4['entropy_4'] = dig4['pf_4'].apply(lambda x:x*math.log(1/x))

dig4_V_4 = dig4.groupby(['prio_year','city'])['entropy_4'].sum()
dig4_V_4 = pd.DataFrame({'sum_entropy_4':dig4_V_4})
dig4_V_4.reset_index(inplace=True)

#8位数熵
pat_dig8 = patent_matchIPC.groupby(['city','prio_year','IPC'])['IPC'].count()
pat_dig8=pd.DataFrame({'count_8':pat_dig8})
pat_dig8.reset_index(inplace=True)

sum8 = patent_matchIPC.groupby(['prio_year','city'])['city'].count()
sum8 = pd.DataFrame({'sum8':sum8})
sum8.reset_index(inplace=True)

dig8 = pd.merge(pat_dig8,sum8, on=['prio_year','city'])
dig8['pf_8'] = dig8['count_8']/dig8['sum8']
dig8['entropy_8'] = dig8['pf_8'].apply(lambda x:x*math.log(1/x))

dig8_V_8 = dig8.groupby(['prio_year','city'])['entropy_8'].sum()
dig8_V_8 = pd.DataFrame({'sum_entropy_8':dig8_V_8})
dig8_V_8.reset_index(inplace=True)

#%%merge后相加减计算UV RV SRV
dig_variety_34 = pd.merge(dig3_V_3,dig4_V_4,on=['prio_year','city'],how='left')
dig_variety_all = pd.merge(dig_variety_34,dig8_V_8,on=['prio_year','city'],how='left')
dig_variety_all['UV'] = dig_variety_all['sum_entropy_3'] 
dig_variety_all['SRV'] = dig_variety_all['sum_entropy_4'] -  dig_variety_all['sum_entropy_3']
dig_variety_all['RV'] = dig_variety_all['sum_entropy_8'] -  dig_variety_all['SRV']
dig_variety_all.to_excel(r'D:\21挑战杯\多样性：中国地级市_所有专利数据\entropy_and_variety.xlsx',index=False)








