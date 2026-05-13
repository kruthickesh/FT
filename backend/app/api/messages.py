from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from uuid import UUID
from typing import List
from ..core.database import get_db
from ..schemas import MessageCreate, MessageResponse
from ..models import Message, User
from .auth import get_current_user

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/", response_model=MessageResponse)
async def send_message(message: MessageCreate, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    receiver = db.query(User).filter(User.id == message.receiver_id).first()
    if not receiver:
        raise HTTPException(status_code=404, detail="Receiver not found")

    db_message = Message(
        sender_id=current_user.id,
        receiver_id=message.receiver_id,
        content=message.content
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/conversations", response_model=List[dict])
async def get_conversations(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    sent = db.query(Message).filter(Message.sender_id == current_user.id).all()
    received = db.query(Message).filter(Message.receiver_id == current_user.id).all()
    
    user_ids = set()
    for m in sent:
        user_ids.add(m.receiver_id)
    for m in received:
        user_ids.add(m.sender_id)
    
    conversations = []
    for uid in user_ids:
        user = db.query(User).filter(User.id == uid).first()
        last_msg = db.query(Message).filter(
            ((Message.sender_id == current_user.id) & (Message.receiver_id == uid)) |
            ((Message.sender_id == uid) & (Message.receiver_id == current_user.id))
        ).order_by(Message.created_at.desc()).first()
        unread = db.query(Message).filter(
            Message.sender_id == uid,
            Message.receiver_id == current_user.id,
            Message.is_read == False
        ).count()
        conversations.append({
            "user_id": str(uid),
            "user_name": user.full_name if user else "Unknown",
            "avatar_url": user.avatar_url if user else None,
            "last_message": last_msg.content if last_msg else "",
            "last_message_time": last_msg.created_at if last_msg else None,
            "unread_count": unread
        })
    
    conversations.sort(key=lambda x: x["last_message_time"] or "", reverse=True)
    return conversations

@router.get("/{user_id}", response_model=List[MessageResponse])
async def get_conversation(user_id: UUID, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    messages = db.query(Message).filter(
        ((Message.sender_id == current_user.id) & (Message.receiver_id == user_id)) |
        ((Message.sender_id == user_id) & (Message.receiver_id == current_user.id))
    ).order_by(Message.created_at.asc()).all()

    db.query(Message).filter(
        Message.sender_id == user_id,
        Message.receiver_id == current_user.id,
        Message.is_read == False
    ).update({"is_read": True})
    db.commit()

    return messages