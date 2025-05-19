from typing import Optional, Dict, Any, List
from datetime import datetime, date
from src.config.firebase_config import FirebaseConfig

class FirebaseRepository:
    """Repository pattern implementation for Firebase Firestore operations"""

    def __init__(self):
        self._firebase = FirebaseConfig()
        self._db = self._firebase.get_db()

    def _ensure_connection(self) -> None:
        """Verify Firebase connection is initialized"""
        if not self._db:
            raise ConnectionError("Firebase connection not initialized")

    def _convert_date_types(self, value: Any) -> str:
        """Convert datetime/date objects to ISO format string"""
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, date):
            return datetime.combine(value, datetime.min.time()).isoformat()
        return value

    def _prepare_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Process data dictionary for Firestore compatibility"""
        if not data:
            return {}
        return {
            key: self._convert_date_types(value)
            for key, value in data.items()
        }

    def add_document(
        self, 
        collection: str, 
        data: Dict[str, Any], 
        doc_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Add a new document to a collection
        
        Args:
            collection: Name of the collection
            data: Document data
            doc_id: Optional custom document ID
        
        Returns:
            Dictionary containing document data and ID
        """
        self._ensure_connection()
        processed_data = self._prepare_data(data)
        
        if doc_id:
            doc_ref = self._db.collection(collection).document(doc_id)
            doc_ref.set(processed_data)
            return {**processed_data, "id": doc_id}
        
        doc_ref = self._db.collection(collection).document()
        doc_ref.set(processed_data)
        return {**processed_data, "id": doc_ref.id}

    def get_document(
        self, 
        collection: str, 
        doc_id: str
    ) -> Optional[Dict[str, Any]]:
        """Retrieve a document by its ID"""
        self._ensure_connection()
        
        doc = self._db.collection(collection).document(doc_id).get()
        if doc.exists:
            return {**doc.to_dict(), "id": doc.id}
        return None

    def update_document(
        self, 
        collection: str, 
        doc_id: str, 
        data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing document"""
        self._ensure_connection()
        
        processed_data = self._prepare_data(data)
        doc_ref = self._db.collection(collection).document(doc_id)
        doc_ref.update(processed_data)
        return {**processed_data, "id": doc_id}

    def delete_document(self, collection: str, doc_id: str) -> bool:
        """Delete a document from a collection"""
        self._ensure_connection()
        
        self._db.collection(collection).document(doc_id).delete()
        return True

    def query_collection(
        self, 
        collection: str, 
        field: Optional[str] = None, 
        operator: Optional[str] = None, 
        value: Optional[Any] = None
    ) -> List[Dict[str, Any]]:
        """
        Query documents with optional filtering
        
        Args:
            collection: Collection name
            field: Field to filter on
            operator: Comparison operator
            value: Value to compare against
        """
        self._ensure_connection()
        
        collection_ref = self._db.collection(collection)
        if all([field, operator, value is not None]):
            docs = collection_ref.where(field, operator, value).stream()
        else:
            docs = collection_ref.stream()
            
        return [{**doc.to_dict(), "id": doc.id} for doc in docs]