% load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_ClosePriceReal_array.mat')

% DailyQuote_ClosePrice_mat = cell2mat(DailyQuote_ClosePrice);
% save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_ClosePriceReal_mat.mat', 'DailyQuote_ClosePriceReal', ...
%     'colInnerCode', 'indexTimeReal')



% DailyQuote_RatioAdjustingFactor_array to _mat
% load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_RatioAdjustingFactor_array.mat')
% save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_RatioAdjustingFactor_mat.mat', ...
%     'RatioAdjustingFactor', 'colInnerCode', 'indexTime')


% convert DailyQuote_AdjClosePrice_array to _mat
% load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_AdjClosePrice_array.mat')
% save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_AdjClosePrice_mat2.mat', ...
%     'DailyQuote_AdjClosePrice', 'colInnerCode', 'indexTime')
% 
% load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_array.mat')
% save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_LogReturn_mat.mat', ...
%     'DailyQuote_LogReturn', 'colInnerCode', 'indexTime')

% load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_AdjClosePriceReal_array.mat')
% save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_AdjClosePriceReal_mat.mat', 'AdjClosePriceReal', ...
%     'colInnerCode', 'indexTimeReal')

% load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TurnoverVolume_array.mat')
% DailyQuote_TurnoverVolume = cell2mat(DailyQuote_ClosePrice);
% save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/DailyQuote/DailyQuote_TurnoverVolume_mat.mat',...
%     'DailyQuote_TurnoverVolume', 'colInnerCode', 'indexTime')

load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_YearDuration_ROE_3Groups_Return_arr.mat')
LC_YearDuration_ROE_3Groups_Return_mat = cell2mat(LC_YearDuration_ROE_3Groups_Return);
save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_YearDuration_ROE_3Groups_Return_mat.mat', ...
    'colItems', 'indexTime', 'LC_YearDuration_ROE_3Groups_Return_mat')


load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/HS300StockCode_arr.mat')
save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/HS300StockCode_mat.mat', 'data', 'col')

load('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_YearDuration_HS300_ROE_3Groups_Return_arr.mat')
LC_YearDuration_HS300_ROE_3Groups_Return_mat = cell2mat(LC_YearDuration_HS300_ROE_3Groups_Return);
save('/home/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/LC_YearDuration_HS300_ROE_3Groups_Return_mat.mat', ...
    'colItems', 'indexTime', 'LC_YearDuration_HS300_ROE_3Groups_Return_mat')


load('/data/factor_db/AStock_factor_db/descriptor/common/astock.mat')



load('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/LC_YearDuration_IA_3Groups_Return_arr.mat')
LC_YearDuration_IA_3Groups_Return_mat = cell2mat(LC_YearDuration_IA_3Groups_Return);
save('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/LC_YearDuration_IA_3Groups_Return_mat.mat', ...
    'colItems', 'indexTime', 'LC_YearDuration_IA_3Groups_Return_mat')



save('/data/liushuanglong/MyFiles/Data/Factors/HLZ/CompanyFundamentalFactors/InvestmentsToAssets/IAExposure_mat.mat', ...
    'beta', 'innerCode', 'timeIndex')






