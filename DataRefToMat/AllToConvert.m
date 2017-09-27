% common and sheet to convert 

saveMain = '/data/liushuanglong/'

%% conver common sheet to dataStruct
loadPathMain = '/data/factor_db/AStock_factor_db/descriptor/common/';
savePathMain = [saveMain, '/Data/Common/'];
if ~exist(savePathMain)
    mkdir(savePathMain);
end

fileNames = dir([loadPathMain, '*.mat']);% n * 5 struct 
nnfold = size(fileNames, 1);

for iifold = 1: nnfold
    ifileName = fileNames(iifold).name;    
    fprintf([ifileName, ' start  ']);    
    data = load([loadPathMain, '/', ifileName]); % table format would be convert to 1*1 construct with 1 field: the name of the table
    tableAtt = whos('-file', [loadPathMain, '/', ifileName]); % 1* 1 struct, get the attibute of the file, including name
    tableName = tableAtt(1).name;  %fetch the name of the mat  
    data_table = data(1).(tableName) ; % load the table format of the .mat
    dataStruct = table2struct(data_table, 'ToScalar',true); % convert the table format to 1*1 struct for python loading, the header of table will be converted to the name att of the struct 
    
    save([savePathMain, '/', ifileName], 'dataStruct');
    fprintf('saved~\n');    
end
    

%%  convert QT sheet to dataStruct
loadPathMain = '/data/factor_db/AStock_factor_db/mat_data/HSJY/JYDB2/';
savePathMain = [saveMain, '/Data/JYDB2/'];
if ~exist(savePathMain)
    mkdir(savePathMain);
end
foldNames = dir(loadPathMain);
nnfold = size(foldNames, 1);

for iifold = 3: nnfold
    ifoldName = foldNames(iifold).name;
    isaveFoldName = [savePathMain, ifoldName];
    fileNames = dir([loadPathMain, ifoldName, '/*.mat']);    
    fprintf([ifoldName, ' start  ']);
    nnfile = size(fileNames, 1);
    if exist(isaveFoldName)
        load([loadPathMain, ifoldName, '/', fileNames(nnfile).name]);
        dataStruct = table2struct(data_table, 'ToScalar',true);
        save([isaveFoldName, '/', fileNames(nnfile).name], 'dataStruct');
        fprintf([fileNames(nnfile).name, ' saved~\n']);
    else 
        mkdir(isaveFoldName);
        for iifile=1:nnfile 
            load([loadPathMain, ifoldName, '/', fileNames(iifile).name]);
            dataStruct = table2struct(data_table, 'ToScalar',true);
            save([isaveFoldName, '/', fileNames(iifile).name], 'dataStruct');
            fprintf([fileNames(iifile).name, ' saved~\n']);
        end
    end
    
end

