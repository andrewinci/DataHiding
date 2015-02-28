function [ out ] = Correlation( img1, img2 )
img2 = imresize(img2,size(img1));
out = corr2(img1, img2);
end

