from fastapi import APIRouter, HTTPException, status
from app.models.ai_assistant import (
    AIAssistantCreate,
    AIAssistantUpdate,
    AIAssistantResponse,
    AIAssistantListResponse,
    DeleteResponse
)
from app.config.database import Database
from bson import ObjectId
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/", response_model=AIAssistantResponse, status_code=status.HTTP_201_CREATED)
async def create_assistant(assistant_data: AIAssistantCreate):
    """
    Create a new AI assistant for a user

    Args:
        assistant_data: AI assistant configuration

    Returns:
        AIAssistantResponse: Created assistant details

    Raises:
        HTTPException: If user not found or error occurs
    """
    try:
        db = Database.get_db()
        users_collection = db['users']
        assistants_collection = db['assistants']

        logger.info(f"Creating AI assistant for user: {assistant_data.user_id}")

        # Verify user exists
        try:
            user_obj_id = ObjectId(assistant_data.user_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user_id format"
            )

        user = users_collection.find_one({"_id": user_obj_id})
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        # Create assistant document
        now = datetime.utcnow()
        assistant_doc = {
            "user_id": user_obj_id,
            "name": assistant_data.name,
            "system_message": assistant_data.system_message,
            "voice": assistant_data.voice,
            "temperature": assistant_data.temperature,
            "created_at": now,
            "updated_at": now
        }

        result = assistants_collection.insert_one(assistant_doc)
        logger.info(f"AI assistant created with ID: {result.inserted_id}")

        return AIAssistantResponse(
            id=str(result.inserted_id),
            user_id=str(assistant_data.user_id),
            name=assistant_data.name,
            system_message=assistant_data.system_message,
            voice=assistant_data.voice,
            temperature=assistant_data.temperature,
            created_at=now.isoformat() + "Z",
            updated_at=now.isoformat() + "Z"
        )

    except HTTPException:
        raise
    except Exception as error:
        import traceback
        logger.error(f"Error creating AI assistant: {str(error)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create AI assistant: {str(error)}"
        )

@router.get("/user/{user_id}", response_model=AIAssistantListResponse, status_code=status.HTTP_200_OK)
async def get_user_assistants(user_id: str):
    """
    Get all AI assistants for a specific user

    Args:
        user_id: User ID

    Returns:
        AIAssistantListResponse: List of user's assistants

    Raises:
        HTTPException: If user not found or error occurs
    """
    try:
        db = Database.get_db()
        assistants_collection = db['assistants']

        logger.info(f"Fetching AI assistants for user: {user_id}")

        # Convert user_id to ObjectId
        try:
            user_obj_id = ObjectId(user_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user_id format"
            )

        # Find all assistants for this user
        assistants_cursor = assistants_collection.find({"user_id": user_obj_id})
        assistants = []

        for assistant in assistants_cursor:
            assistants.append(AIAssistantResponse(
                id=str(assistant['_id']),
                user_id=str(assistant['user_id']),
                name=assistant['name'],
                system_message=assistant['system_message'],
                voice=assistant['voice'],
                temperature=assistant['temperature'],
                created_at=assistant['created_at'].isoformat() + "Z",
                updated_at=assistant['updated_at'].isoformat() + "Z"
            ))

        logger.info(f"Found {len(assistants)} assistants for user {user_id}")

        return AIAssistantListResponse(
            assistants=assistants,
            total=len(assistants)
        )

    except HTTPException:
        raise
    except Exception as error:
        import traceback
        logger.error(f"Error fetching AI assistants: {str(error)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch AI assistants: {str(error)}"
        )

