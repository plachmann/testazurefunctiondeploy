import logging
import json
import azure.functions as func
import firebase_admin as firebase_admin
from firebase_admin import firestore


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    jsonstr = getWayfinderData()

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')

    if name:
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully." + jsonstr)
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


def getWayfinderData(): 
    default_app = firebase_admin.initialize_app()
    print("NAME: " + default_app.name)
    db = firestore.client()
    docs = db.collection("Assessments").stream()

    jsondoc=[]

    for doc in docs:
        json_dict = {}
        # bob = "{" + 'id : {}, value : {}'.format(doc.id, doc.to_dict()) +"}"
        json_dict["id"] = doc.id
        json_dict["value"] = assessmentFromDictionary(doc.to_dict(), doc.id, db)
        # print(bob)
        jsondoc.append(json_dict)
        # print(bob)
        return json.dumps(jsondoc)

    return json.dumps(jsondoc)
        

def assessmentFromDictionary(theDictionary, assessmentId, db):
    assessment = {}
    assessment["startDate"] = theDictionary["startDate"] if "startDate" in theDictionary else ""
    assessment["completedDate"] = theDictionary["completedDate"] if "completedDate" in theDictionary else ""
    assessment["email"] = theDictionary["email"] if "email" in theDictionary else ""
    assessment["congregationid"] = theDictionary["congregationid"] if "congregationid" in theDictionary else ""
    assessment["congregation"] = theDictionary["congregation"] if "congregation" in theDictionary else ""
    assessment["firstname"] = theDictionary["firstname"] if "firstname" in theDictionary else ""
    assessment["lastname"] = theDictionary["lastname"] if "lastname" in theDictionary else ""
    assessment["learned"] = theDictionary["learned"] if "learned" in theDictionary else ""
    assessment["resultsEmailSent"] = theDictionary["resultsEmailSent"] if "resultsEmailSent" in theDictionary else ""
    assessment["reflectionEmailSent"] = theDictionary["reflectionEmailSent"] if "reflectionEmailSent" in theDictionary else ""
    assessment["resultsEmailSendDate"] = buildDateString(theDictionary["resultsEmailSendDate"]) if "resultsEmailSendDate" in theDictionary else ""
    assessment["reflectionEmailSendDate"] = buildDateString(theDictionary["reflectionEmailSendDate"]) if "reflectionEmailSendDate" in theDictionary else ""
    assessment["Responses"] = getResponses(assessmentId, db)
    return assessment

def buildDateString(crapFromFirestore):
    dateString = str(crapFromFirestore)
    return dateString

def getResponses(assessmentId, db):
    responses = []
    # get the responses from firestore
    docs = db.collection("Assessments/"+assessmentId+"/Responses").stream()

    for doc in docs:
        response = {}
        # build the response
        theDictionary = doc.to_dict()
        response["id"] = doc.id
        response["answertext"] = theDictionary["answertext"] if "answertext" in theDictionary else ""
        response["answervalue"] = theDictionary["answervalue"] if "answervalue" in theDictionary else ""
        response["category"] = theDictionary["category"] if "category" in theDictionary else ""
        response["categoryweight"] = theDictionary["categoryweight"] if "categoryweight" in theDictionary else ""
        response["enddate"] = theDictionary["enddate"] if "enddate" in theDictionary else ""
        response["startdate"] = theDictionary["startdate"] if "startdate" in theDictionary else ""
        response["questionid"] = theDictionary["questionid"] if "questionid" in theDictionary else ""
        response["questiontext"] = theDictionary["questiontext"] if "questiontext" in theDictionary else ""
        response["questionweight"] = theDictionary["questionweight"] if "questionweight" in theDictionary else ""
        response["sortorder"] = theDictionary["sortorder"] if "sortorder" in theDictionary else ""
        responses.append(response)
    
    return responses
    