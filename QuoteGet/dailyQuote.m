dataPathMain = '/data/factor_db/AStock_factor_db/mat_data/HSJY/JYDB2/QT_DailyQuote/';
savePathMain = '/data/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/';
fileNames = dir([dataPathMain, '*.mat']);
nndata = size(fileNames, 1);
for ii = 1: nndata
    ifileName = fileNames(ii).name;
    load([dataPathMain, ifileName]);
    data = data_table{:, :};
    col = data_table.Properties.VariableNames;
    ind = data_table.Properties.RowNames;
    save([savePathMain, ifileName], 'data', 'col', 'ind');
end



load('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_ClosePrice_170811_array.mat');
save('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_ClosePrice_170811_mat.mat', ...
    'colInnerCode', 'DailyQuote_ClosePrice_170811', 'indexTime');

load('/data/factor_db/AStock_factor_db/mat_data/HSJY/JYDB2/QT_AdjustingFactor/QT_AdjustingFactor.mat')
data = data_table{:, :};
col = data_table.Properties.VariableNames;
ind = data_table.Properties.RowNames;
save('/data/liushuanglong/MyFiles/Data/JYDB2/QT_AdjustingFactor/QT_AdjustingFactor.mat', 'data', 'col', 'ind');