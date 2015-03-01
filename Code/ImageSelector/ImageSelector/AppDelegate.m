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
@synthesize linkList;
@synthesize linkIndex;
@synthesize allowedLink;
@synthesize denyLink;
@synthesize db;


- (void)applicationDidFinishLaunching:(NSNotification *)aNotification {
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
    if (sqlite3_open([db_filename UTF8String], &db)!= SQLITE_OK)
    {
        sqlite3_close(db);
        NSLog(@"Database failed to open");
    }
    else{
        //initialize array
        linkList = [[NSMutableArray alloc] init];
        //read all link from table
        NSString *tableName = @"comparated_image";
        NSString *sql = [NSString stringWithFormat:@"SELECT * FROM %@", tableName];
        sqlite3_stmt * statement;
        if(sqlite3_prepare_v2(db, [sql UTF8String], -1, &statement, nil) == SQLITE_OK)
        {
            while(sqlite3_step(statement) == SQLITE_ROW)
            {
                char *field3 = (char *) sqlite3_column_text(statement, 3);
                NSString *link = [[NSString alloc] initWithUTF8String:field3];
                field3 = (char *) sqlite3_column_text(statement, 2);
                NSString *localPath = [[NSString alloc] initWithUTF8String:field3];
                field3 = (char *) sqlite3_column_text(statement, 5);
                NSString *allowed = [[NSString alloc] initWithUTF8String:field3];
                [linkList addObject:[[LinkPath alloc] initWithLink:link Path:localPath andAllowed:allowed]];
            }
        }
    }

    linkIndex = 0;
    allowedLink = [[NSMutableArray alloc] init];
    denyLink = [[NSMutableArray alloc] init];
    [self showImage];
}

- (void)applicationWillTerminate:(NSNotification *)aNotification {
    // Insert code here to tear down your application
    sqlite3_close(db);
}

- (IBAction)AllowPressed:(id)sender {
    [allowedLink addObject:linkList[linkIndex]];
    NSString *queryString =[NSString stringWithFormat:@"update image set allowed = 'Y' where url ='%@' ",[linkList[linkIndex] Link]];
    const char *query = [queryString UTF8String];
    sqlite3_exec(db,query, NULL, NULL, NULL);
    linkIndex++;
    [self showImage];
}

- (IBAction)DenyPressed:(id)sender {
    [denyLink addObject:linkList[linkIndex]];
    NSString *queryString =[NSString stringWithFormat:@"update image set allowed = 'N' where url ='%@' ",[linkList[linkIndex] Link]];
    const char *query = [queryString UTF8String];
    sqlite3_exec(db,query, NULL, NULL, NULL);
    linkIndex++;
    [self showImage];
}

- (IBAction)SkipPressed:(id)sender {
    [allowedLink addObject:linkList[linkIndex]];
    NSString *queryString =[NSString stringWithFormat:@"update image set allowed = '0' where url ='%@' ",[linkList[linkIndex] Link]];
    const char *query = [queryString UTF8String];
    sqlite3_exec(db,query, NULL, NULL, NULL);
    linkIndex++;
    [self showImage];
}

- (IBAction)BackPressed:(id)sender {
    linkIndex--;
    [self showImage];
}

- (IBAction)AllPressed:(id)sender {
}

-(void)showImage{
    LinkPath *el = linkList[linkIndex];
    //show first image
    //NSImage *image = [[NSImage alloc]initWithData:[NSData dataWithContentsOfURL:[NSURL URLWithString:el.Link]]];
    NSString *path = [NSString stringWithFormat:@"%@%@",@"/Users/darka/Dev/DataHiding/Code/",el.LocalPath];
    NSImage *image = [[NSImage alloc] initByReferencingFile:path];
    [self.ImageViewer setImage:image];
    [self.LinkLabel setStringValue:el.Link];
}

@end
