function is_similar = commonface(image1, feature1, image2, feature2)
    commonfeature = matchFeatures(feature1, feature2);
    Ncommonfeature = size(commonfeature,1);
    Nfeature1 = size(feature1,1);
    Nfeature2 = size(feature2,1);
    corr2(image1,image2)
    rank=double(2*Ncommonfeature)/double(Nfeature1+Nfeature2)
    if rank>=0.4
        is_similar=1;
    else
        is_similar=0;
    end
end

