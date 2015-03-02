function [H,S,C] = getParameter(corr)
img_base_path = corr.img_base_path;
img_correlated_path = corr.img_corr_path;
%compare
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
