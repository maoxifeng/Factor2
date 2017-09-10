%  convert new table to mat

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
    
    
       