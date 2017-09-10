%% calculate daily realized volatility 

market = [1011, 1012];
dataPathMain = '/data/liushuanglong/MyFiles/Data/StockSlice/';
savePathMain = '/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/';
stoCounts = 0;

for mar = market
    for year=2011:2016
        mkdir([savePathMain, num2str(mar), '/', num2str(year),'/'])
    end
end

for mar = market
    fprintf([num2str(mar), '\n']);
%     marDirStr = [savePathMain, num2str(mar)];
%     mkdir(marDirStr);   % already maded
    stoFolNames = dir([dataPathMain,num2str(mar)]);
    nstoFol = size(stoFolNames,1);
    
    for iistoFol = 3: nstoFol
        stoCounts = stoCounts + 1;
        istoFolStr = stoFolNames(iistoFol).name;
        istoFilNames = dir([dataPathMain,num2str(mar),'/',  istoFolStr,'/*.mat']);            
        nnstoFil = size(istoFilNames,1);
        
        if nnstoFil ~= 0            
%             inewStoDirStr = [marDirStr, '/', istoFolStr, '/'];  % already maded            
%             mkdir(inewStoDirStr);        
            
            for iistoFil = 1: nnstoFil
                fprintf([num2str(stoCounts), '  ', istoFilNames(iistoFil).name(1:11), '  ']);  % print doing sto id
                iyearStr = istoFilNames(iistoFil).name(1:4);   
                if strcmp(iyearStr, '2017')
                    fprintf('None\n')
                    continue;
                end
                istoSavFilStr = [savePathMain, num2str(mar), '/', iyearStr, '/', istoFilNames(iistoFil).name(1:11), '_DailyRT.mat'];  %                 
                if  exist(istoSavFilStr,'file')==2
                    continue;
                end                
                
                load([dataPathMain, num2str(mar), '/', istoFolStr, '/', istoFilNames(iistoFil).name]);

                dataSave = sqrt(250*sum(diff(log(dataSaveTemp)).^2, 'omitnan'));  %% realized volatility formula
                               
                save(istoSavFilStr, 'dataSave');
                fprintf('Done\n')
                
%                 a = 1;
            end        
        end                                    
    end           
end
%% combine year daily realized volitily 

% market = [1012, 1011];
% dataPathMain = '/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/';
% savePathMain = '/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/YearAllSto_ReaVol/';
% 
% % load('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat');  % load defaulted date
% % dateSeriesUse = dateSeries(dateSeries>20110000, 1);
% 
% % stoCounts = 0;
% % get year stock secuID
% 
% stockIDCell = cell(6, 1);
% for iyear=2011:2016  
%     stoIDTemp = [];
%     for mar = market        
%     %     marDirStr = [savePathMain, num2str(mar)];
%     %     mkdir(marDirStr);   % already maded
%         stoFilNames = dir([dataPathMain,num2str(mar), '/', num2str(iyear), '/', '*.mat']);
%         nnstoFile = size(stoFilNames, 1);
%         stoSecuID = nan(nnstoFile, 1);  % keep secu ID
%         
%         for iistoFile = 1: nnstoFile
%             istoNamStr = stoFilNames(iistoFile).name;
%             istoSecuID = str2num(istoNamStr(6:11));
%             stoSecuID(iistoFile) = istoSecuID;
%             
%         end
%   
%     stoIDTemp = [stoIDTemp; stoSecuID];
%     end
%     stockIDCell(iyear-2010) = {stoIDTemp};
% end
% save('./stockIDCell.mat', 'stockIDCell');
%%


market = [1012, 1011];
dataPathMain = '/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/';
savePathMain = '/data/liushuanglong/MyFiles/Data/StockSlice/DailyRealizedVolatility/YearAllSto_ReaVol/';

load('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat');  % load defaulted date
dateSeriesUse = dateSeries(dateSeries>20110000, 1);

% load('/home/liusl/Programm/Matlab/fechData/stockIDCell.mat')
load ('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/secuCode.mat');
allSecuCode = str2num(cell2mat(code(:, 4)));
for iyear=2011:2016        
    iyearDateSer = dateSeriesUse((dateSeriesUse>(iyear * 10^4)) & (dateSeriesUse<((iyear+1) * 10^4)), 1);
    if exist([savePathMain, num2str(iyear), '_DailyVolatility', '.mat'], 'file') == 2
        continue;        
    end

    iyearAllStoVol = nan(size(iyearDateSer, 1), size(allSecuCode, 1));  % keep iyear all stock data
    for mar = market
        fprintf([num2str(mar), '  ', num2str(iyear), '\n']);
    %     marDirStr = [savePathMain, num2str(mar)];
    %     mkdir(marDirStr);   % already maded
        stoFilNames = dir([dataPathMain,num2str(mar), '/', num2str(iyear), '/', '*.mat']); % read data names
        nnstoFile = size(stoFilNames, 1);        
        for iistoFile = 1: nnstoFile            
            istoFilNamStr = stoFilNames(iistoFile).name;
            load([dataPathMain, num2str(mar), '/', num2str(iyear), '/', istoFilNamStr])
%             a = 0;
            istoSecuID = str2num(istoFilNamStr(6:11));
%             if istoSecuID == 4
%                 a = 0;
%             end
            stoPos = find(allSecuCode==istoSecuID, 1);
            iyearAllStoVol(:, stoPos) = dataSave;                        
                    
        end
    end
    SecuCode = allSecuCode' ;
    iyearAllStoVol(iyearAllStoVol==0) = nan;
    save([savePathMain, num2str(iyear), '_DailyVolatility', '.mat'], 'iyearAllStoVol', 'SecuCode', 'iyearDateSer');
    fprintf('Done\n');
end
