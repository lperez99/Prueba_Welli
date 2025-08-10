# 📚 Prueba_Welli

## 🚀 Quick Start Instructions

1. 🌀 **Clone the repository:**
   ```sh
   git clone https://github.com/lperez99/Prueba_Welli
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

---

## 📉 Least Popular Books Job (Stock Reduction)

Every 6 months, the system runs a job that reviews all books and reduces the minimum stock for books **without any purchases (physical or digital) in the last 6 months**:

- 🔍 The job checks all books and counts their purchases in the last 6 months.
- 📉 If a book has **zero purchases** in that period, its `min_stock_for_sell` is reduced by 2.
- 🚫 The minimum stock will never go below 2 (it is set to 2 if the reduction would make it lower or negative).

### ▶️ How to run the least popular books job manually

From the project root, run:

```sh
python -m app.cronjobs.least_popular_book
```

This will:
1. 🔍 Review all books for purchases in the last 6 months.
2. 📉 Reduce the minimum stock for books with zero purchases.
3. 📝 Print the changes in the console for easy verification.

💡 *You can adjust the review period and reduction amount in `app/services/least_popular_book.py` for your needs.*

---

## ⏳ Job Scheduling in Production

In a real production environment, these jobs should be scheduled to run automatically using a task scheduler like **cron** (Linux/macOS) or Task Scheduler (Windows).  
Below are the recommended schedules for each job:

| Job                        | Frequency (Production)         | Example cron expression           | Description                                      |
|----------------------------|-------------------------------|-----------------------------------|--------------------------------------------------|
| Reserved Stock             | Every minute (infinite loop)  | `* * * * *`                       | Processes pending purchases and stock reservation |
| Most Popular Books         | 1st day of each month, 1:00AM | `0 1 1 * *`                       | Increases min stock for popular books            |
| Least Popular Books        | Every 6 months, 1:00AM        | `0 1 1 1,7 *`                     | Decreases min stock for least popular books      |
| Overdue Loan Fines         | Daily, 1:00AM                 | `0 1 * * *`                       | Applies fines for overdue loans                  |

> **Note:** For this technical test, you can run all jobs manually using the provided commands.  
> In production, add the appropriate cron lines to your server's crontab.

### 🛠️ Example: How to schedule jobs with cron (Linux/macOS)

Edit your crontab with `crontab -e` and add lines like these (replace `/path/to/project` with your actual path):

```cron
# Reserved Stock (every minute)
* * * * * cd /path/to/project && .venv/bin/python -m app.services.reserved_stock

# Most Popular Books (monthly)
0 1 1 * * cd /path/to/project && .venv/bin/python -m app.cronjobs.most_popular_book

# Least Popular Books (every 6 months)
0 1 1 1,7 * cd /path/to/project && .venv/bin/python -m app.cronjobs.least_popular_book

# Overdue Loan Fines (daily)
0 1 * * * cd /path/to/project && .venv/bin/python -m app.cronjobs.pending_transactions
```

---

**For the technical test:**  
You can run each job manually as described in the sections above.  
In production, use a scheduler to automate their execution at the recommended times.
