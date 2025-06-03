# Database Scripts

This directory contains SQL scripts for database initialization and management.

## Scripts

### `create_tables.sql`
- Creates all necessary database tables
- Defines table relationships and constraints
- Sets up indexes for performance
- Initializes the database schema

### `managers.sql`
- Creates the managers table
- Inserts initial manager records
- Defines manager roles and permissions
- Required for report generation functionality

## Table Structure

### Clients Table
- `id`: Primary key
- `name`: Client name
- `city`: Client's city
- `email`: Client's email
- `created_at`: Timestamp of creation

### Invoices Table
- `id`: Primary key
- `client_id`: Foreign key to clients
- `amount`: Invoice amount
- `status`: Invoice status (pending/completed/canceled)
- `issued_at`: Issue date
- `due_date`: Due date
- `created_at`: Timestamp of creation

### Managers Table
- `id`: Primary key
- `name`: Manager name
- `email`: Manager email
- `role`: Manager role
- `created_at`: Timestamp of creation

### Reports Table
- `id`: Primary key
- `client_id`: Foreign key to clients (nullable)
- `client_name`: Client name (nullable)
- `period`: Report period
- `manager_email`: Recipient email
- `manager_name`: Recipient name
- `report_type`: Type of report
- `report_text`: Report content
- `created_at`: Timestamp of creation

## Usage

These scripts are automatically executed during:
- Initial database setup
- Docker container initialization
- Test database creation

## Best Practices

1. Keep schema changes in version control
2. Document all table relationships
3. Use appropriate data types and constraints
4. Include indexes for frequently queried columns
5. Maintain data integrity with foreign keys 