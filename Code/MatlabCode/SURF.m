function [ out ] = SURF(img1, img2)
out = 0;

points1 = detectSURFFeatures(img1);
points2 = detectSURFFeatures(img2);

[f1, vpts1] = extractFeatures(img1, points1);
[f2, vpts2] = extractFeatures(img2, points2);

indexPairs = matchFeatures(f1, f2) ;
out = size(indexPairs);
out = out(1);
%{
val = size(indexPairs);
  val = val(1);
if val > 1
 out = 1;
end
%}
end

