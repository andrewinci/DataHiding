//
//  LinkPath.h
//  ImageSelector
//
//  Created by Darka on 24/02/15.
//  Copyright (c) 2015 Darka. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface LinkPath : NSObject
@property(strong) NSString *Link;
@property(strong) NSString *LocalPath;
@property(strong) NSString *Allowed;

-(id)initWithLink:(NSString*)link Path:(NSString*)localPath andAllowed:(NSString*)allow;
@end
