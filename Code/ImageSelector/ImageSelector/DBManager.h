//
//  DataLoader.h
//  ImageSelector
//
//  Created by Darka on 02/03/15.
//  Copyright (c) 2015 Darka. All rights reserved.
//

#import <Foundation/Foundation.h>
#import <sqlite3.h>
#import "DataModel.h"
@interface DBManager : NSObject

-(id) initWithDatabaseName:(NSString*)dbName;
-(void)setIsSimilar:(bool)isSimilar whereBasePathIs:(NSString*)basePath CorrPathIs:(NSString*)corrPath;
-(void)closeDB;

@property sqlite3 *db;
@property NSMutableArray *DataList;
@end
