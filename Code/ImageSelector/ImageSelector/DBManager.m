//
//  DataLoader.m
//  ImageSelector
//
//  Created by Darka on 02/03/15.
//  Copyright (c) 2015 Darka. All rights reserved.
//

#import "DBManager.h"

@implementation DBManager
@synthesize db;
@synthesize DataList;

/*
 .schema comparated_image
 
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

-(id)initWithDatabaseName:(NSString *)dbName{
    if (sqlite3_open([dbName UTF8String], &db)!= SQLITE_OK){
        sqlite3_close(db);
        NSLog(@"Database failed to open");
    }
    else{
        //initialize array
        DataList = [[NSMutableArray alloc] init];
        
        //read data from table comparated_image
        NSString *tableName = @"comparated_image";
        NSString *sql = [NSString stringWithFormat:@"SELECT * FROM %@", tableName];
        sqlite3_stmt * statement;
        if(sqlite3_prepare_v2(db, [sql UTF8String], -1, &statement, nil) == SQLITE_OK)
        {
            while(sqlite3_step(statement) == SQLITE_ROW)
            {
                //retrieve img base path using column number
                char * img_base_path = (char *) sqlite3_column_text(statement, 2);
                NSString *imgBasePath = [[NSString alloc] initWithUTF8String: img_base_path];
                
                //retrieve img correlated path using column number
                char * img_corr_path = (char *) sqlite3_column_text(statement,4);
                NSString *imgCorrPath = [[NSString alloc] initWithUTF8String: img_corr_path];
                
                //retrieve SURF value
                char * SURF = (char *) sqlite3_column_text(statement,5);
                float surfValue = [[[NSString alloc] initWithUTF8String: SURF] floatValue];
                
                //make object with paths
                DataModel* el = [[DataModel alloc] initWithBasePath:imgBasePath CorrPath:imgCorrPath SURFValue:surfValue];
                //adding el to list
                [DataList addObject:el];
            }
        }
    }
    return self;
}

-(void)setIsSimilar:(bool)isSimilar whereBasePathIs:(NSString*)basePath CorrPathIs:(NSString*)corrPath{
    NSString* s = @"1";
    if(!isSimilar)
        s=@"0";
    NSString *queryString =[NSString stringWithFormat:@"update comparated_image set is_similar = %@ where img_base_path = '%@' and img_corr_path = '%@';",
                            s,basePath,corrPath];
    NSLog(queryString);
    const char *query = [queryString UTF8String];
    sqlite3_exec(db,query, NULL, NULL, NULL);
}

-(void)closeDB{
    sqlite3_close(db);
}
@end
