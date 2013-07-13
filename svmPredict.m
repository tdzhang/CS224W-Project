%% SVM for signed edge prediction
% Written by Haomiao, DEC 3

%load normalized_data.mat
% load dataSampled.mat
% data = dataSampled;
function svmPredict(data)
[m n] = size(data);

trainSize = floor(0.9*m);
xTrain = sparse(data(1:trainSize,1:n-1));
yTrain = data(1:trainSize,n);

xTest = sparse(data(trainSize+1:end,1:n-1));
yTest = data(trainSize+1:end,n);

% Training
model = train(yTrain,xTrain,' -e 0.000001');

% Prediction
[~,acc,~] = predict(yTest,xTest,model);

disp(['Accuracy:' num2str(acc(1))]);