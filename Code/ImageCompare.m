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

%clean previous item
sqlite3.execute('delete from comparated_image;');

%Load images base
h=waitbar(0,'Load images base...');
imgs_base = ImageLoader(imgs_base_from_sql);

%load correlated images
waitbar(0.5,h,'Load correated image..');
imgs_corr = ImageLoader(imgs_corr_from_sql);

cont=1;
%calculate the number of total confront
Nbase = size(imgs_base);
Nbase = Nbase(2);
Ncorr = size(imgs_corr);
Ncorr = Ncorr(2);
numComp =  Ncorr * Nbase;

waitbar(0,h,'Comparing and store into database...');

%compare images
for imgbase=imgs_base
for imgcorr=imgs_corr
    S=0;
    S2=0;
    C=0;
    %Compare face, if there is two equal face in both image then
    %the image are similar otherwise we say NO
    %compare faces
    Nfacebase = size(imgbase.face,2); %number of face in base image
    Nfacecorr = size(imgcorr.face,2); %number of face in correlated image

    %if there are face in both image check if the face are similar
    if Nfacebase>0 && Nfacecorr>0
       is_sim = similarFace(imgbase.face, imgcorr.face);
    else
        %if we can't check the similitude with face we try with
        %correlation and surf on all the image
        %SURF part
        f1 = imgbase.features;
        f2 = imgcorr.features;
        %tune the threshold
        indexPairs = matchFeatures(f1, f2, 'MatchThreshold',0.6) ;

        Stemp = size(indexPairs,1);
        is_sim = 2;

        mf1 = size(f1,1);

        mf2 = size(f2,1);

        S2 = 2*double(Stemp)/double(mf1+mf2);
        S = double(Stemp)/double(min(mf1,mf2));

        %Correlation  part
        img1 = imgbase.image;
        img2 = imgcorr.image;
        img2 = imresize(img2,size(img1));
        C = corr2(img1, img2);
    end

    %visualization and store into database
    perc = double(cont)/double(numComp);
    waitbar(perc,h,'Comparing and store into database...')
    %fprintf('%d of %d', cont, numComp);
    sqlite3.execute('insert into comparated_image values(1,?,?,?,?,?,?,?,?)',imgbase.sql_result.id, imgbase.sql_result.local_path,imgcorr.sql_result.id, imgcorr.sql_result.local_path,S,C,is_sim,S2);
    cont=cont +1;
end
end
sqlite3.close();
clc;
clear;
