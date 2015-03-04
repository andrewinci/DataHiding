//
//  ComparatedImageModel.h
//  ImageSelector
//
//  Created by Darka on 02/03/15.
//  Copyright (c) 2015 Darka. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface DataModel : NSObject
/*
 article_base_id integer,
 img_base_id integer,
 img_base_path text,
 img_corr_id integer,
 img_corr_path text,
 Harris real,
 SURF real,
 correlation real,
 is_similar integer,
 */
-(id) initWithBasePath:(NSString*)imgBasePath CorrPath:(NSString*)imgCorrPath SURFValue:(float) surfValue;


@property (strong) NSString* imageBasePath;
@property (strong) NSString* imageBaseLink;

@property(strong) NSString* imageCorrPath;
@property(strong) NSString* imageCorrLink;

@property float SURF;

@end
