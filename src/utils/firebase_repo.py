
from src.config.firebase_config import FirebaseConfig
import uuid
from datetime import datetime
from datetime import datetime, date


class FirebaseRepository:
    def __init__(self):
        self.firebase = FirebaseConfig()
        self.db = self.firebase.get_db()

    def _convert_datetime_to_timestamp(self, dt):
        """Convert Python datetime to Firestore timestamp-compatible format"""
        if isinstance(dt, datetime):
            return dt.isoformat()
        return dt
    def _prepare_data(self, data):
        """Prepare data for Firestore by handling special data types"""
        if not data:
            return data

        result = {}
        for key, value in data.items():
            if isinstance(value, datetime):
                result[key] = value.isoformat()
            elif isinstance(value, date):
                # Convert date to datetime first
                dt_value = datetime.combine(value, datetime.min.time())
                result[key] = dt_value.isoformat()
            else:
                result[key] = value
        return result

    def add_document(self, collection, data, doc_id=None):
        """Add a document to Firestore collection"""
        if not self.db:
            raise Exception("Firebase not initialized")
            
        data = self._prepare_data(data)
        
        if doc_id:
            doc_ref = self.db.collection(collection).document(doc_id)
            doc_ref.set(data)
            return {**data, "id": doc_id}
        else:
            # For collections that need auto-generated IDs
            doc_ref = self.db.collection(collection).document()
            doc_ref.set(data)
            return {**data, "id": doc_ref.id}

    def get_document(self, collection, doc_id):
        """Get a document by ID"""
        if not self.db:
            raise Exception("Firebase not initialized")
            
        doc = self.db.collection(collection).document(doc_id).get()
        if doc.exists:
            return {**doc.to_dict(), "id": doc.id}
        return None

    def update_document(self, collection, doc_id, data):
        """Update a document"""
        if not self.db:
            raise Exception("Firebase not initialized")
            
        data = self._prepare_data(data)
        doc_ref = self.db.collection(collection).document(doc_id)
        doc_ref.update(data)
        return {**data, "id": doc_id}

    def delete_document(self, collection, doc_id):
        """Delete a document"""
        if not self.db:
            raise Exception("Firebase not initialized")
            
        self.db.collection(collection).document(doc_id).delete()
        return True

    def query_collection(self, collection, field=None, operator=None, value=None):
        """Query documents from a collection with optional filtering"""
        if not self.db:
            raise Exception("Firebase not initialized")
            
        if field and operator and value is not None:
            docs = self.db.collection(collection).where(field, operator, value).stream()
        else:
            docs = self.db.collection(collection).stream()
            
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]