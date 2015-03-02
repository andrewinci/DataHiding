//
//  AppDelegate.m
//  ImageSelector
//
//  Created by Darka on 24/02/15.
//  Copyright (c) 2015 Darka. All rights reserved.
//

#import "AppDelegate.h"

@interface AppDelegate ()

@property (weak) IBOutlet NSWindow *window;
@end

@implementation AppDelegate

@synthesize DataManager;
@synthesize index;

-(NSString*)select_db{
    NSString *db_filename = @"provadb.db";
    // Create the File Open Dialog class.
    NSOpenPanel* openDlg = [NSOpenPanel openPanel];
    
    // Enable the selection of files in the dialog.
    [openDlg setCanChooseFiles:YES];
    
    // Multiple files not allowed
    [openDlg setAllowsMultipleSelection:NO];
    
    // Can't select a directory
    [openDlg setCanChooseDirectories:NO];
    
    [openDlg setTitle:@"Choose your db"];
    // Display the dialog. If the OK button was pressed,
    // process the files.
    if ( [openDlg runModalForDirectory:nil file:nil] == NSOKButton )
    {
        // Get an array containing the full filenames of all
        // files and directories selected.
        NSArray* files = [openDlg filenames];
        
        db_filename = [files objectAtIndex:0];
        
    }
    return db_filename;
}

- (void)applicationDidFinishLaunching:(NSNotification *)Notification {
    //Select Database
    NSString * db_filename = [self select_db];
    DataManager = [[DBManager alloc] initWithDatabaseName:db_filename];
    index = 0;
    [self showImage];
}

- (void)applicationWillTerminate:(NSNotification *)aNotification {
    [DataManager closeDB];
}


-(void)showImage{
    //show base image
    DataModel *el = [DataManager DataList][index];
    NSString *imgBasepath = [NSString stringWithFormat:@"%@%@",@"/Users/darka/Dev/DataHiding/Code/",el.imageBasePath];
    NSImage *imageBase = [[NSImage alloc] initByReferencingFile:imgBasepath];
    [self.ImageBase setImage:imageBase];
    
    //show correlated image
    NSString *imgCorrpath = [NSString stringWithFormat:@"%@%@",@"/Users/darka/Dev/DataHiding/Code/",el.imageCorrPath];
    NSImage *imageCorr = [[NSImage alloc] initByReferencingFile:imgCorrpath];
    [self.ImageCorrelated setImage:imageCorr];
    
    //show SURF value
    [self.SURFvalue setStringValue: [NSString stringWithFormat:@"%f", el.SURF]];
    
}

- (IBAction)AllowPressed:(id)sender {
    DataModel *el = [DataManager DataList][index];
    [[self DataManager] setIsSimilar:true whereBasePathIs:el.imageBasePath CorrPathIs:el.imageCorrPath];
    index++;
    [self showImage];
}

- (IBAction)SkipPressed:(id)sender {
    index++;
}

- (IBAction)BackPressed:(id)sender {
    index--;
    [self showImage];
}

- (IBAction)DenyPressed:(id)sender {
    DataModel *el = [DataManager DataList][index];
    [[self DataManager] setIsSimilar:false whereBasePathIs:el.imageBasePath CorrPathIs:el.imageCorrPath];
    index++;
    [self showImage];
}
@end
