# 📚 Prueba_Welli

## 🚀 Quick Start Instructions

1. 🌀 **Clone the repository:**
   ```sh
   git clone <URL_DEL_REPOSITORIO>
   cd Prueba_Welli
   ```

2. 🔑 **Give execution permissions to the start script (only the first time):**
   ```sh
   chmod +x start.sh
   ```

3. ▶️ **Run the project (this will install dependencies, populate the database, and start the server):**
   ```sh
   ./start.sh
   ```

✨ This will automatically install requirements, run the script to populate the database (`run.py`), and start the FastAPI server in development mode.

---

## ⏰ Automatic Job for Overdue Loan Fines

This project includes an **automatic job** that reviews all active loans daily and applies fines to users for overdue days:

- 📅 **First 30 days overdue:** $2,000 per day.
- 🔥 **From day 31:** $4,000 per day.
- 🛡️ The system tracks already fined days, so **the same fine is not charged twice** even if the job runs every day.

### 🛠️ How does it work?

- The job checks all active loans whose `end_date` has passed.
- Calculates overdue days and applies the corresponding fine only for new overdue days.
- Adds the fine to the user's `fines` field.
- Updates the `days_fined` field in the loan to keep track.

### ▶️ How to run it manually?

From the project root, run:

```sh
python3 -m app.cronjobs.pending_transactions
```

This will run the job once and show the applied fines in the console.

### ⏳ How to schedule automatic execution?

The file `app/cronjobs/pending_transactions.py` is set to run automatically every day at 1:00 AM using the `schedule` library.  
You can leave it running in the background with:

```sh
python3 -m app.cronjobs.pending_transactions
```

or schedule its daily execution using tools like **cron** on your server.

---

## 🕒 Reserved Stock Job for Pending Purchases

This project includes a **reserved stock job** that manages temporary stock reservations for pending purchases:

- 🛒 When a purchase is created, its status is set to `pending` and the stock is reserved for 1 minute (`reserved_until`).
- ⏳ The job checks for pending purchases whose reservation time has expired and randomly approves or rejects them (for testing purposes).
- ❌ If a purchase is rejected, the stock is returned to the book (for physical purchases).
- ✅ If approved, the stock remains reduced.

### ▶️ How to run the reserved stock job manually

From the project root, run:

```sh
python -m app.services.reserved_stock
```

This will:
1. 🛒 Reserve stock for all pending purchases that don't have a reservation.
2. ⚡ Immediately process any purchases whose reservation has expired.
3. 🔄 Continue checking every minute for 3 minutes, processing any new expired reservations.

💡 *You can adjust the reservation time and job frequency in `app/services/reserved_stock.py` for your testing needs.*
