load('/data/factor_db/AStock_factor_db/descriptor/common/astock.mat')
data = astock{:, 1:2};
col = astock.Properties.VariableNames(1:2)
save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/astockCode_mat.mat', 'data', 'col')


load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/bond_10y.mat')
data = bond_10y{:, :};
col = bond_10y.Properties.VariableNames;
save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/bond_10y_mat.mat', 'data', 'col') 

