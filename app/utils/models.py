from chainlit.element import ElementDict
import requests
from typing import TYPE_CHECKING, Any, Dict, List, Optional, Union
import json
import uuid

from chainlit.data.sql_alchemy import SQLAlchemyDataLayer
from chainlit.logger import logger
from chainlit.user import PersistedUser, User
from sqlalchemy import Column, Integer, String, Text, JSON, DateTime
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.dialects.postgresql import UUID, JSONB
from datetime import datetime

    
class CustomSQLAlchemyDataLayer(SQLAlchemyDataLayer):
    def __init__(self, conninfo: str, **kwargs):
        super().__init__(conninfo, **kwargs)
    
    async def get_user(self, identifier: str) -> Optional[PersistedUser]:
        """
        Retrieve a user from the database based on the provided identifier.
        
        Args:
            identifier (str): The unique identifier of the user to retrieve.
        
        Returns:
            Optional[PersistedUser]: The retrieved user if found, else None.
        """
        if self.show_logger:
            logger.info(f"SQLAlchemy: get_user, identifier={identifier}")
        query = "SELECT * FROM users WHERE identifier = :identifier"
        parameters = {"identifier": identifier}
        result = await self.execute_sql(query=query, parameters=parameters)
        if result and isinstance(result, list):
            user_data = result[0]
            user_data["display_name"] = user_data.pop("displayName")
            return PersistedUser(**user_data)
        return None
    
    async def create_user(self, user: User) -> Optional[PersistedUser]:
        """
        Create a new user in the database or update an existing user's metadata and display name.

        Args:
            user (User): The user object to be created or updated.

        Returns:
            Optional[PersistedUser]: The created or updated user if successful, else None.
        """
        if self.show_logger:
            logger.info(f"SQLAlchemy: create_user, user_identifier={user.identifier}")
        existing_user: Optional["PersistedUser"] = await self.get_user(user.identifier)
        user_dict: Dict[str, Any] = {
            "identifier": str(user.identifier),
            "metadata": json.dumps(user.metadata) or {},
            "displayName": str(user.display_name)
        }
        
        if not existing_user:  # create the user
            if self.show_logger:
                logger.info("SQLAlchemy: create_user, creating the user")
            user_dict["id"] = str(uuid.uuid4())
            user_dict["createdAt"] = await self.get_current_timestamp()
            query = """INSERT INTO users ("id", "identifier", "createdAt", "metadata", "displayName") VALUES (:id, :identifier, :createdAt, :metadata, :displayName)"""
            await self.execute_sql(query=query, parameters=user_dict)
        else:  # update the user
            if self.show_logger:
                logger.info("SQLAlchemy: update user metadata")
            query = """UPDATE users SET "metadata" = :metadata, "displayName" = :displayName WHERE "identifier" = :identifier"""
            await self.execute_sql(
                query=query, parameters=user_dict
            )  # We want to update the metadata
        return await self.get_user(user.identifier)

    async def get_element(self, thread_id: str, element_id: str) -> Optional["ElementDict"]:
        if self.show_logger:
            logger.info(
                f"SQLAlchemy: get_element, thread_id={thread_id}, element_id={element_id}"
            )
        query = """SELECT * FROM elements WHERE "threadId" = :thread_id AND "id" = :element_id"""
        parameters = {"thread_id": thread_id, "element_id": element_id}
        element: Union[List[Dict[str, Any]], int, None] = await self.execute_sql(
            query=query, parameters=parameters
        )
        if isinstance(element, list) and element:
            element_dict: Dict[str, Any] = element[0]
            return ElementDict(
                id=element_dict["id"],
                threadId=element_dict.get("threadId"),
                type=element_dict["type"],
                chainlitKey=element_dict.get("chainlitKey"),
                url=element_dict.get("url"),
                objectKey=element_dict.get("objectKey"),
                name=element_dict["name"],
                display=element_dict["display"],
                size=element_dict.get("size"),
                language=element_dict.get("language"),
                page=element_dict.get("page"),
                autoPlay=element_dict.get("autoPlay"),
                playerConfig=element_dict.get("playerConfig"),
                forId=element_dict.get("forId"),
                mime=element_dict.get("mime"),
            )
        else:
            return None
        
class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, nullable=False)
    identifier = Column(Text, nullable=False)
    metadata_ = Column("metadata", JSONB, nullable=False)
    created_at = Column("createdAt", Text, default=lambda: datetime.utcnow().isoformat())
    display_name = Column("displayName", Text)
    password = Column(String(255))

    def __repr__(self):
        return f"<User(id={self.id}, identifier={self.identifier}, display_name={self.display_name})>"    
    