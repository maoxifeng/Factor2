%% difference of realized volatility


load('/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/YearAllSto_ReaVol/AllDailyVolatility.mat');
load('/data/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_AdjClosePrice_170811_array.mat');

iiCloseStart = find(indexTime>20110000, 1);

adjClose = DailyQuote_AdjClosePrice_170811(iiCloseStart:end, :);

% formula
difRV = dataRVAll(2:end, :) ./ dataRVAll(1:(end-1), :) - 1 ;  

difClo = adjClose(2:end, :) ./ adjClose(1:(end-1), :) -1 ;

DifRV = difRV ./ difClo ;
%

start = find(~all(isnan(DifRV), 2), 1);
dateSeries = dateSerAll(start+1:end, :);
DifRealVolit = DifRV(start:end, :);

save('/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/YearAllSto_ReaVol/Diff_RealizedVolatility.mat', ...
    'DifRealVolit', 'dateSeries', 'SecuCode') ; 

