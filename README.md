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

---

## 📈 Most Popular Books Job (Stock Increase)

This project includes a job that reviews all books **every month** and increases the minimum stock for books with high sales:

- 🔍 The job checks all books and counts their purchases (physical or digital) in the last month.
- 📈 If a book has **more than 10 purchases** in that period, its `min_stock_for_sell` is increased by 3.
- 📝 The change is printed in the console for easy verification.

### ▶️ How to run the most popular books job manually

From the project root, run:

```sh
python -m app.cronjobs.most_popular_book
```

This will:
1. 🔍 Review all books for purchases in the last month.
2. 📈 Increase the minimum stock for books with more than 10 purchases.
3. 📝 Print the changes in the console for easy verification.

💡 *You can adjust the review period and increase amount in `app/services/most_popular_book.py` for your needs.*
