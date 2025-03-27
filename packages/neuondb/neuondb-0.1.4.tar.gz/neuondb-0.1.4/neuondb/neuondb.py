# -*- coding: utf-8 -*-
"""
Created on Tue Jun 18 15:11:26 2024

@author: yangl
"""

from pymongo import MongoClient, uri_parser
import pymongo
from neuon.neuon_utils import print_debug as print
from datetime import datetime, timedelta,timezone
import os
from typing import Optional, List, Dict
from bson.objectid import ObjectId

LOG_PING = True

def supress_ping_log(supress:bool=True):
    """
    Overide function to supress ping logs emiteed during checking connection
    with database. This ping message will emit everytime interaction
    with database is invoke to check if database connection is active which
    potentially could be over-logging.

    Parameters
    ----------
    supress : bool, optional  
        True to supress this specific log. The default is True.

    Returns
    -------
    None.

    """
    global LOG_PING
    LOG_PING = not supress

class neuondb(object):
    def __init__(self, uri:str, dbname:str,max_conn_pool=5):
        """
        Init connection to mongodb

        Parameters
        ----------
        uri : str  
            uri address.
        dbname : str  
            database name to connect.

        Returns
        -------
        None.

        """
        self.max_conn_pool = max_conn_pool
        
        self.uri = uri
        self.dbname = dbname
        self.connect_db()
        
        self.user = uri_parser.parse_uri(uri)
        
        self.current_timezone = datetime.now(timezone.utc).astimezone().tzinfo
        self.current_utcoffset = datetime.now(timezone.utc).astimezone().utcoffset()
        
        self.creation_timestamp_name = 'createdAt'
        self.update_timestamp_name = 'updatedAt'
        
    def set_creation_timestamp_name(self,custom_str:str):
        """
        Modified the creation_timestamp_name attribute to custom value
        Default is 'createdAt'

        Parameters
        ----------
        custom_str : str
            custom attribute/field to save for creation datetime.

        Returns
        -------
        None.

        """
        self.creation_timestamp_name = custom_str
    
    def set_update_timestamp_name(self,custom_str:str):
        """
        Modified the creation_timestamp_name attribute to custom value
        Default is 'updatedAt'        

        Parameters
        ----------
        custom_str : str
            custom attribute/field to save for updated datetime.

        Returns
        -------
        None.

        """
        self.update_timestamp_name = custom_str
    
    def timezone_aware(self,dt:datetime) -> datetime:
        """
        Convert datetime object to timezone aware format

        Parameters
        ----------
        dt : datetime  
            datetime presumably no timezone aware. i.e. +xx at the end
            is not provided.

        Returns
        -------
        datetime  
            datetime object with added timezone aware value.

        """
        return dt.replace(tzinfo=self.current_timezone)
    
    def connect_db(self) -> bool:
        """
        Init connection to db by URI provided in object creation.  
        Usually is used to re-establish connection with database

        Returns
        -------
        bool  
            return True if successfully connected.

        """
        self.client = MongoClient(self.uri,tz_aware=True,
                                  maxPoolSize=self.max_conn_pool)
        return self.is_db_connected()
    
    def is_db_connected(self):
        """
        Send a ping to server and get status

        Returns
        -------
        bool  
            True if database connected.

        """
        try:
            self.client.admin.command('ping')
            if LOG_PING:
                print("Pinged your deployment. You successfully connected to MongoDB!")
            return True
        except Exception as e:
            print(e)
            return False
        
    def insert_record(self,coll:str,insert_doc:dict) -> Optional[pymongo.results.InsertOneResult]:
        """
        Insert new record document to database

        Parameters
        ----------
        coll : str  
            collection name.  
        insert_doc : dict  
            dictionary to insert with key,value pairs.

        Returns
        -------
        inserted_result : pymongo.results.InsertOneResult or None  
            None if insert failed with error. Otherwise, pymongo.results.

        """
        if not self.is_db_connected():
            ret = self.connect_db()
        else:
            ret = True
            
        if ret:
            try:
                coll = self.client[self.dbname][coll]
                insert_doc[self.creation_timestamp_name] = datetime.now(tz=timezone.utc)
                inserted_result = coll.insert_one(insert_doc)
                
                return inserted_result
            except Exception as e:
                print('Connection failed!')
                print(e)
                return None
        
        else:
            print('Database not connected, insert failed')
            return None 

    def get_record(self, 
                   coll:str, 
                   query_doc:dict, 
                   project_doc:dict={},
                   sort_param:tuple=None,
                   limit:int=None) -> Optional[List[Dict]]:
        """
        Query record document

        Parameters
        ----------
        coll : str  
            collection name.  
        query_doc : dict  
            dictionary field to query with specific value.  
        project_doc : dict, optional  
            dictionary field with field to return set to 1. E.g.{_id:1}  
            The default is {}.  
        sort_param : tuple, optional  
            ('field_name',<1 or -1>). 1 for ascending, -1 descending.  
            The default is None.

        Returns
        -------
        list of dict  
            List of dictionary of query documents. Return None if failed.
            [] for empty return i.e. no matched entry

        """
        coll = self.client[self.dbname][coll]

        if not self.is_db_connected():
            ret = self.connect_db()
        else:
            ret = True
            
        if ret:
            if sort_param is not None:
                if limit is not None:
                    ret_doc = coll.find(query_doc,project_doc).sort(sort_param[0],sort_param[1]).limit(limit)
                else:
                    ret_doc = coll.find(query_doc,project_doc).sort(sort_param[0],sort_param[1])
            else:
                if limit is not None:
                    ret_doc = coll.find(query_doc,project_doc).limit(limit)
                else:
                    ret_doc = coll.find(query_doc,project_doc)
            ret = [x for x in ret_doc]
            if ret:
                return ret
            else:
                return []
        else:
            print('Database not connected, query failed')
            return None 
        
    def update_record(self, 
                      coll:str, 
                      update_uid:ObjectId, 
                      update_doc:dict) -> Optional[pymongo.results.UpdateResult]:
        """
        Update an existing record with specific field or add new field

        Parameters
        ----------
        coll : str  
            collection name.  
        update_uid : objectid.ObjectId  
            object uid of document to be updated.  
        update_doc : dict  
            dictionary with field to update or added.  

        Returns
        -------
        updated_result : pymongo.results.UpdateResult or None  
            return updated results obj or None if error occur.

        """
        if not self.is_db_connected():
            ret = self.connect_db()
        else:
            ret = True    
            
        if ret:
            try:
                coll = self.client[self.dbname][coll]
                update_doc[self.update_timestamp_name] = datetime.now(tz=timezone.utc)
                updated_result = coll.update_one({'_id':update_uid},
                                                 {'$set':update_doc})
                
                return updated_result
            except Exception as e:
                print('Connection failed!')
                print(e)
                return None
        
        else:
            print('Database not connected, update failed')
            return None 
        
    def delete_record(self, 
                      coll:str, 
                      delete_uid:ObjectId) -> Optional[pymongo.results.DeleteResult]:
        """
        Delete a record document given collection name and ObjectID

        Parameters
        ----------
        coll : str
            collection name.
        delete_uid : objectid.ObjectId
            object uid of the document to delete.

        Returns
        -------
        delete_res : pymongo.results.DeleteResult or None
            return result pymongo.results on delete or None of error occurs
            
            delete_res.acknowledged - bool
            delete_res.deleted_count - int
        """
        if not self.is_db_connected():
            ret = self.connect_db()
        else:
            ret = True  
            
        if ret:
            try:
                coll = self.client[self.dbname][coll]
                delete_res = coll.delete_one({'_id':delete_uid})
                
                return delete_res
            except Exception as e:
                print('Connection failed!')
                print(e)
                return None

        else:
            print('Database not connected, delete failed')
            return None             
        
        
