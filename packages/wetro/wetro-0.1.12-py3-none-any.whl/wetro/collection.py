
from wetro.api_client import WetrocloudClient
from typing import Optional,List, Union, Iterable
from wetro.custom_types import (
    ChatModel, 
    ResourceType, 
    ChatHistory, 
    JSONSchema, 
    CollectionID, 
    ResourceID
    )
from wetro.custom_response import (
    QueryResponse, 
    ChatResponse, 
    InsertResponse, 
    RemoveResponse, 
    DeleteCollectionResponse,
    ListCollectionResponse,
    CreateCollectionResponse
    )




class CollectionAPI:
    """
    Interface for collection operations.
    """
    def __init__(
            self, 
            client: WetrocloudClient
        ):
        self.client = client
        self.collection_id: Optional[CollectionID] = None

    def get_or_create_collection_id(
            self, 
            collection_id: CollectionID
        ) -> None:
        """
        Check if the collection exists and get collection; if not, create a new collection.
        """
        get_response = self.client.get_collection(collection_id)
        if get_response.found:
            self.collection_id = get_response.collection_id
        else:
            create_response = self.client.create_collection(collection_id)
            self.collection_id = create_response.collection_id

    def create_collection_id(
            self, 
            collection_id: CollectionID
        ) -> CreateCollectionResponse:
        """
        Create a new collection.
        """
        return self.client.create_collection(collection_id)

    def get_all(
            self
        ) -> ListCollectionResponse:
        """
        Get all collection.
        """
        return self.client.list_collection()

    def insert(
            self,
            resource: str, 
            type: ResourceType,
            collection_id: Optional[CollectionID] = None
        ) -> InsertResponse:
        """
        Inserts resource into a collection.
        """
        if collection_id == None:
            if not self.collection_id:
                raise ValueError("Collection ID not set.")
            else:
                collection_id = self.collection_id
        return self.client.insert_resource(collection_id, resource, type)
    
    def delete_resource(
            self, 
            resource_id: ResourceID,
            collection_id: Optional[CollectionID] = None
        ) -> RemoveResponse:
        """
        Removes resource from a collection.
        """
        if collection_id == None:
            if not self.collection_id:
                raise ValueError("Collection ID not set.")
            else:
                collection_id = self.collection_id
        return self.client.remove_resource(collection_id, resource_id)

    def query(
            self, 
            request_query: str, 
            model: Optional[ChatModel] = None,
            json_schema: Optional[JSONSchema] = None,
            json_schema_rules: Optional[List[str]] = None,
            stream: bool = False,
            collection_id: Optional[CollectionID] = None
            ) -> Union[QueryResponse, Iterable[QueryResponse]]:
        """
        Query your collection.
        """
        if collection_id == None:
            if not self.collection_id:
                raise ValueError("Collection ID not set.")
            else:
                collection_id = self.collection_id
        return self.client.query_collection(
            collection_id,
            request_query,
            model=model,
            json_schema=json_schema,
            json_schema_rules=json_schema_rules,
            stream=stream
        )

    def chat(
            self, 
            message: str, 
            chat_history: ChatHistory, 
            model: Optional[ChatModel] = None,
            stream: bool = False,
            collection_id: Optional[CollectionID] = None
        ) -> Union[QueryResponse, Iterable[ChatResponse]]:
        """
        Chat with your collection.
        """
        if collection_id == None:
            if not self.collection_id:
                raise ValueError("Collection ID not set.")
            else:
                collection_id = self.collection_id
        return self.client.chat_with_collection(
            collection_id, 
            message, 
            chat_history, 
            model=model,
            stream=stream
            )

    def delete(self,collection_id: Optional[CollectionID] = None) -> DeleteCollectionResponse:
        """
        Delete your collection.
        """
        if collection_id == None:
            if not self.collection_id:
                raise ValueError("Collection ID not set.")
            else:
                collection_id = self.collection_id
        response = self.client.delete_collection(collection_id)
        self.collection_id = None
        return response
