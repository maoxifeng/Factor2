# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import scipy.io as sio

#import pdb
#pdb.set_trace()


# import secuCode
def groupGet():
    
    pathCode = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat'
    dataCodeRaw = sio.loadmat(pathCode)
    dataCodeRaw.keys()
    dataCodeArr = dataCodeRaw['data']
    dataInnerCodeArr = dataCodeArr[:, 0]
    dataComCodeArr = dataCodeArr[:, 1] # 3415
    dataComCodeArr.shape
    dataCodeArr.shape
    # import secuCode
    pathCode = '/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/AStockCode_mat.mat'
    dataCodeRaw = sio.loadmat(pathCode)
    dataCodeRaw.keys()
    dataSecuCodeRaw = dataCodeRaw['secuCode']
    dataSecuCodeRaw.shape
    dataSecuCodeArr = np.array([dataSecuCodeRaw[i][0][0] for i in range(len(dataSecuCodeRaw))])
    
    df1 = pd.DataFrame(dataCodeArr, columns = ['inner', 'com'])
    df2 = pd.DataFrame(dataCodeRaw['data'], columns = ['inner', 'com', 'market'])
    df2['secu'] = dataSecuCodeArr
    df3 = df2[df2['inner'].isin(dataInnerCodeArr)]
    df4 = df3.sort_values('secu')
    
    df_83 = df4[df4['market']==83]
    df_90 = df4[df4['market']==90]
    groDic = {'90': df_90['secu'].values, '83': df_83['secu'].values}
    return df3

data = groupGet()
cc = np.array([['innerCode', 'comCode','market', 'secuCode' ]])
 
# save code 
dataDic = {'col':np.array([['innerCode', 'comCode','market', 'secuCode' ]], dtype=object), 'code':data.values }
sio.savemat('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/secuCode.mat', dataDic)

