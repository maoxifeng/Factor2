% common and sheet to convert 

%% conver common sheet to dataStruct
loadPathMain = '/data/factor_db/AStock_factor_db/descriptor/common/';
savePathMain = '/data/liushuanglong/MyFiles/Data/Common/';

fileNames = dir([loadPathMain, '*.mat']);
nnfold = size(fileNames, 1);

for iifold = 1: nnfold
    ifileName = fileNames(iifold).name;    
    fprintf([ifileName, ' start  ']);    
    data = load([loadPathMain, '/', ifileName]);
    tableAtt = whos('-file', [loadPathMain, '/', ifileName]);
    tableName = tableAtt(1).name;
    data_table = data(1).(tableName);
    dataStruct = table2struct(data_table, 'ToScalar',true);
    
    save([savePathMain, '/', ifileName], 'dataStruct');
    fprintf('saved~\n');    
end
    

%%  convert new table to mat

loadPathMain = '/data/factor_db/AStock_factor_db/mat_data/HSJY/JYDB2/';
savePathMain = '/data/liushuanglong/MyFiles/Data/JYDB2/';
foldNames = dir(loadPathMain);
nnfold = size(foldNames, 1);

for iifold = 3: nnfold
    ifoldName = foldNames(iifold).name;
    fileNames = dir([loadPathMain, ifoldName, '/*.mat']);    
    fprintf([ifoldName, ' start  ']);
    nnfile = size(fileNames, 1);
    
    load([loadPathMain, ifoldName, '/', fileNames(nnfile).name]);
    dataStruct = table2struct(data_table, 'ToScalar',true);
    save([savePathMain, ifoldName, '/', fileNames(nnfile).name], 'dataStruct');
    fprintf([fileNames(nnfile).name, ' saved~\n']);
    
end

