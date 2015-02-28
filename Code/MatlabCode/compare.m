%import from database 
addpath ~/Dev/matlab-sqlite3-driver/
sqlite3.open('/Users/darka/Dev/DataHiding/Code/cache/articles.db');
base_images = sqlite3.execute('select * from image where article_id = 0');
articles = sqlite3.execute('select * from article');
correlated_images = sqlite3.execute('select * from image');
texts = sqlite3.execute('select * from body');

base_images_n = size(base_images);
base_images_n = base_images_n(2);

correlated_images_n = size(correlated_images);
correlated_images_n = correlated_images_n(2);

%compare
for i=1:base_images_n
for j=1:correlated_images_n

img_base_path = base_images(i).local_path;
img_correlated_path = correlated_images(j).local_path;
try
img_base = imread(strcat('/Users/darka/Dev/DataHiding/Code/',img_base_path));
img_corr = imread(strcat('/Users/darka/Dev/DataHiding/Code/',img_correlated_path));
img_base_gray = rgb2gray(img_base);
img_corr_gray = rgb2gray(img_corr);
%algorithms
H = HarrisAlg(img_base_gray, img_corr_gray);
S = SURF(img_base_gray, img_corr_gray);
C = Correlation(img_base_gray, img_corr_gray);
disp([H,S,C]);
catch
    disp('error in imread or in algorithms');
end
end
end
