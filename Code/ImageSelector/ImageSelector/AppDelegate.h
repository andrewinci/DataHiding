//
//  AppDelegate.h
//  ImageSelector
//
//  Created by Darka on 24/02/15.
//  Copyright (c) 2015 Darka. All rights reserved.
//

#import <Cocoa/Cocoa.h>
#import <sqlite3.h>
#import "DBManager.h"

@interface AppDelegate : NSObject <NSApplicationDelegate>

//controller
@property (strong)DBManager* DataManager;
@property int index;
@property (strong)NSString* mainPath;
-(void)showImage;


//view
@property (weak) IBOutlet NSTextField *LabelImageBase;
@property (weak) IBOutlet NSImageView *ImageBase;
@property (weak) IBOutlet NSTextField *LabelImageCorrelated;
@property (weak) IBOutlet NSImageView *ImageCorrelated;
@property (weak) IBOutlet NSTextField *SURFvalue;

- (IBAction)AllowPressed:(id)sender;
- (IBAction)SkipPressed:(id)sender;
- (IBAction)BackPressed:(id)sender;
- (IBAction)DenyPressed:(id)sender;


@end

