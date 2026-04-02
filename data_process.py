import os
import json
import mysql.connector

BASE_PATH = "data"   # your extracted pulse data folder

# ------------------------------
# MySQL Connection
# ------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="phonepe_pulse"
)

cursor = conn.cursor()


# ------------------------------
# Utility Functions
# ------------------------------
def read_json(path):
    try:
        with open(path, 'r') as f:
            return json.load(f)
    except:
        return None


# Handles both state + india level
def extract_details(path):
    parts = path.replace("\\", "/").lower().split("/")

    try:
        if "state" in parts:
            idx = parts.index("state")
            state = parts[idx + 1]
            year = int(parts[idx + 2])
            quarter = int(parts[idx + 3].replace(".json", ""))
        else:
            state = "india"
            idx = parts.index("india")
            year = int(parts[idx + 1])
            quarter = int(parts[idx + 2].replace(".json", ""))

        return state, year, quarter

    except Exception as e:
        print(f"Path parsing error: {path} -> {e}")
        return None, None, None


#Proper category detection
def get_category(path):
    parts = path.replace("\\", "/").lower().split("/")

    if "insurance" in parts:
        return "insurance"
    elif "transaction" in parts:
        return "transaction"
    else:
        return None


# ------------------------------
# INSERT HELPER
# ------------------------------
"""def insert_many(query, data):
    if data:
        cursor.executemany(query, data)
        conn.commit()"""

def insert_many(query, data):
    if not data:
        print("⚠️ No data to insert")
        return

    print(f"➡️ Trying to insert {len(data)} rows")

    for i, row in enumerate(data):
        try:
            cursor.execute(query, row)
        except Exception as e:
            print("\n❌ FAILED AT ROW:", i)
            print("❌ DATA:", row)
            print("❌ ERROR:", e)
            return  # stop immediately

    conn.commit()
    print(f"✅ Successfully inserted {len(data)} rows")


# =========================================================
# 1. AGGREGATED
# =========================================================
def process_aggregated():
    txn_data = []
    user_data = []
    device_data = []

    base = os.path.join(BASE_PATH, "aggregated")

    for root, _, files in os.walk(base):
        for file in files:
            if not file.endswith(".json"):
                continue

            path = os.path.join(root, file)
            data = read_json(path)

            # ✅ NULL safety
            if not data or not data.get("data"):
                continue

            state, year, quarter = extract_details(path)
            if not state:
                continue

            # =============================
            # TRANSACTION / INSURANCE
            # =============================
            category = get_category(path)

            if category and data["data"].get("transactionData"):
                for item in data["data"]["transactionData"]:
                    for pi in item.get("paymentInstruments", []):
                        txn_data.append((
                            state,
                            year,
                            quarter,
                            item.get("name"),
                            pi.get("count", 0) or 0,
                            pi.get("amount", 0) or 0,
                            category
                        ))

            # =============================
            # USER SUMMARY
            # =============================
            if data["data"].get("aggregated"):
                agg = data["data"]["aggregated"]
                user_data.append((
                    state,
                    year,
                    quarter,
                    agg.get("registeredUsers", 0) or 0,
                    agg.get("appOpens", 0) or 0
                ))

            # =============================
            # USER DEVICE
            # =============================
            if data["data"].get("usersByDevice"):
                for d in data["data"]["usersByDevice"]:
                    device_data.append((
                        state,
                        year,
                        quarter,
                        d.get("brand"),
                        d.get("count"),
                        d.get("percentage")
                    ))

    # ---------------- INSERT ----------------
    insert_many("""
        INSERT INTO aggregated_transaction_insurance
        (state, year, quarter, type, count, amount, category)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, txn_data)

    insert_many("""
        INSERT INTO aggregated_user
        (state, year, quarter, registeredUsers, appOpens)
        VALUES (%s,%s,%s,%s,%s)
    """, user_data)

    insert_many("""
        INSERT INTO aggregated_user_device
        (state, year, quarter, brand, count, percentage)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, device_data)


# =========================================================
# 2. MAP
# =========================================================
def process_map():
    txn_data = []
    user_data = []

    base = os.path.join(BASE_PATH, "map")

    for root, _, files in os.walk(base):
        for file in files:
            if not file.endswith(".json"):
                continue

            path = os.path.join(root, file)
            data = read_json(path)

            if not data or not data.get("data"):
                continue

            state, year, quarter = extract_details(path)
            if not state:
                continue

            # ---- TRANSACTION / INSURANCE ----
            if data["data"].get("hoverDataList"):
                for item in data["data"]["hoverDataList"]:
                    metric = item.get("metric", [{}])[0]
                    txn_data.append((
                        state or "",
                        int(year) if year else 0,
                        int(quarter) if quarter else 0,
                        item.get("name") or "",
                        int(metric.get("count", 0) or 0),
                        float(metric.get("amount", 0) or 0)
                    ))

            # ---- USER ----
            if data["data"].get("hoverData"):
                for district, val in data["data"]["hoverData"].items():
                    user_data.append((
                        state,
                        year,
                        quarter,
                        district,
                        int(val.get("registeredUsers", 0) or 0),
                        int(val.get("appOpens", 0) or 0)
                    ))

    # INSERT
    insert_many("""
        INSERT INTO map_transaction_insurance
        (state, year, quarter, district, count, amount)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, txn_data)

    insert_many("""
        INSERT INTO map_user
        (state, year, quarter, district, registeredUsers, appOpens)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, user_data)


# =========================================================
# 3. TOP
# =========================================================
def process_top():
    txn_data = []
    user_data = []

    base = os.path.join(BASE_PATH, "top")

    for root, _, files in os.walk(base):
        for file in files:
            if not file.endswith(".json"):
                continue

            path = os.path.join(root, file)
            data = read_json(path)

            if not data or not data.get("data"):
                continue

            state, year, quarter = extract_details(path)
            if not state:
                continue

            for key in ["states", "districts", "pincodes"]:
                if data["data"].get(key):

                    for item in data["data"][key]:

                        # ---- TRANSACTION / INSURANCE ----
                        if "metric" in item:
                            metric = item["metric"]
                            txn_data.append((
                                state,
                                year,
                                quarter,
                                key,
                                item.get("entityName") or item.get("name"),
                                metric.get("count", 0) or 0,
                                metric.get("amount", 0) or 0
                            ))

                        # ---- USER ----
                        if "registeredUsers" in item:
                            user_data.append((
                                state,
                                year,
                                quarter,
                                key,
                                item.get("name"),
                                item.get("registeredUsers", 0) or 0
                            ))

    # INSERT
    insert_many("""
        INSERT INTO top_transaction_insurance
        (state, year, quarter, type, name, count, amount)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, txn_data)

    insert_many("""
        INSERT INTO top_user
        (state, year, quarter, type, name, registeredUsers)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, user_data)


# =========================================================
# MAIN RUN
# =========================================================
if __name__ == "__main__":
    print("Processing Aggregated...")
    #process_aggregated()

    print("Processing Map...")
    process_map()

    print("Processing Top...")
    process_top()

    cursor.close()
    conn.close()

    print("✅ DATA INSERTED INTO MYSQL SUCCESSFULLY")