%% Data Divider - Large part & Small part
%  Write by Haomiao, DEC 3

%data = csvread('./data/sampleDandR100000with35f');
data = csvread('./data/featuresWithStatus.txt');
%data = csvread('./data/slash_featuresWithStatus.txt');
data = data(:,1:end-2); % Ignore node id column

[m n] = size(data);
nTriangles = sum([data(:,1:4) data(:,13:16)],2);

bound = median(nTriangles);
% Take care of out+ out- in+ in-
ind = data(:,end)==1;
data(ind,27) = data(ind,27) - 1;
% data(ind,28) = data(ind,28) + 0.5;
data(ind,29) = data(ind,29) - 1;
% data(ind,30) = data(ind,30) + 0.5;

ind = data(:,end)==-1;
% data(ind,27) = data(ind,27) + 0.5;
data(ind,28) = data(ind,28) - 1;
% data(ind,29) = data(ind,29) + 0.5;
data(ind,30) = data(ind,30) - 1;
% Normalize
p = [0 4 12 16 24 28 32 34 36 40];
for i = 1:length(p)-1
    d = sum(data(:,p(i)+1:p(i+1)),2);
    d(d == 0) = 1;
    data(:,p(i)+1:p(i+1)) = data(:,p(i)+1:p(i+1)) ./ repmat(d,[1 p(i+1)-p(i)]);
end

% if n > 35
%     data(:,35) = data(:,35) / max(data(:,35));
%     data(:,36) = data(:,36) / max(data(:,36));
% end

%
dataLarge = data(nTriangles>bound,:);
dataSmall = data(nTriangles<=bound, :);

save dataDivided.mat data dataLarge dataSmall