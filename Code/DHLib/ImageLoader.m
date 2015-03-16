function imglist = ImageLoader(list_from_sql)
FDetect = vision.CascadeObjectDetector;
imglist = struct('sql_result',{},'features',{},'image',{}, 'face', {});
cont = 1;

for img=list_from_sql
    try
        tempimage = imread(img.local_path);
        %face detection
        BB = step(FDetect, tempimage);
        Nface=size(BB,1);
        tempimagegray = rgb2gray(tempimage);
        %detect feature foreach face
        cont2=1;
        facelist = struct('image',{},'features',{});
        if Nface>0
            for i = 1:Nface
                %cropping the face
                face = imcrop(tempimagegray,BB(i,:));
                %resize
                face = imresize(face,[56 56]);
                %detect and extract features
                points1 = detectMSERFeatures(face);
                f1 = extractFeatures(face, points1);
                facelist(cont2) = struct('image',face,'features',f1);
                cont2 = cont2+1;
            end
        end

        %Surf
        points1 = detectSURFFeatures(tempimagegray);
        f1 = extractFeatures(tempimagegray, points1);

        imglist(cont) = struct('sql_result',img,'features',f1,'image',tempimagegray, 'face', facelist);
        cont = cont +1;
    catch
    end
end
end