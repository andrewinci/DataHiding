//
//  AppDelegate.h
//  ImageSelector
//
//  Created by Darka on 24/02/15.
//  Copyright (c) 2015 Darka. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import <sqlite3.h>
#import "LinkPath.h"

@interface AppDelegate : NSObject <NSApplicationDelegate>

@property (weak) IBOutlet NSTextField *LinkLabel;
@property (weak) IBOutlet NSImageView *ImageViewer;

- (IBAction)AllowPressed:(id)sender;
- (IBAction)DenyPressed:(id)sender;
- (IBAction)SkipPressed:(id)sender;
- (IBAction)BackPressed:(id)sender;
- (IBAction)AllPressed:(id)sender;

@property (strong) NSMutableArray* linkList;
@property int linkIndex;
@property (strong) NSMutableArray* allowedLink;
@property (strong) NSMutableArray* denyLink;
@property sqlite3 *db;
-(void)showImage;
@end

