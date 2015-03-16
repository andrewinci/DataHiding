FDetect = vision.CascadeObjectDetector;
im1 = imread('~/Downloads/face1.jpg');
im2 = imread('~/Downloads/face2.jpg');

B1 = step(FDetect, im1);
B2 = step(FDetect, im2);


%iterate over all couple of images
for i=1:size(B1,1)
    for j=1:size(B2,1)
        %crop images
        face1 = imcrop(im1, B1(i,:));
        face2 = imcrop(im2, B2(j,:)); 
        
        face1g = rgb2gray(face1);
        face2g = rgb2gray(face2);
        
        face2g = imresize(face2g,size(face1g));
        %dectfeature
        p1 = detectMSERFeatures(face1g);% SURFFeatures(face1g)
        p2 = detectMSERFeatures(face2g);% SURFFeatures(face2g)
        %extract features
        f1 = extractFeatures(face1g, p1);
        f2 = extractFeatures(face2g, p2);

        commonface(face1g,f1,face2g,f2);
        %show images
        subplot(1,2,1), imshow(face1)
        subplot(1,2,2), imshow(face2)
        pause
    end
end
