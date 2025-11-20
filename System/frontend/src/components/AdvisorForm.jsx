import React, { useState } from "react";

const AdvisorForm = () => {
  const [symbol, setSymbol] = useState("");
  const [loading, setLoading] = useState(false);
  const [advice, setAdvice] = useState("");
  const [chatHistory, setChatHistory] = useState([]);
  const [isTyping, setIsTyping] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!symbol.trim()) return;

    const userMessage = { type: "user", text: symbol };
    setChatHistory((prev) => [...prev, userMessage]);
    setSymbol("");
    setLoading(true);
    setIsTyping(true);
    setAdvice("");

    try {
      const res = await fetch("http://localhost:5050/advice", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ symbol }),
      });

      const data = await res.json();
      const botMessage = { type: "bot", text: data.message || "No advice available." };
      setChatHistory((prev) => [...prev, botMessage]);
    } catch {
      const errorMsg = { type: "bot", text: "❌ Failed to get advice. Please try again." };
      setChatHistory((prev) => [...prev, errorMsg]);
    }

    setLoading(false);
    setIsTyping(false);
  };

  return (
    <div className="bg-white/70 backdrop-blur-md p-6 md:p-10 rounded-xl shadow-xl max-w-2xl w-full border border-gray-200">
      <h2 className="text-2xl md:text-3xl font-bold text-gray-800 mb-6 text-center tracking-tight">
        📊 Smart Investment Advisor
      </h2>

      <div className="overflow-y-auto max-h-96 mb-6 space-y-3">
        {chatHistory.map((msg, index) => (
          <div
            key={index}
            className={`px-5 py-3 rounded-lg w-fit max-w-[90%] whitespace-pre-line ${
              msg.type === "user"
                ? "ml-auto bg-blue-600 text-white"
                : "mr-auto bg-gray-100 text-gray-800"
            }`}
          >
            {msg.text}
          </div>
        ))}

        {isTyping && (
          <div className="mr-auto px-5 py-3 rounded-lg bg-gray-100 text-gray-500 animate-pulse">
            Bot is thinking...
          </div>
        )}
      </div>

      <form onSubmit={handleSubmit} className="flex space-x-4">
        <input
          type="text"
          value={symbol}
          onChange={(e) => setSymbol(e.target.value)}
          placeholder="Ask about a stock (e.g. AAPL)"
          className="flex-1 px-5 py-3 rounded-lg border border-gray-300 shadow-sm focus:outline-none focus:ring-2 focus:ring-blue-500 transition"
        />
        <button
          type="submit"
          disabled={loading}
          className="px-6 py-3 bg-blue-600 text-white font-semibold rounded-lg hover:bg-blue-700 transition disabled:opacity-60"
        >
          {loading ? "Analyzing..." : "Ask"}
        </button>
      </form>
    </div>
  );
};

export default AdvisorForm;
