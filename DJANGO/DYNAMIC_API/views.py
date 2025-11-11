import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection


@csrf_exempt
def dynamic_api(request, table, type):
    type = type.lower()

    if not table or not type:
        return JsonResponse({
            'status': 'error',
            'message': 'Table name and type are required in the URL.'
        }, status=400)

    try:
        data = json.loads(request.body.decode('utf-8') or '{}')
    except json.JSONDecodeError:
        data = {}

    data['table'] = table

    if type == 'insert':
        return insert_action(data)
    elif type == 'update':
        return update_action(data)
    elif type == 'delete':
        return delete_action(data)
    elif type == 'get':
        return get_action(data)
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid action type. Use insert/update/delete/get.'
        }, status=400)


# -------------------------------
# INSERT ACTION
# -------------------------------
def insert_action(data):
    table = data.get('table')
    values = data.get('data')

    if not values or not isinstance(values, dict):
        return JsonResponse({
            'status': 'error',
            'message': 'Data is required for insert operation.'
        }, status=400)

    columns = ', '.join(values.keys())
    placeholders = ', '.join(['%s'] * len(values))
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"

    with connection.cursor() as cursor:
        cursor.execute(sql, list(values.values()))
        inserted_id = cursor.lastrowid

    return JsonResponse({
        'status': 'success',
        'message': 'Data inserted successfully.',
        'inserted_id': inserted_id
    })


# -------------------------------
# UPDATE ACTION
# -------------------------------
def update_action(data):
    table = data.get('table')
    pk_field = data.get('primary_key_field')
    pk_value = data.get('primary_key_value')
    update_data = data.get('data')

    if not pk_field or pk_value is None or not update_data:
        return JsonResponse({
            'status': 'error',
            'message': 'Primary key field, value, and data are required for update operation.'
        }, status=400)

    set_clause = ', '.join([f"{k}=%s" for k in update_data.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE {pk_field}=%s"

    with connection.cursor() as cursor:
        cursor.execute(sql, list(update_data.values()) + [pk_value])
        updated = cursor.rowcount

    return JsonResponse({
        'status': 'success' if updated else 'error',
        'message': 'Data updated successfully.' if updated else 'No record updated.'
    })


# -------------------------------
# DELETE ACTION
# -------------------------------
def delete_action(data):
    table = data.get('table')
    pk_field = data.get('primary_key_field')
    pk_value = data.get('primary_key_value')

    if not pk_field or pk_value is None:
        return JsonResponse({
            'status': 'error',
            'message': 'Primary key field and value are required for delete operation.'
        }, status=400)

    sql = f"DELETE FROM {table} WHERE {pk_field}=%s"

    with connection.cursor() as cursor:
        cursor.execute(sql, [pk_value])
        deleted = cursor.rowcount

    return JsonResponse({
        'status': 'success' if deleted else 'error',
        'message': 'Record deleted successfully.' if deleted else 'No record found to delete.'
    })


# -------------------------------
# GET ACTION
# -------------------------------
def get_action(data):
    table = data.get('table')
    pk_field = data.get('primary_key_field')
    pk_value = data.get('primary_key_value')
    filters = data.get('filters', {})
    limit = data.get('limit', 10)

    where_clauses = []
    params = []

    if pk_field and pk_value is not None:
        where_clauses.append(f"{pk_field}=%s")
        params.append(pk_value)

    for field, value in filters.items():
        where_clauses.append(f"{field}=%s")
        params.append(value)

    where_sql = f"WHERE {' AND '.join(where_clauses)}" if where_clauses else ""
    sql = f"SELECT * FROM {table} {where_sql} LIMIT %s"
    params.append(limit)

    with connection.cursor() as cursor:
        cursor.execute(sql, params)
        columns = [col[0] for col in cursor.description]
        rows = [dict(zip(columns, row)) for row in cursor.fetchall()]

    return JsonResponse({
        'status': 'success',
        'count': len(rows),
        'data': rows
    })
