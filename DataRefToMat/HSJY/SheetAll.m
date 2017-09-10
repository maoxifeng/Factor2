%  convert table to mat

loadPathMain = '/data/factor_db/AStock_factor_db/mat_data/HSJY/JYDB2/';
savePathMain = '/data/liushuanglong/MyFiles/Data/JYDB2/';
foldNames = dir(loadPathMain);
nnfold = size(foldNames, 1);
for iifold = 3: nnfold
    ifoldName = foldNames(iifold).name;
    fileNames = dir([loadPathMain, ifoldName, '/*.mat']);    
    fprintf([ifoldName, ' start  ']);
    nnfile = size(fileNames, 1);
    for iifile=1:nnfile        
        load([loadPathMain, ifoldName, '/', fileNames(iifile).name]);
        dataStruct = table2struct(data_table, 'ToScalar',true);
        save([savePathMain, ifoldName, '/', fileNames(iifile).name], 'dataStruct');
        fprintf([fileNames(iifile).name, ' saved~\n']);
    end
    
end
    
    
       