% conver common sheet to dataStruct
loadPathMain = '/data/factor_db/AStock_factor_db/descriptor/common/';
savePathMain = '/data/liushuanglong/MyFiles/Data/Common/';

fileNames = dir([loadPathMain, '*.mat']);
nnfold = size(fileNames, 1);

for iifold = 1: nnfold
    ifileName = fileNames(iifold).name;    
    fprintf([ifileName, ' start  ']);    
    dataStruct = load([loadPathMain, '/', ifileName]);
    save([savePathMain, '/', ifileName], 'dataStruct');
    fprintf('saved~\n');    
end
    