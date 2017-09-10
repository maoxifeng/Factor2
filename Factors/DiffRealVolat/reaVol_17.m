% calculate realized volatility of year 2017

market = [1012, 1011];
dataPathMain = '/data/liushuanglong/MyFiles/Data/StockSlice/2017/';
savePathMain = '/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/YearAllSto_ReaVol/';

% load('/home/liusl/Programm/Matlab/fechData/stockIDCell.mat')
load ('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/secuCode.mat');
allSecuCode = str2num(cell2mat(code(:, 4)));

% load 2017 year trading days
load('/data/factor_db/AStock_factor_db/descriptor/common/header.mat');
dateSer = alltdays{:, 1};
dateSer2017 = dateSer(dateSer>20170000);
nnsto = size(allSecuCode, 1);
nndate = size(dateSer2017, 1);
iyearAllStoVol = nan(nndate, nnsto);
for imar=[1011, 1012]
    
    fileNames = dir([dataPathMain, num2str(imar), '/', '*.mat']);        
    for iidate = 1:nndate                        
        ifileName = fileNames(iidate).name;
%         fprintf([ifileName(7:14), '  ']);
%         idate = ifileName(7:15);        
        load([dataPathMain, num2str(imar), '/', ifileName]);  % load one day data
        stTem = sqrt(250*sum(diff(log(dataSave)).^2, 'omitnan'));
        [men1, men2] = ismember(secuCodeSave, allSecuCode);
        iyearAllStoVol(iidate, men2) = stTem' ;        
    end
end
fprintf('\n');
iyearAllStoVol(iyearAllStoVol==0) = nan ;
SecuCode = allSecuCode';
iyearDateSer = dateSer2017;
save('/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/YearAllSto_ReaVol/2017_DailyVolatility.mat',...
    'iyearAllStoVol', 'SecuCode', 'iyearDateSer')
