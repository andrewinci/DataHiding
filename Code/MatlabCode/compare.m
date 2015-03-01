%import from database
addpath ~/Dev/matlab-sqlite3-driver/
sqlite3.open('/Users/darka/Dev/DataHiding/Code/cache/articles.db');
corr = sqlite3.execute('select * from comparated_image;');
corr_size = size(corr);
corr_size = corr_size(2);
for i=1:corr_size
  id_base = corr(i).img_base_id;
  id_corr = corr(i).img_corr_id;
  img_base_path = corr(i).img_base_path;
  img_correlated_path = corr(i).img_corr_path;
%compare
try
img_base = imread(strcat('/Users/darka/Dev/DataHiding/Code/',img_base_path));
img_corr = imread(strcat('/Users/darka/Dev/DataHiding/Code/',img_correlated_path));
img_base_gray = rgb2gray(img_base);
img_corr_gray = rgb2gray(img_corr);
%algorithms
%H = HarrisAlg(img_base_gray, img_corr_gray);
H = 0;
S = SURF(img_base_gray, img_corr_gray);
C = Correlation(img_base_gray, img_corr_gray);
clc;
%disp(['processed' i ' relation over' corr_size])
disp(sprintf('processed %d reation over %d',i,corr_size))
disp([H,S,C]);
%save to database
sqlite3.execute('update comparated_image set Harris = ?, SURF = ?, correlation = ?, is_similar = 2 where img_base_id =? and img_corr_id =?;', H, S, C, id_base, id_corr );
catch
    disp('error in imread or in algorithms');
end
end
