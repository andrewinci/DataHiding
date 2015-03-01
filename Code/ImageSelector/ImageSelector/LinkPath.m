//
//  LinkPath.m
//  ImageSelector
//
//  Created by Darka on 24/02/15.
//  Copyright (c) 2015 Darka. All rights reserved.
//

#import "LinkPath.h"

@implementation LinkPath
@synthesize Link;
@synthesize LocalPath;
@synthesize Allowed;

-(id)initWithLink:(NSString*)link Path:(NSString*)localPath andAllowed:(NSString*)allow{
    Link = link;
    LocalPath = localPath;
    Allowed = allow;
    return self;
}

@end
