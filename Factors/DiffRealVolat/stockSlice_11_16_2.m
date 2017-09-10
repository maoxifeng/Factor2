% 
% load('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/sdtime.mat')
% timeAmSeries = sdtime(1:7201);
% timePmSeries = sdtime(7202: 14402);
% timePeriod = 60
% amTSUse = [];
% pmTSUse = [];
% % tcount = 0;
% for tcount=1:7201
%     if mod((tcount-1), timePeriod)==0
%         amTSUse = [amTSUse; timeAmSeries(tcount)];
%         pmTSUse = [pmTSUse; timePmSeries(tcount)];
%         a = 0;
%     end
% end
% TSUse = [amTSUse; pmTSUse];
% save TSUse TSUse;



% load date series
% load TSUse
% load('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat');
% 
% dateSeriesUse = dateSeries(dateSeries>20110000, 1);
% timeCell = cell(7, 1);
% for iyear = 2011:2017
% %     yearSmall = iyear * 10^4;
% %     yearBig = (iyear+1) * 10^4;
%     
%     dateYSer = dateSeriesUse((dateSeriesUse>(iyear * 10^4)) & (dateSeriesUse<((iyear+1) * 10^4)), 1);
%     timeYSer = 10^6 * kron(dateYSer, ones(size(TSUse, 1), 1)) + kron(ones(size(dateYSer, 1), 1), TSUse);
%     timeCell(iyear-2010) = {timeYSer};
% end
% 
% save timeSeries, timeCell;


% load date series
% load TSUse
% 
% load('/data/liushuanglong/MyFiles/Data/Factors/HLZ/Time&Code/alltdays_mat.mat');
% 
% dateSeriesUse = dateSeries(dateSeries>20110000, 1);
% dateCell = cell(7, 1);
% for iyear = 2011:2017
% %     yearSmall = iyear * 10^4;
% %     yearBig = (iyear+1) * 10^4;
%     
%     dateYSer = dateSeriesUse((dateSeriesUse>(iyear * 10^4)) & (dateSeriesUse<((iyear+1) * 10^4)), 1);
%     
%     dateCell(iyear-2010) = {dateYSer};
% end
% % 
% save dateSeries, dateCell;

load TSUse
load dateSeries;
load timeSeries;
data_dir = '/data/liushuanglong/MyFiles/Data/'; 
stoCounts = 0;
dateDefTime = TSUse;  % one day default time
for i=[1011,1012]
    
    fprintf([num2str(i), '\n']);
    newDirStr = ['/data/liushuanglong/MyFiles/Data/StockSlice/',num2str(i)];
    mkdir(newDirStr);
    foldernames = dir([data_dir,num2str(i)]);
    nfolder = size(foldernames,1);

    for ifolder = 3:nfolder
        stoCounts =  stoCounts + 1;
        ifolder_str = foldernames(ifolder).name;

        filenames = dir([data_dir,num2str(i),'/',ifolder_str,'/*.mat']);
            
        nf = size(filenames,1);
        newDirStoStr = ['/data/liushuanglong/MyFiles/Data/StockSlice/',num2str(i), '/', ifolder_str, '/'];
        mkdir(newDirStoStr);
        
        if nf ~= 0                    
            for ifile = 1:nf
                fprintf([num2str(stoCounts), '  ', filenames(ifile).name(1:11), '  ']);
                savefile_str = ['/data/liushuanglong/MyFiles/Data/StockSlice/',num2str(i), '/', ifolder_str, '/',filenames(ifile).name];
                if  exist(savefile_str,'file')==2
                    continue;
                end
                iyear = str2double(filenames(ifile).name(1:4));
                iyearnum = mod(iyear, 10);
                
                ifile_str = [data_dir,num2str(i),'/',ifolder_str,'/',filenames(ifile).name];
                
                load(ifile_str);      % load file
                if size(data, 1)==0
                    fprintf('no data\n');
                    continue;
                end
                secData = mod(data(:, 1), 100);
                dataBool = secData(:, 1) <= 60;                
                dataTempMat = data(dataBool, 1:2);            % drop >60s data , keep effective data, two columns                  
                dateTempMat = floor(dataTempMat(:, 1)/10^6); % stock effective date
                dateTempUniMat = unique(dateTempMat);     % stock unique date
                timeSerTemp = timeCell{iyearnum};  % load default day time
                dateSerTemp = dateCell{iyearnum};  % load iyear default date
                
                dataSaveTemp = nan(size(TSUse, 1), size(dateSerTemp, 1));   % for saving used data
                for idate=dateTempUniMat'                    
                    dataUseBool = (dateTempMat(:, 1) == idate);
                    dataUseTemp = dataTempMat(dataUseBool, :);  % select one day data of stock
                    dataUseTemp = sortrows(dataUseTemp, 1);  % sort 
                    dateNumInd = find(dateSerTemp == idate, 1);
                    
                    if size(dataUseTemp, 1)==1  %the date has only one row data 
                        dataSaveTemp(1, dateNumInd) = dataUseTemp(1, 2);
                        fprintf('only one  ');
                        continue;
                    end
                    
                    timeUseTemp = dataUseTemp(:, 1);   % select one day datetime of stock
                    timeUseTemp = mod(timeUseTemp, 10^6);  % select one day time of stock
                    
                    if dateDefTime(1) >= timeUseTemp(1)
                        sindex = 1;
                    else
                        sindex = find(dateDefTime>=timeUseTemp(1), 1);
                    end
                                        
                    itimeSto = 2;
                    for iddate = sindex:242  % default time index
                        Flag = 0;
                        itime=dateDefTime(iddate);    % a used default time
                        timeStoLen = size(timeUseTemp, 1);        % one stock time length

                        for iitimeSto=itimeSto:timeStoLen
                            if timeUseTemp(iitimeSto, 1) > itime
                                dataSaveTemp(iddate, dateNumInd) = dataUseTemp(iitimeSto-1, 2);
                                itimeSto = iitimeSto;
                                break;
                                
                            elseif timeUseTemp(timeStoLen, 1) <= itime
                                dataSaveTemp(iddate:end, dateNumInd) = dataUseTemp(end, 2);
                                Flag = 1;
                                
                                break;
                            end
                        end

                        if Flag == 1
                            break;                                
                        end                                                                                
                    end                    
                end
                
                save(savefile_str, 'dataSaveTemp');      % save file 
                fprintf('Done\n');
            end
        end
    end
end
