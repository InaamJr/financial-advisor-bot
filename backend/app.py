from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # ✅ Allow all origins temporarily for dev

# If you want to restrict in production, use:
# CORS(app, resources={r"/advice": {"origins": "http://localhost:5173"}})
print("✅ This is the correct app.py running")

@app.route("/advice", methods=["POST"])
def get_advice():
    from data.fetch_stock_data import get_stock_data
    from strategies.basic_strategy import apply_moving_average_strategy
    from strategies.q_learning_strategy import QLearningTrader
    from engine.advisor import generate_advice

    data = request.get_json()
    symbol = data.get("symbol", "").upper().strip()

    # ✅ Fix Yahoo-style symbols (e.g., BRK-B → BRK.B)
    if symbol == "BRK-B":
        symbol = "BRK.B"

    # ✅ Reject malformed inputs
    if not symbol or not (symbol.replace(".", "").isalpha() and len(symbol) <= 10):
        return jsonify({"message": f"'{symbol}' is not a valid stock symbol."}), 400

    try:
        stock_df = get_stock_data(symbol, period="6mo")

        # ✅ Check if stock data exists
        if stock_df.empty or 'close' not in stock_df.columns:
            return jsonify({"message": f"No valid stock data found for {symbol}."}), 404

        stock_df = apply_moving_average_strategy(stock_df)

        q_bot = QLearningTrader()
        stock_df = q_bot.train(stock_df, episodes=20)

        if not stock_df.empty and 'signal' in stock_df.columns:
            advice = generate_advice(stock_df, symbol=symbol)
            return jsonify({"message": advice})
        else:
            return jsonify({"message": f"No signal data available for {symbol}."}), 204

    except Exception as e:
        print(f"[ERROR] {e}")
        return jsonify({"message": f"Error generating advice for {symbol}."}), 500


@app.route("/evaluate", methods=["POST"])
def evaluate_strategy():
    from data.fetch_stock_data import get_stock_data
    from strategies.basic_strategy import apply_moving_average_strategy
    from evaluation.backtester import backtest_strategy

    data = request.get_json()
    symbol = data.get("symbol", "").upper()

    if not symbol:
        return jsonify({"message": "No symbol provided."}), 400

    try:
        # 🧪 Step 1: Fetch data
        stock_df = get_stock_data(symbol, period="6mo")
        print(f"[DEBUG] Fetched data for {symbol}, shape: {stock_df.shape}")

        # 🧪 Step 2: Apply strategy
        stock_df = apply_moving_average_strategy(stock_df)
        print(f"[DEBUG] After strategy applied, columns: {stock_df.columns.tolist()}")

        # ❗ Check if signals are available
        if stock_df.empty or 'signal' not in stock_df.columns:
            print(f"[DEBUG] No usable signals found for {symbol}. Sample:\n{stock_df.head()}")
            return jsonify({"message": "No signal data available."}), 204

        # 🧪 Step 3: Run backtest
        print(f"[DEBUG] Running backtest for {symbol}...")
        summary, trades, equity = backtest_strategy(stock_df)

        return jsonify({
            "summary": summary,
            "trades": trades.to_dict(orient="records"),
            "equity": equity.to_dict(orient="records")
        })

    except Exception as e:
        print(f"[ERROR] Evaluation failed for {symbol}: {e}")
        return jsonify({"message": "Evaluation failed."}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5050)
