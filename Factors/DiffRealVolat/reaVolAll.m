fileNames = dir(['/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/YearAllSto_ReaVol/', '*.mat']);
nnyear = size(fileNames, 1);

dateSerCell = cell(7, 1);
dataRVCell = cell(7, 1);
for iiyear=1:nnyear
    ifileName = fileNames(iiyear).name ;
    load(['/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/YearAllSto_ReaVol/', ifileName]);
    dateSerCell(iiyear) = {iyearDateSer};
    dataRVCell(iiyear) = {iyearAllStoVol};
end

dataRVAll = cell2mat(dataRVCell);
dateSerAll = cell2mat(dateSerCell);

save('/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/YearAllSto_ReaVol/AllDailyVolatility.mat',...
    'dataRVAll', 'dateSerAll', 'SecuCode');


