loadPathMain = '/data/factor_db/AStock_factor_db/mat_data/HSJY/JYDB2/QT_DailyQuote/';
savePathMain = '/data/liushuanglong/MyFiles/Data/JYDB2/QT_DailyQuote/';
fileNames = dir([loadPathMain, '*.mat']);

newestfileName = fileNames(end).name;
load([loadPathMain, newestfileName]);
data = data_table{:, :};
col = data_table.Properties.VariableNames;
ind = data_table.Properties.RowNames;
save([savePathMain, newestfileName], 'data', 'col', 'ind');




