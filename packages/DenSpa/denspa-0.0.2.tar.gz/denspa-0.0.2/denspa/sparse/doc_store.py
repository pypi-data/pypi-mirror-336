import joblib


class DocStore:

    def __init__(self,documents={}):
        self.documents = documents

    def get(self,key):
        return self.documents[key]

    def put(self,key,value):
        self.documents[key] = value
        return self

    def remove(self,key):
        del self.documents[key]
        return self
    def get_last_key(self):
        return next(reversed(self.documents.keys()))

    def is_empty(self):
        return len(self.documents.keys())==0

    def search(self,metadata):
        documents = []
        for key,doc in self.documents.items():
            if all(doc.metadata.get(k,None)==v for k,v in metadata.items()):
                documents.append((key,doc))
        return documents

    def save_local(self,folder_path,filename):
        joblib.dump(self,folder_path+"/"+filename+".pkl", compress=True)
        return self

    @staticmethod
    def load_local(folder_path,filename):
        return joblib.load(folder_path+"/"+filename+".pkl")