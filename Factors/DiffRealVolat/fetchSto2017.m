%% single stock data
load ('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/secuCode.mat');

secuCode = str2num(cell2mat(code(:, 4)));

load TSUse;
dataPathMain = '/data/CompanyDataCenter/';
savePathMain = '/data/liushuanglong/MyFiles/Data/StockSlice/2017/';
defaultfTime = TSUse;

%% one day all stock trading price
for imar=[1011, 1012]
    mkdir([savePathMain, num2str(imar), '/']);
    fileNames = dir([dataPathMain, num2str(imar), '/', '*.mat']);
    ndays = size(fileNames, 1);
    for iday = 1:ndays        
        ifileName = fileNames(iday).name;
        fprintf([ifileName(7:15), '  ']);
        savefileName = [savePathMain, num2str(imar), '/', ifileName];   
        
        if  exist(savefileName,'file')==2
            continue;
        end
        
        load([dataPathMain, num2str(imar), '/', ifileName]);  % load one day data
        idayData = data(:, [2, 9, 33]); % select secucode, price, date, time
        idayData = idayData(mod(idayData(:, 3), 100)<=60, :);
        secuCodeTemp = unique(idayData(:, 1));     
        secuCodeUse = intersect(secuCodeTemp, secuCode);                
        ntime = size(defaultfTime, 1);
        ncode = size(secuCodeUse, 1);
        dataSave = nan(ntime, ncode);  % save data mat
        
        for icode=1:ncode
            
            if mod(icode, 100)==0
                fprintf([num2str(icode), '  ']);  % print code
            end          
            icodeData = idayData(idayData(:, 1)==secuCodeUse(icode, 1), :);
            icodeData = sortrows(icodeData, 3);
            icodeTime = unique(icodeData(:, 3));
                
            if size(icodeData, 1)==1  %the date has only one row data 
                dataSave(1, icode) = icodeData(1, 2);
                fprintf('only one  ');
                continue;
            end
                    
                
            if defaultfTime(1) >= icodeTime(1)
                sindex = 1;
            else
                sindex = find(defaultfTime>=icodeTime(1), 1);
            end

            itimeSto = 2;
            for idtime = sindex:ntime % default time index
                Flag = 0;
                itime=defaultfTime(idtime, 1);    % a used default time
                timeStoLen = size(icodeTime, 1);        % one stock time length

                for iitimeSto=itimeSto:timeStoLen
                    if icodeTime(iitimeSto, 1) > itime
                        dataSave(idtime, icode) = icodeData(iitimeSto-1, 2);
                        itimeSto = iitimeSto;
                        break;

                    elseif icodeTime(timeStoLen, 1) <= itime
                        dataSave(idtime:end, icode) = icodeData(end, 2);
                        Flag = 1;

                        break;
                    end
                end

                if Flag == 1
                    break;                                
                end                                                                                
            end
        end
%         a = 0;
        secuCodeSave = secuCodeUse' ;
        save (savefileName, 'dataSave', 'secuCodeSave') ;      % save file 
        fprintf('Done\n');
    end
end


