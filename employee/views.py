import bson
import pymongo
from bson.objectid import ObjectId
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
import json
from utils import get_db_handle, get_collection_handle
from django.db import transaction

# Create your views here.
class Employee(viewsets.ModelViewSet):
    myclient = pymongo.MongoClient("mongodb+srv://<username>:<password>@cluster0.ruanruv.mongodb.net/?retryWrites=true&w=majority"
        )
    mydb = myclient["mydatabase2"]
    collection_ = mydb['mySampleCollection2']

    def create_employee(self,request):
        # db_name='mydatabase'
        # host='ac-5wvscvj-shard-00-00.ruanruv.mongodb.net'
        # username='mahnoor'
        # password='h7dC3dl0CzBi0cle'
        list1=list()
        # port=27017
        # db_handle,client = get_db_handle(db_name, host, port, username, password)
        # collection_handle=get_collection_handle(db_handle,"mySampleCollection")
        # data=collection_handle.find({})
        data_dict=request.data.copy()


        result=self.collection_.insert_one(data_dict)

        data=self.collection_.find_one({"_id": {"$eq": result.inserted_id}})
        id_ = str(result.inserted_id)
        data.update({'_id': id_})
        return Response({"result":data,"msg":"data added"})

    def view_employee(self,request):
        try:
            id_=request.query_params.get("id")
            new_id=ObjectId(id_)
            data=self.collection_.find_one({"_id":{"$eq":new_id}})
            print(data)
            if data is None:
                return Response({"msg":"no data found"})
            id_to_str=str(data.get("_id"))
            data.update({'_id':id_to_str})
            return Response(data)
        except Exception as e:
            return Response({"msg":str(e)})


    def view_all_emp(self,request):
        data=dict()
        data = list(self.collection_.find({}))
        for x in data:
            for key,values in x.items():
                if key=='_id':
                    key_=str(values)
                    x.update({key:key_})
        # id_to_str = str(data.get("_id"))
        # data.update({'_id': id_to_str})
        return Response(data)

    def delete_emp(self,request):
        id_ = request.query_params.get("id")
        new_id = ObjectId(id_)
        dele=self.collection_.delete_one({"_id":new_id})
        if dele.deleted_count>0:
            return Response({"msg":"deleted"})
        return Response({"msg":"no record found for deletion"})


    def update_emp(self,request):
        try:
            id_ = request.query_params.get("id")
            new_id = ObjectId(id_)
            prev = self.collection_.find_one({"_id": {"$eq": new_id}})
            if prev is None:
                return  Response({"msg":"can't find id for update"})
            data_dict=request.data.copy()
            nextt={"$set":{"EmployeeName":data_dict["EmployeeName"],"Department":data_dict['Department'],"DateOfJoining":data_dict["DateOfJoining"]}}
            try:
                dele = self.collection_.update_one(prev,nextt)
                if dele.modified_count >0:

                   result=self.collection_.find_one({"_id": {"$eq": new_id}})

                   id_to_str = str(result.get("_id"))
                   result.update({'_id': id_to_str})

                   return Response({"data":result,"msg":"data updated"})
                else:
                    return Response({"msg":"No record updated"})
            except Exception as e:
                return Response({"error": str(e)})

        except Exception as e:
            return Response({"error":str(e)})

    def filter_data(self,request):
        result=self.collection_.aggregate(
            [{"$group":{"_id":"$Department","value":{"$count":{}}}}])
        x=list(result)
        return Response({"data":x})







