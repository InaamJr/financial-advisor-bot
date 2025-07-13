import React, { useState, useRef, useEffect } from "react";

const ChatBot = ({ onNewSymbol }) => {
  const [messages, setMessages] = useState([
    {
      sender: "bot",
      text: "👋 Hey there! Ask me about any stock like AAPL or TSLA. I'm ready when you are!",
    },
  ]);

  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef(null);

  // 🧠 Extract stock symbol from natural language
  const extractSymbol = (sentence) => {
    const knownSymbols = ["AAPL", "TSLA", "MSFT", "GOOG", "AMZN", "NVDA", "NFLX", "NKE", "META", "IBM"];
    const words = sentence.toUpperCase().match(/\b[A-Z]{2,5}\b/g);
    if (!words) return null;
    const found = words.find((w) => knownSymbols.includes(w));
    return found || words[0]; // fallback
  };

  const sendMessage = async () => {
    if (!input.trim()) return;
  
    const userMessage = { sender: "user", text: input.trim() };
    setMessages((prev) => [...prev, userMessage]);
    setLoading(true);
    setIsTyping(true);
    setInput("");
  
    const symbol = extractSymbol(userMessage.text);
    if (!symbol) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: "❌ Hmm... I couldn't detect a stock symbol. Try something like 'Tell me about AAPL'.",
        },
      ]);
      setIsTyping(false);
      setLoading(false);
      return;
    }
  
    // 🔁 Send symbol to parent (App.jsx) for backtest use
    if (onNewSymbol) onNewSymbol(symbol);
  
    console.log("[DEBUG] Sending request for:", symbol);
  
    try {
      const res = await fetch("http://localhost:5050/advice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol }),
      });
  
      const contentType = res.headers.get("content-type") || "";
  
      if (!res.ok) {
        throw new Error(`Server responded with ${res.status}`);
      }
  
      // 🛡️ Validate JSON
      if (!contentType.includes("application/json")) {
        throw new Error("Invalid response format — expected JSON.");
      }
  
      const data = await res.json();
      console.log("[DEBUG] Bot response:", data);
  
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: data.message || "⚠️ Response was empty or malformed.",
        },
      ]);
    } catch (error) {
      console.error("[ERROR] Chat fetch failed:", error);
  
      setMessages((prev) => [
        ...prev,
        {
          sender: "bot",
          text: `🚫 Server error: ${error.message || "Unexpected error."}`,
        },
      ]);
    }
  
    setIsTyping(false);
    setLoading(false);
  };  

  const handleKeyDown = (e) => {
    if (e.key === "Enter") sendMessage();
  };

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isTyping]);

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 px-4">
      {/* Modern Card Container */}
      <div className="w-full max-w-2xl bg-white shadow-lg rounded-xl overflow-hidden flex flex-col h-[85vh] border border-gray-200 relative">
        {/* Professional Header with Gradient */}
        <div className="bg-gradient-to-r from-gray-900 to-gray-800 text-white py-5 px-6 text-xl font-semibold flex items-center">
          <div className="w-3 h-3 bg-green-400 rounded-full mr-2 animate-pulse"></div>
          <span className="ml-6">💼 Financial Advisor</span>
          <span className="ml-auto text-sm font-normal opacity-80">AI-powered</span>
        </div>

        {/* Enhanced Message Area */}
        <div className="flex-1 overflow-y-auto p-6 bg-gray-50">
          <div className="space-y-3">
            {messages.map((msg, i) => (
              <div 
                key={i} 
                className={`flex ${msg.sender === "user" ? "justify-end" : "justify-start"}`}
              >
                <div
                  className={`max-w-[85%] px-4 py-3 rounded-2xl text-sm leading-relaxed ${
                    msg.sender === "user"
                      ? "bg-gradient-to-br from-blue-500 to-blue-600 text-white rounded-br-none shadow-md"
                      : "bg-white text-gray-800 rounded-bl-none shadow-sm border border-gray-100"
                  } whitespace-pre-line transition-all duration-200`}
                >
                  {msg.text}
                </div>
              </div>
            ))}

            {/* Sleek Typing Indicator */}
            {isTyping && (
              <div className="flex justify-start">
                <div className="bg-white text-gray-500 text-xs px-4 py-2 rounded-2xl rounded-bl-none shadow border border-gray-100 flex items-center space-x-1">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></div>
                  </div>
                  <span>Analyzing...</span>
                </div>
              </div>
            )}

            <div ref={messagesEndRef} />
          </div>
        </div>

        {/* Premium Input Area */}
        <div className="border-t border-gray-200 bg-white p-4">
          <div className="flex items-center space-x-2 bg-gray-100 rounded-xl px-3 py-2 focus-within:ring-2 focus-within:ring-blue-400 focus-within:bg-white transition-all">
            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Ask about AAPL, TSLA, etc..."
              className="flex-1 bg-transparent border-none outline-none text-gray-700 placeholder-gray-400 text-sm py-2 px-2"
            />
            <button
              onClick={sendMessage}
              disabled={loading}
              className={`p-2 rounded-full ${
                loading 
                  ? "text-gray-400" 
                  : "text-white bg-blue-600 hover:bg-blue-700"
              } transition-all`}
            >
              {loading ? (
                <svg className="w-5 h-5 animate-spin" viewBox="0 0 24 24">
                  <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                  <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
                </svg>
              ) : (
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-8.707l-3-3a1 1 0 00-1.414 1.414L10.586 9H7a1 1 0 100 2h3.586l-1.293 1.293a1 1 0 101.414 1.414l3-3a1 1 0 000-1.414z" clipRule="evenodd" />
                </svg>
              )}
            </button>
          </div>
          <p className="text-xs text-gray-400 mt-2 text-center">
            Tip: Try "Show me TSLA trends" or "Analyze AAPL"
          </p>
        </div>
      </div>
    </div>
  );
};

export default ChatBot;
