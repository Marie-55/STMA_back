from src.utils.firebase_repo import FirebaseRepository

class FirebaseUser:
    def __init__(self):
        self.repo = FirebaseRepository()
        self.collection = "users"
    
    def create(self, email, password):
        return self.repo.add_document(self.collection, {"email": email, "password": password}, doc_id=email)
        
    def get_by_email(self, email):
        return self.repo.get_document(self.collection, email)
    
    # def get_by_email(self, email):
    #     return self.repo.get_document(self.collection, passwo)
        
    def update(self, email, data):
        return self.repo.update_document(self.collection, email, data)
        
    def delete(self, email):
        return self.repo.delete_document(self.collection, email)