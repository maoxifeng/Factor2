% ctrl + r , ctrl +t

% load('/home/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/QT_DailyQuote_3000.mat')
% data = data_table{:, :};
% col = data_table.Properties.VariableNames;
% ind = data_table.Properties.RowNames;
% save('/home/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/astock_mat.mat', 'data', 'col', 'ind')
% 
% 
% load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_ClosePrice_array.mat')


% transfort QT_AdjustingFactor to .mat
% load('/home/liushuanglong/MyFiles/Data/JYDB2/QT_AdjustingFactor/QT_AdjustingFactor.mat')
% data = data_table{:, :};
% col = data_table.Properties.VariableNames;
% ind = data_table.Properties.RowNames;
% save('/home/liushuanglong/MyFiles/Data/JYDB2/QT_AdjustingFactor/QT_AdjustingFactor_mat.mat', 'data', 'col', 'ind')


load('/data/factor_db/AStock_factor_db/descriptor/common/alltdays.mat')
data = alltdays{:, :};
save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/alltdays_mat.mat', 'data')