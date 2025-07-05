from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
import os
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = MongoClient(MONGO_URI)
db = client["webhookDB"]
collection = db["events"]

@app.route("/")
def index():
    return "✅ Flask server is running and connected to MongoDB"

@app.route("/webhook", methods=["POST"])
def webhook():
    event_type = request.headers.get("X-GitHub-Event")
    data = request.get_json()

    print(f"📩 Received event: {event_type}")
    print("🧾 Raw payload:", data)

    timestamp = datetime.utcnow().strftime("%d %B %Y - %I:%M %p UTC")
    message = None

    try:
        if event_type == "push":
            print("📦 Handling PUSH event")
            author = data.get("pusher", {}).get("name", "unknown")
            ref = data.get("ref", "")
            print(f"🔍 Pusher: {author}, Ref: {ref}")

            if not ref:
                raise ValueError("Missing ref in push event")
            to_branch = ref.split("/")[-1]
            message = f"{author} pushed to {to_branch} on {timestamp}"

        elif event_type == "pull_request":
            action = data.get("action")
            author = data.get("sender", {}).get("login", "unknown")
            from_branch = data.get("pull_request", {}).get("head", {}).get("ref")
            to_branch = data.get("pull_request", {}).get("base", {}).get("ref")

            print(f"📦 Handling PULL REQUEST: {action}")
            print(f"🔍 From: {from_branch} → To: {to_branch} by {author}")

            if action == "opened":
                message = f"{author} submitted a pull request from {from_branch} to {to_branch} on {timestamp}"
            elif action == "closed" and data.get("pull_request", {}).get("merged"):
                message = f"{author} merged branch {from_branch} to {to_branch} on {timestamp}"

        if message:
            collection.insert_one({"message": message, "timestamp": timestamp})
            print("✅ Event saved to MongoDB:", message)
            return "Event saved", 200
        else:
            print("⚠️ No valid message constructed. Event ignored.")
            return "Event ignored", 200

    except Exception as e:
        print("❌ Error during event handling:", e)
        return "Internal server error", 500

@app.route("/events", methods=["GET"])
def get_events():
    try:
        events = list(collection.find({}, {"_id": 0}))
        print(f"📤 Returning {len(events)} event(s)")
        return jsonify(events)
    except Exception as e:
        print("❌ Failed to fetch events:", e)
        return jsonify([])

if __name__ == "__main__":
    app.run(debug=True)
