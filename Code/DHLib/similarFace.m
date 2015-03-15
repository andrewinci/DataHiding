%return if in two image there are the same face
function is_similar = similarFace(imagestruct1, imagestruct2)
for face1 = imagestruct1
    for face2 = imagestruct2
        f1 = face1.features;
        f2 = face2.features;
        %find common features
        commonfeature = matchFeatures(f1, f2);
        Ncommonfeature = size(commonfeature,1);
        %calculate max SURF
        Nfeature1 = size(f1,1);
        Nfeature2 = size(f2,1);
        rank=double(2*Ncommonfeature)/double(Nfeature1+Nfeature2);
        if rank>=0.5 | corr2(face1.image, face2.image)>0.8
            is_similar=1;
            return
        else
            is_similar=0;
        end
    end
end