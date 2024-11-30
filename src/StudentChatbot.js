import React, { useState } from 'react';
import { Send, Info } from 'lucide-react';

const StudentChatbot = () => {
  const [messages, setMessages] = useState([
    { 
      text: "Hello! I'm your Student Information Chatbot. Ask me about student details like roll number, CGPA, projects, and more.", 
      type: 'bot' 
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage = { text: inputMessage, type: 'user' };
    setMessages(prevMessages => [...prevMessages, userMessage]);
    
    const currentQuery = inputMessage;
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('http://127.0.0.1:5000/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: currentQuery })
      });

      const data = await response.json();
      
      setMessages(prevMessages => [
        ...prevMessages, 
        { text: data.response || "I couldn't understand that query.", type: 'bot' }
      ]);
    } catch (error) {
      setMessages(prevMessages => [
        ...prevMessages, 
        { text: "Sorry, there was an error processing your request.", type: 'bot' }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-md mx-auto h-[600px] bg-white shadow-lg rounded-xl flex flex-col">
      <div className="bg-indigo-600 text-white p-4 rounded-t-xl flex items-center">
        <Info className="mr-2" />
        <h2 className="font-bold text-lg">Student Information Chatbot</h2>
      </div>

      <div className="flex-grow overflow-y-auto p-4 space-y-3">
        {messages.map((message, index) => (
          <div 
            key={index}
            className={`p-3 rounded-lg max-w-[80%] ${
              message.type === 'user' 
                ? 'bg-indigo-100 text-indigo-800 self-end ml-auto' 
                : 'bg-gray-100 text-gray-800 self-start mr-auto'
            }`}
          >
            {message.text}
          </div>
        ))}
        {isLoading && (
          <div className="text-center text-gray-500 italic">
            Thinking...
          </div>
        )}
      </div>

      <div className="p-4 border-t flex">
        <input 
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Ask about a student or introduce yourself."
          className="flex-grow p-2 border rounded-l-lg focus:outline-none focus:ring-2 focus:ring-indigo-500"
        />
        <button 
          onClick={handleSendMessage}
          disabled={isLoading}
          className="bg-indigo-600 text-white p-2 rounded-r-lg hover:bg-indigo-700 disabled:opacity-50 transition-colors"
        >
          <Send size={20} />
        </button>
      </div>
    </div>
  );
};

export default StudentChatbot;
