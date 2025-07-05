# Webhook Listener & GitHub Actions Demo

This project demonstrates a working GitHub **Webhook Listener** and **GitHub Actions CI/CD** integration as part of a two-repo setup:

- 🔧 `action-repo`: Contains GitHub Actions workflow that triggers on every push
- 📡 `webhook-repo`: Listens for webhook events from GitHub and displays them live on a frontend page

---

## 📁 Repository Structure

### 🔹 webhook-repo

- `index.js` – Node.js Express server to receive and store webhook events
- `ui.html` – Frontend UI to display incoming events (auto-refreshes every 3 seconds)
- `package.json` – Project dependencies (`express`, `body-parser`)
- `.github/workflows/ci.yml` – GitHub Actions workflow file (inside `action-repo`)

---

## 🚀 How to Run Locally

```bash
# 1. Install dependencies
npm install

# 2. Start the webhook server
node index.js
