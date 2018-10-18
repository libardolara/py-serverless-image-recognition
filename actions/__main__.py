import sys
import os
import json
from watson_developer_cloud import VisualRecognitionV3
from cloudant.client import Cloudant

client = None
dbname = None
dbNameProcessed = None

def main(args):
    global client
    global dbname
    global dbNameProcessed

    #print(args)
    dbhost = "https://"+ args["username"]+".cloudant.com"
    client = Cloudant(args["username"], args["password"], url=dbhost, connect=True)
    dbname = args["dbname"]
    dbNameProcessed = args["dbname_processed"]

    id = args.get("id","")
    print(id)
    my_database = client[dbname]
    my_doc = my_database[id]
    my_image = my_doc.get_attachment('image')

    #client.disconnect()
    return processImageToWatson(my_image, args["id"], args["watson_vr_apikey"])

def processImageToWatson(data, id, apikey):
    filename = os.path.dirname('__file__') + "/" + id
    newFile = open(filename, "wb")
    newFile.write(data)
    newFile.close()

    with open(filename, 'rb') as images_file:
        visual_recognition = VisualRecognitionV3('2018-03-19',iam_apikey=apikey)
        classes = visual_recognition.classify(images_file).get_result()

    return updateDocument(classes, id)

def updateDocument(watsonResult, id):
    global client
    global dbNameProcessed

    mydb = client[dbNameProcessed]
    doc = {
        "_id" : id,
        "watsonResults" : watsonResult["images"][0]["classifiers"]
    }
    mydoc = mydb.create_document(doc)
    return mydoc
