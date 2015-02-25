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
img_base = imread(img_base_path);
img_corr = imread(img_correlated_path);
try
I1 = rgb2gray(img_base);
I2 = rgb2gray(img_corr);
catch err
disp('error for converting image in gray, possibly image are already in gray scale')
end %end try/catch

points1 = detectHarrisFeatures(I1);
points2 = detectHarrisFeatures(I2);

[features1, valid_points1] = extractFeatures(I1, points1);
[features2, valid_points2] = extractFeatures(I2, points2);

indexPairs = matchFeatures(features1, features2);
val = size(indexPairs);
  val = val(1);
if val > 1
disp('base image url')
disp(base_images(i).url);
disp('correlated image url')
disp(correlated_images(j).url);
disp(val);
disp(size(indexPairs))
end

end
end
