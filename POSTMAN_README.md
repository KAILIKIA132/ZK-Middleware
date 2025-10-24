# Postman Collection for ZK Middleware

This Postman collection contains all the API endpoints for testing the ZK Middleware for Canteen Management System.

## Prerequisites

1. [Postman](https://www.postman.com/downloads/) installed
2. The ZK Middleware running locally on port 5000
3. The mock school API running locally on port 8080

## How to Use

1. Start the ZK Middleware:
   ```bash
   cd /Users/aaron/CanteenManagementSystem/zk_middleware
   export SCHOOL_API_BASE_URL=http://localhost:8080/api
   export SCHOOL_API_KEY=test_api_key
   python app.py
   ```

2. Start the mock school API (in a separate terminal):
   ```bash
   cd /Users/aaron/CanteenManagementSystem/zk_middleware
   python mock_school_api.py
   ```

3. Import the Postman collection:
   - Open Postman
   - Click "Import" in the top left
   - Select the `ZK_Middleware_API.postman_collection.json` file
   - Click "Import"

## Collection Structure

The collection is organized into the following folders:

### Middleware Endpoints
- **Health Check**: Check if the middleware is running
- **Get Student Fees Status**: Check if a student has paid their fees
- **Log Attendance**: Log an attendance entry
- **Print Meal Ticket**: Print a meal ticket for a student
- **Test Print**: Test the printer connection
- **Test Error Print**: Test printing an error message
- **Admin Dashboard**: Access the admin interface

### Mock API Endpoints
- **Mock API Health Check**: Check if the mock API is running
- **Get Student Fees (Mock API)**: Direct access to student fee information
- **Get All Students (Mock API)**: Get a list of all students

## Sample Student IDs

The mock API includes the following sample students:

- `1001` - Wangari Maathai (Paid)
- `1002` - Jomo Kenyatta (Unpaid)
- `1003` - Chinua Achebe (Paid)
- `1004` - Grace Ogot (Paid)
- `1005` - Ngugi wa Thiong'o (Unpaid)

## Environment Variables

The collection uses localhost URLs by default:
- Middleware: `http://localhost:5000`
- Mock API: `http://localhost:8080`

You can modify these in Postman by creating an environment.

## Testing Scenarios

1. **Successful Payment Check**: Use student ID `1001` or `1003` to test successful payment verification
2. **Unpaid Student**: Use student ID `1002` or `1005` to test unpaid student handling
3. **Unknown Student**: Use any other student ID to test unknown student handling
4. **Printer Testing**: Use the test print endpoints to verify printer functionality

## Notes

- The ZK device connection will fail in local testing as it requires physical hardware
- The printer connection will fail in local testing unless you have a network printer configured
- All other functionality can be tested locally with the provided mock API