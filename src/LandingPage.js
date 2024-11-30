import React from 'react';
import { ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-600 to-purple-700 flex items-center justify-center p-4">
      <div className="bg-white rounded-xl shadow-2xl p-8 w-full max-w-md text-center transform transition-all duration-300 hover:scale-105">
        <h1 className="text-3xl font-bold text-indigo-800 mb-6">3/4 CSM Chatbot</h1>
        
        <div className="mb-6">
          <h2 className="text-xl font-semibold text-gray-700 mb-4">Team Members</h2>
          <div className="space-y-2 text-gray-600">
            <p>S Sai Prasad</p>
            <p>M Pranitham</p>
            <p>Vishnu Vardhan</p>
            <p>Revanth</p>
          </div>
        </div>
        
        <Link 
          to="/chatbot"
          className="flex items-center justify-center w-full bg-indigo-600 text-white py-3 rounded-lg hover:bg-indigo-700 transition-colors group"
        >
          Enter Chatbot
          <ArrowRight 
            className="ml-2 group-hover:translate-x-1 transition-transform" 
            size={24} 
          />
        </Link>
      </div>
    </div>
  );
};

export default LandingPage;