@router.get("/{assistant_id}", response_model=AIAssistantResponse, status_code=status.HTTP_200_OK)
async def get_assistant(assistant_id: str):
    """
    Get a specific AI assistant by ID

    Args:
        assistant_id: Assistant ID

    Returns:
        AIAssistantResponse: Assistant details

    Raises:
        HTTPException: If assistant not found or error occurs
    """
    try:
        db = Database.get_db()
        assistants_collection = db['assistants']

        logger.info(f"Fetching AI assistant: {assistant_id}")

        # Convert to ObjectId
        try:
            assistant_obj_id = ObjectId(assistant_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid assistant_id format"
            )

        assistant = assistants_collection.find_one({"_id": assistant_obj_id})

        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AI assistant not found"
            )

        return AIAssistantResponse(
            id=str(assistant['_id']),
            user_id=str(assistant['user_id']),
            name=assistant['name'],
            system_message=assistant['system_message'],
            voice=assistant['voice'],
            temperature=assistant['temperature'],
            created_at=assistant['created_at'].isoformat() + "Z",
            updated_at=assistant['updated_at'].isoformat() + "Z"
        )

    except HTTPException:
        raise
    except Exception as error:
        import traceback
        logger.error(f"Error fetching AI assistant: {str(error)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to fetch AI assistant: {str(error)}"
        )

@router.put("/{assistant_id}", response_model=AIAssistantResponse, status_code=status.HTTP_200_OK)
async def update_assistant(assistant_id: str, update_data: AIAssistantUpdate):
    """
    Update an existing AI assistant

    Args:
        assistant_id: Assistant ID
        update_data: Fields to update

    Returns:
        AIAssistantResponse: Updated assistant details

    Raises:
        HTTPException: If assistant not found or error occurs
    """
    try:
        db = Database.get_db()
        assistants_collection = db['assistants']

        logger.info(f"Updating AI assistant: {assistant_id}")

        # Convert to ObjectId
        try:
            assistant_obj_id = ObjectId(assistant_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid assistant_id format"
            )

        # Check if assistant exists
        assistant = assistants_collection.find_one({"_id": assistant_obj_id})
        if not assistant:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AI assistant not found"
            )

        # Build update document
        update_doc = {"updated_at": datetime.utcnow()}

        if update_data.name is not None:
            update_doc["name"] = update_data.name
        if update_data.system_message is not None:
            update_doc["system_message"] = update_data.system_message
        if update_data.voice is not None:
            update_doc["voice"] = update_data.voice
        if update_data.temperature is not None:
            update_doc["temperature"] = update_data.temperature

        # Update the assistant
        assistants_collection.update_one(
            {"_id": assistant_obj_id},
            {"$set": update_doc}
        )

        # Fetch updated assistant
        updated_assistant = assistants_collection.find_one({"_id": assistant_obj_id})

        logger.info(f"AI assistant {assistant_id} updated successfully")

        return AIAssistantResponse(
            id=str(updated_assistant['_id']),
            user_id=str(updated_assistant['user_id']),
            name=updated_assistant['name'],
            system_message=updated_assistant['system_message'],
            voice=updated_assistant['voice'],
            temperature=updated_assistant['temperature'],
            created_at=updated_assistant['created_at'].isoformat() + "Z",
            updated_at=updated_assistant['updated_at'].isoformat() + "Z"
        )

    except HTTPException:
        raise
    except Exception as error:
        import traceback
        logger.error(f"Error updating AI assistant: {str(error)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update AI assistant: {str(error)}"
        )

@router.delete("/{assistant_id}", response_model=DeleteResponse, status_code=status.HTTP_200_OK)
async def delete_assistant(assistant_id: str):
    """
    Delete an AI assistant

    Args:
        assistant_id: Assistant ID

    Returns:
        DeleteResponse: Success message

    Raises:
        HTTPException: If assistant not found or error occurs
    """
    try:
        db = Database.get_db()
        assistants_collection = db['assistants']

        logger.info(f"Deleting AI assistant: {assistant_id}")

        # Convert to ObjectId
        try:
            assistant_obj_id = ObjectId(assistant_id)
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid assistant_id format"
            )

        # Delete the assistant
        result = assistants_collection.delete_one({"_id": assistant_obj_id})

        if result.deleted_count == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="AI assistant not found"
            )

        logger.info(f"AI assistant {assistant_id} deleted successfully")

        return DeleteResponse(message="AI assistant deleted successfully")

    except HTTPException:
        raise
    except Exception as error:
        import traceback
        logger.error(f"Error deleting AI assistant: {str(error)}")
        logger.error(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete AI assistant: {str(error)}"
        )
