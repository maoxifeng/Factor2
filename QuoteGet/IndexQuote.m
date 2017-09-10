dataPathMain = '/data/factor_db/AStock_factor_db/mat_data/HSJY/JYDB2/QT_IndexQuote/';
savePathMain = '/data/liushuanglong/MyFiles/Data/JYDB2/QT_IndexQuote/';
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

matlab.engine.shareEngine

