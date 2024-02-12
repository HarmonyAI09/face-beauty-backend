from pydantic import BaseModel
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

mongoURL = os.getenv("MONGO_URL")
client = MongoClient(mongoURL)
db = client[os.getenv("DB")]
reportCollection = db[os.getenv("REPORT_COLLECTION")]
keypointCollection = db[os.getenv("KEYPOINT_COLLECTION")]

class ReportStoreSchema(BaseModel):
    mail: str
    reportID: str
    gender: str
    race: str
    reportOwner: str
    keyPoints: list
    frontImage: str
    sideImage: str

    def store(self):
        current_date = str((datetime.now()).date())

        report_data = {
            "id": self.reportID,
            "owner": self.reportOwner,
            "gender": self.gender,
            "race": self.race,
            "date": current_date, 
            "front_image": self.frontImage,
            "side_image": self.sideImage
        }

        existing_record = reportCollection.find_one({"mail": self.mail})

        if existing_record:
            if any(report['id'] == self.reportID for report in existing_record.get('reports', [])):
                # Update all fields of the existing report
                reportCollection.update_one(
                    {"mail": self.mail, "reports.id": self.reportID},
                    {"$set": {"reports.$": report_data}}
                )
            else:
                reportCollection.update_one(
                    {"mail": self.mail},
                    {"$push": {"reports": report_data}}
                )
        else:
            reportCollection.insert_one({
                "mail": self.mail,
                "reports": [report_data]
            })

        existing_keypoint_record = keypointCollection.find_one({"reportID": self.reportID})

        if existing_keypoint_record:
            keypointCollection.update_one(
                {"reportID": self.reportID},
                {"$set": {"keyPoints": self.keyPoints}}
            )
        else:
            keypointCollection.insert_one({
                "reportID": self.reportID,
                "keyPoints": self.keyPoints
            })

        return {"success": True, "status": "Saved successfully."}
    
    def getReports(mail: str):
        reports = reportCollection.find({"mail": mail})
        reportList = []
        for report in reports:
            reportList.extend(report.get('reports', []))
        return reportList
    
    def getDetails(id: str):
        detail = keypointCollection.find_one({"reportID": id})
        del detail["_id"]

        return detail
    
class ReportSaveSchema(BaseModel):
    report_id: str
    gender: str
    name: str
    percentage: float
    race: str
    score: float

class ReportFrontSideSaveSchema(BaseModel):
    report_id: str
    profile_data: str