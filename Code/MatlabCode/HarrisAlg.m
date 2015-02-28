function [out] = HarrisAlg(img1, img2)

points1 = detectHarrisFeatures(img1);
points2 = detectHarrisFeatures(img2);

[features1, valid_points1] = extractFeatures(img1, points1);
[features2, valid_points2] = extractFeatures(img2, points2);

indexPairs = matchFeatures(features1, features2);
out = size(indexPairs);
out = out(1);

end

