function [sliced_price, sliced_volume, tt] = slice_stock_price1(slice_length, standard_time_type, date_list, stock_list)
%%
% date_list = [20160118, 20160427];
% stock_list = [600000, 1011; 000001, 1012];
% sliced_data = slice_stock_price(3, 1, date_list, stock_list);

%%
data_path = 'D:/DataHF/SELF/matData/';
save_path = './';
% slice_length = 3;
if standard_time_type == 1    
    load sdtime;
end
first_time_afternoon = find(sdtime>120000, 1);
slice_time_index = [1:slice_length:first_time_afternoon-1, first_time_afternoon:slice_length:length(sdtime)];
% start_date = 20150708;
% end_date = 20150808;
% date_list = [20150708, 20150808];
% stock_list = [600000, 1011; 000002, 1012];

sd = sdtime(slice_time_index);
nsd = size(sd, 1);


% ifsave = 1;

nd = length(date_list);
ns = size(stock_list, 1);

for j = 1:nd
    sliced_cell = cell(nd, 1);
    for i = 1:ns
            
%         load_file_name = [data_path, num2str(stock_list(i,2)), '/', num2str(date_list(j)), '/', sprintf('%0.6d', stock_list(i, 1)), '.mat'];
%         load(load_file_name);
%
        load data
        
        data(:, 1) = ceil(data(:, 1)/1000);
        
        data(:, 3:4) = cumsum(data(:, 3:4));
%         [utimelist, ia, ic] = unique(data(:,1));
%         data = accumarray(ic, )
        
        sliced_stock = zeros(nsd, 3);
%         nmd = size(data, 1);
        ind0 = find(data(:, 1)<=93000, 1, 'last');
        if isempty(ind0)
            si = find(sd(:, 1)>=data(1,1), 1);
        else
            si = 1;
        end
        % row's index in data
        pind = 1;
        for ist = si:nsd
            ctime = sd(ist);
            tind = find(data(pind:end, 1)<=ctime, 1, 'last');
            if ~isempty(tind)
                cind = tind+pind-1;
            else
                cind = pind;
            end
            sliced_stock(ist, :) = data(cind, 2:4);
            pind = cind;
        end
               
        sliced_stock(2:end,2:3) = diff(sliced_stock(:,2:3));
        sliced_cell(i, 1) = {sliced_stock};
    end
    
    sliced_price = [];
    sliced_volume = [];
    for i = 1:ns
        sliced_price = [sliced_price, sliced_cell{i}(:, 1)];
        sliced_volume = [sliced_volume, sliced_cell{i}(:, 2)];
    end
    sliced_price = [sd, sliced_price];
    sliced_volume = [sd, sliced_volume];
    save([save_path, num2str(date_list(j)), '.mat'], 'sliced_price', 'sliced_volume');
end


t1 = array2table([sliced_price, sliced_volume(:, 2)]);
t1.Properties.VariableNames{1} = 'time';
t2 = array2table(data);
t2.Properties.VariableNames{1} = 'time';
% t2{:, 1} = ceil(t2{:, 1}/1000);
tt = outerjoin(t1, t2);


end
