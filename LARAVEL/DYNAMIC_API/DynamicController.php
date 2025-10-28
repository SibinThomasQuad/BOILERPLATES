<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;

class DynamicController extends Controller
{
    /**
     * Main dynamic handler
     * URL format: /api/dynamic_api/{table}/{type}
     */
    public function handle(Request $request, $table, $type)
    {
        $type = strtolower($type);

        if (!$table || !$type) {
            return response()->json([
                'status' => 'error',
                'message' => 'Table name and type are required in the URL.'
            ], 400);
        }

        switch ($type) {
            case 'insert':
                $action = new InsertAction();
                break;
            case 'update':
                $action = new UpdateAction();
                break;
            case 'delete':
                $action = new DeleteAction();
                break;
            case 'get':
                $action = new GetAction();
                break;
            default:
                return response()->json([
                    'status' => 'error',
                    'message' => 'Invalid action type. Use insert/update/delete/get.'
                ], 400);
        }

        // Attach table to request
        $request->merge(['table' => $table]);

        return $action->execute($request);
    }
}

/*-----------------------------------------------
| INSERT ACTION
-----------------------------------------------*/
class InsertAction
{
    public function execute(Request $request)
    {
        $table = $request->input('table');
        $data = $request->input('data');

        if (!$data || !is_array($data)) {
            return response()->json([
                'status' => 'error',
                'message' => 'Data is required for insert operation.'
            ], 400);
        }

        $id = DB::table($table)->insertGetId($data);

        return response()->json([
            'status' => 'success',
            'message' => 'Data inserted successfully.',
            'inserted_id' => $id
        ]);
    }
}

/*-----------------------------------------------
| UPDATE ACTION
-----------------------------------------------*/
class UpdateAction
{
    public function execute(Request $request)
    {
        $table = $request->input('table');
        $primaryKeyField = $request->input('primary_key_field');
        $primaryKeyValue = $request->input('primary_key_value');
        $data = $request->input('data');

        if (!$primaryKeyField || !$primaryKeyValue || !$data) {
            return response()->json([
                'status' => 'error',
                'message' => 'Primary key field, value, and data are required for update operation.'
            ], 400);
        }

        $updated = DB::table($table)->where($primaryKeyField, $primaryKeyValue)->update($data);

        return response()->json([
            'status' => $updated ? 'success' : 'error',
            'message' => $updated ? 'Data updated successfully.' : 'No record updated.'
        ]);
    }
}

/*-----------------------------------------------
| DELETE ACTION
-----------------------------------------------*/
class DeleteAction
{
    public function execute(Request $request)
    {
        $table = $request->input('table');
        $primaryKeyField = $request->input('primary_key_field');
        $primaryKeyValue = $request->input('primary_key_value');

        if (!$primaryKeyField || !$primaryKeyValue) {
            return response()->json([
                'status' => 'error',
                'message' => 'Primary key field and value are required for delete operation.'
            ], 400);
        }

        $deleted = DB::table($table)->where($primaryKeyField, $primaryKeyValue)->delete();

        return response()->json([
            'status' => $deleted ? 'success' : 'error',
            'message' => $deleted ? 'Record deleted successfully.' : 'No record found to delete.'
        ]);
    }
}

/*-----------------------------------------------
| GET ACTION (Supports filter + limit)
-----------------------------------------------*/
class GetAction
{
    public function execute(Request $request)
    {
        $table = $request->input('table');
        $primaryKeyField = $request->input('primary_key_field');
        $primaryKeyValue = $request->input('primary_key_value');
        $filters = $request->input('filters', []);
        $limit = $request->input('limit', 10);

        $query = DB::table($table);

        if ($primaryKeyField && $primaryKeyValue) {
            $query->where($primaryKeyField, $primaryKeyValue);
        }

        if (!empty($filters) && is_array($filters)) {
            foreach ($filters as $field => $value) {
                $query->where($field, $value);
            }
        }

        $data = $query->limit($limit)->get();

        return response()->json([
            'status' => 'success',
            'count' => $data->count(),
            'data' => $data
        ]);
    }
}
