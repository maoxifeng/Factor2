load('/data/factor_db/AStock_factor_db/descriptor/common/header.mat');
dateSer = alltdays{:, 1};
dateSer2017 = dateSer(dateSer>20170000);
save('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/dateSer2017.mat', 'dateSer2017');





