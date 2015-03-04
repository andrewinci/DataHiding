clc;
currentFolder = pwd;
%add sqlite driver
sqlitedriver = strcat(currentFolder,'/matlab-sqlite3-driver/');
addpath(sqlitedriver)

%load database
dbfile = strcat(currentFolder,'/cache/articles.db');

% NB
% Compiling ALL the sqlite3 because, if not, it won't work :|
% You know... compiling external library...
% sqlite3.make('all');

sqlite3.open(dbfile);
imgs_base_from_sql = sqlite3.execute('select * from image where article_id in (select id from article where is_base = 1);');
imgs_corr_from_sql = sqlite3.execute('select * from image where article_id in (select id from article where is_base = 0);');

disp('load images base');
%load images base
cont = 1;

for img=imgs_base_from_sql
try
tempimage = imread(img.local_path);
tempimagegray = rgb2gray(tempimage);
points1 = detectSURFFeatures(tempimagegray);
[f1, vpts1] = extractFeatures(tempimagegray, points1);

imgs_base(cont) = struct('sql_result',img,'features',f1,'image',tempimagegray);
cont = cont +1;
catch

    end
end


%now all the images and the features are in the imgs_base list

%load correlated images
disp('load correlated images');
cont = 1;
for img=imgs_corr_from_sql
try
tempimage = imread(img.local_path);
tempimagegray = rgb2gray(tempimage);
points1 = detectSURFFeatures(tempimagegray);
[f1, vpts1] = extractFeatures(tempimagegray, points1);

imgs_corr(cont) = struct('sql_result',img,'features',f1, 'image', tempimagegray);
cont = cont +1;
catch
    end
end


%now all the images and the features are in the imgs_corr list

disp('Comparing images');

cont=1;
%calculate the number of total confront
Nbase = size(imgs_base);
Nbase = Nbase(2);
Ncorr = size(imgs_corr);
Ncorr = Ncorr(2);
numComp =  Ncorr * Nbase;

%compare images
for imgbase=imgs_base
for imgcorr=imgs_corr
%SURF part
f1 = imgbase.features;
f2 = imgcorr.features;
indexPairs = matchFeatures(f1, f2);
Stemp = size(indexPairs);
Stemp = Stemp(1);

mf1 = size(f1);
mf1 = mf1(1);

mf2 = size(f2);
mf2 = mf2(1);

S = double(Stemp)/double(min(mf1,mf2));

%correlation part
img1 = imgbase.image;
img2 = imgcorr.image;
img2 = imresize(img2,size(img1));
C = corr2(img1, img2);
clc;
fprintf('%d of %d', cont, numComp);
sqlite3.execute('insert into comparated_image values(1,?,?,?,?,?,?,?)',imgbase.sql_result.id,imgbase.sql_result.local_path,imgcorr.sql_result.id,imgcorr.sql_result.local_path,S,C,2);
cont= cont +1;
end
end
clc;
clear;
exit
