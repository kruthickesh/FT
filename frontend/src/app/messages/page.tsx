"use client";
import { useState, useEffect } from "react";
import { useAuth } from "@/lib/auth";
import { apiRequest } from "@/lib/utils";
import { Card, CardContent } from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Button } from "@/components/ui/button";
import { Message } from "@/types";

export default function MessagesPage() {
  const { user, loading } = useAuth();
  const [conversations, setConversations] = useState<any[]>([]);
  const [selectedUser, setSelectedUser] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [newMessage, setNewMessage] = useState("");
  const [sending, setSending] = useState(false);

  useEffect(() => {
    if (user) loadConversations();
  }, [user]);

  useEffect(() => {
    if (selectedUser) loadMessages();
  }, [selectedUser]);

  const loadConversations = async () => {
    try {
      const data = await apiRequest("/messages/conversations");
      setConversations(data);
    } catch {}
  };

  const loadMessages = async () => {
    if (!selectedUser) return;
    try {
      const data = await apiRequest(`/messages/${selectedUser}`);
      setMessages(data);
    } catch {}
  };

  const sendMessage = async () => {
    if (!newMessage.trim() || !selectedUser) return;
    setSending(true);
    try {
      await apiRequest("/messages/", {
        method: "POST",
        body: JSON.stringify({ receiver_id: selectedUser, content: newMessage })
      });
      setNewMessage("");
      loadMessages();
      loadConversations();
    } catch (err: any) { alert(err.message); }
    finally { setSending(false); }
  };

  if (loading) return <div className="min-h-screen flex items-center justify-center">Loading...</div>;

  return (
    <div className="min-h-screen bg-gray-50 flex">
      <div className="w-80 bg-white border-r">
        <div className="p-4 border-b"><h2 className="text-xl font-bold">Messages</h2></div>
        <div className="overflow-y-auto h-[calc(100vh-65px)]">
          {conversations.length === 0 ? (<p className="p-4 text-gray-500 text-center">No conversations</p>) : (
            conversations.map((c) => (
              <div key={c.user_id} onClick={() => setSelectedUser(c.user_id)} className={`p-4 border-b cursor-pointer hover:bg-gray-50 ${selectedUser === c.user_id ? 'bg-primary/5' : ''}`}>
                <div className="flex justify-between"><span className="font-semibold">{c.user_name}</span>{c.unread_count > 0 && <span className="bg-primary text-white text-xs px-2 py-0.5 rounded-full">{c.unread_count}</span>}</div>
                <p className="text-sm text-gray-500 truncate">{c.last_message}</p>
              </div>
            ))
          )}
        </div>
      </div>
      <div className="flex-1 flex flex-col">
        {selectedUser ? (
          <>
            <div className="flex-1 overflow-y-auto p-4 space-y-4">
              {messages.map((m) => (
                <div key={m.id} className={`flex ${m.sender_id === user?.id ? 'justify-end' : 'justify-start'}`}>
                  <div className={`max-w-xs px-4 py-2 rounded-lg ${m.sender_id === user?.id ? 'bg-primary text-white' : 'bg-white'}`}>{m.content}</div>
                </div>
              ))}
            </div>
            <div className="p-4 border-t bg-white flex gap-2">
              <Input value={newMessage} onChange={e => setNewMessage(e.target.value)} placeholder="Type a message..." onKeyDown={e => e.key === 'Enter' && sendMessage()} />
              <Button onClick={sendMessage} disabled={sending}>Send</Button>
            </div>
          </>
        ) : (
          <div className="flex-1 flex items-center justify-center text-gray-500">Select a conversation to start messaging</div>
        )}
      </div>
    </div>
  );
}