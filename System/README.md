# Financial Advisor Bot
An AI-powered financial assistant that provides BUY, SELL, or HOLD advice using a hybrid strategy that combines simple moving average (SMA) crossovers and reinforcement learning (Q-learning). Designed to be intuitive, explainable, and suitable for non-technical users, this project merges technical finance with user-friendly design.


## Features
- Q-Learning + SMA Crossover Strategy
    Blends traditional technical indicators with machine learning to generate informed signals.

- Real-time Backtesting with Equity Curve
    Simulates strategy performance on historical data and visualizes returns.

- Explanation Engine (XAI)
    Every recommendation includes a clear, human-readable explanation with a confidence score.

- Interactive Web Interface
    Chat-style UI with conversational queries and animated evaluation results.

## Tech Stack
- Backend: Python 3, Flask, yfinance, NumPy, Pandas
- Frontend: React.js, Tailwind CSS, Recharts
- Machine Learning: Tabular Q-learning agent
- Natural Language Generation: Custom explanation logic with optional LLM (Ollama) fallback
- Testing: Manual testing through browser and API validation

## Getting Started
1. Clone the repository:
    git clone https://github.com/your-username/finadvisor-bot.git
    cd finadvisor-bot

2. Install backend dependencies:
    pip install -r requirements.txt

3. Start the Flask backend:
    python app.py

4. Open a new terminal for frontend:
    cd client
    npm install
    npm run dev

5. Open your browser and navigate to http://localhost:5173

6. Type a stock symbol like:

7. The system will respond with:
    - BUY, SELL, or HOLD signal
    - A brief natural language explanation
    - An option to “Run Backtest” and view performance graphs

## License
MIT
