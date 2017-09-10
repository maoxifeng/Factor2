%% trading days
load('/data/factor_db/AStock_factor_db/descriptor/common/alltdays.mat');
dateSeries = alltdays{:, :};
save('/data/liushuanglong/MyFiles/Data/Common/alltdays.mat', 'dateSeries');


%% code
load('/data/factor_db/AStock_factor_db/descriptor/common/astock.mat');
code = table2cell(astock(:, [1, 2, 5, 3]));
col = astock.Properties.VariableNames([1, 2, 5, 3]);
save('/data/liushuanglong/MyFiles/Data/Common/astock.mat');










