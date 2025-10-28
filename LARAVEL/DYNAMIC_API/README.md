

---

```markdown
# 🧩 Dynamic API Controller (Laravel)

This API provides **dynamic CRUD operations** (`insert`, `update`, `delete`, `get`) for **any database table** without writing separate controllers or models.

It allows developers to perform database actions quickly using simple **JSON requests**.

---

## 🚀 Base URL

```

/api/dynamic_api/{table}/{type}

```

| Parameter | Description |
|------------|-------------|
| `{table}`  | The name of the database table (e.g., `test_table`) |
| `{type}`   | One of: `insert`, `update`, `delete`, `get` |

---

## 🧱 Example Table: `test_table`

| Field   | Type         | Attributes       | Description |
|----------|--------------|------------------|--------------|
| `id`     | `INT(11)`    | Primary, Auto Increment | Record ID |
| `name`   | `VARCHAR(200)` | NOT NULL | Person’s name |
| `email`  | `VARCHAR(200)` | NOT NULL | Email address |
| `address`| `TEXT`       | NOT NULL | Address info |

---

## 📥 1. INSERT Data

**Endpoint:**
```

POST /api/dynamic_api/test_table/insert

````

**Request Body (JSON):**
```json
{
  "data": {
    "name": "John Doe",
    "email": "john@example.com",
    "address": "123 Main Street, New York"
  }
}
````

**Success Response:**

```json
{
  "status": "success",
  "message": "Data inserted successfully.",
  "inserted_id": 5
}
```

**Error Response:**

```json
{
  "status": "error",
  "message": "Data is required for insert operation."
}
```

---

## ✏️ 2. UPDATE Data

**Endpoint:**

```
POST /api/dynamic_api/test_table/update
```

**Request Body (JSON):**

```json
{
  "primary_key_field": "id",
  "primary_key_value": 5,
  "data": {
    "name": "Jane Doe",
    "address": "456 Park Avenue, New York"
  }
}
```

**Success Response:**

```json
{
  "status": "success",
  "message": "Data updated successfully."
}
```

**Error Response (missing fields):**

```json
{
  "status": "error",
  "message": "Primary key field, value, and data are required for update operation."
}
```

**Error Response (no match):**

```json
{
  "status": "error",
  "message": "No record updated."
}
```

---

## ❌ 3. DELETE Data

**Endpoint:**

```
POST /api/dynamic_api/test_table/delete
```

**Request Body (JSON):**

```json
{
  "primary_key_field": "id",
  "primary_key_value": 5
}
```

**Success Response:**

```json
{
  "status": "success",
  "message": "Record deleted successfully."
}
```

**Error Response:**

```json
{
  "status": "error",
  "message": "No record found to delete."
}
```

---

## 🔍 4. GET Data

**Endpoint:**

```
POST /api/dynamic_api/test_table/get
```

---

### a) Get All Records (with limit)

**Request Body (JSON):**

```json
{
  "limit": 10
}
```

**Response:**

```json
{
  "status": "success",
  "count": 3,
  "data": [
    {
      "id": 1,
      "name": "Jane Doe",
      "email": "jane@example.com",
      "address": "456 Park Avenue, New York"
    },
    {
      "id": 2,
      "name": "Alice",
      "email": "alice@example.com",
      "address": "London"
    }
  ]
}
```

---

### b) Get by Primary Key

**Request Body (JSON):**

```json
{
  "primary_key_field": "id",
  "primary_key_value": 1
}
```

**Response:**

```json
{
  "status": "success",
  "count": 1,
  "data": [
    {
      "id": 1,
      "name": "Jane Doe",
      "email": "jane@example.com",
      "address": "456 Park Avenue, New York"
    }
  ]
}
```

---

### c) Get by Filters

**Request Body (JSON):**

```json
{
  "filters": {
    "name": "Alice"
  }
}
```

**Response:**

```json
{
  "status": "success",
  "count": 1,
  "data": [
    {
      "id": 2,
      "name": "Alice",
      "email": "alice@example.com",
      "address": "London"
    }
  ]
}
```

---

## ⚙️ Error Handling

| Error Type          | Example Message                                                    |
| ------------------- | ------------------------------------------------------------------ |
| Missing Parameters  | `"Table name and type are required in the URL."`                   |
| Invalid Action      | `"Invalid action type. Use insert/update/delete/get."`             |
| Missing Data        | `"Data is required for insert operation."`                         |
| Missing Primary Key | `"Primary key field and value are required for delete operation."` |

---

## 🧠 Notes

* Works for any table name passed in `{table}`.
* Requires valid JSON body with appropriate fields.
* Always use `POST` requests for all operations.
* Responses are always in **JSON** format.

---

## 🧑‍💻 Example cURL Request

```bash
curl -X POST http://yourdomain.com/api/dynamic_api/test_table/insert \
     -H "Content-Type: application/json" \
     -d '{
           "data": {
             "name": "John Doe",
             "email": "john@example.com",
             "address": "123 Main Street, NY"
           }
         }'
```

**Response:**

```json
{
  "status": "success",
  "message": "Data inserted successfully.",
  "inserted_id": 1
}
```

---

## 🏗️ Author

**DynamicController** by [Your Name]
📦 Built with **Laravel + DB Facade**

---

```
```
