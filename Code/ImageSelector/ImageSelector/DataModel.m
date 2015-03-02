//
//  ComparatedImageModel.m
//  ImageSelector
//
//  Created by Darka on 02/03/15.
//  Copyright (c) 2015 Darka. All rights reserved.
//

#import "DataModel.h"

@implementation DataModel

-(id) initWithBasePath:(NSString*)imgBasePath CorrPath:(NSString*)imgCorrPath SURFValue:(float) surfValue{
    self.SURF = surfValue;
    self.imageBasePath = imgBasePath;
    self.imageCorrPath = imgCorrPath;
    return self;
}

@end

