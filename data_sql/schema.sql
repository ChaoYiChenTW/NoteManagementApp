-- Drop existing tables (if any) for a clean setup
DROP TABLE IF EXISTS user_roles CASCADE;
DROP TABLE IF EXISTS role_permissions CASCADE;
DROP TABLE IF EXISTS permissions CASCADE;
DROP TABLE IF EXISTS roles CASCADE;
DROP TABLE IF EXISTS users CASCADE;

-- Create Users table
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Roles table
CREATE TABLE roles (
    role_id SERIAL PRIMARY KEY,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Permissions table
CREATE TABLE permissions (
    permission_id SERIAL PRIMARY KEY,
    permission_name VARCHAR(100) UNIQUE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create User_Roles table (join table)
CREATE TABLE user_roles (
    user_id INT NOT NULL,
    role_id INT NOT NULL,
    PRIMARY KEY (user_id, role_id),
    FOREIGN KEY (user_id) REFERENCES users (user_id) ON DELETE CASCADE,
    FOREIGN KEY (role_id) REFERENCES roles (role_id) ON DELETE CASCADE
);

-- Create Role_Permissions table (join table)
CREATE TABLE role_permissions (
    role_id INT NOT NULL,
    permission_id INT NOT NULL,
    PRIMARY KEY (role_id, permission_id),
    FOREIGN KEY (role_id) REFERENCES roles (role_id) ON DELETE CASCADE,
    FOREIGN KEY (permission_id) REFERENCES permissions (permission_id) ON DELETE CASCADE
);

-- Insert default roles
INSERT INTO roles (role_name) VALUES
('Admin'),
('Moderator'),
('Regular User'),
('Guest/Viewer');

-- Insert default permissions
INSERT INTO permissions (permission_name) VALUES
('manage_users'),
('assign_roles'),
('create_note'),
('edit_own_note'),
('edit_any_note'),
('delete_own_note'),
('delete_any_note'),
('view_note'),
('create_resource'),
('edit_own_resource'),
('edit_any_resource'),
('delete_own_resource'),
('delete_any_resource'),
('view_resource'),
('manage_settings');

-- Assign permissions to Admin
INSERT INTO role_permissions (role_id, permission_id)
SELECT roles.role_id, permissions.permission_id
FROM roles, permissions
WHERE roles.role_name = 'Admin';

-- Assign permissions to Moderator
INSERT INTO role_permissions (role_id, permission_id)
SELECT roles.role_id, permissions.permission_id
FROM roles
JOIN permissions ON
    permissions.permission_name IN (
        'create_note', 'edit_own_note', 'edit_any_note',
        'delete_own_note', 'delete_any_note', 'view_note',
        'create_resource', 'edit_own_resource', 'edit_any_resource',
        'delete_own_resource', 'delete_any_resource', 'view_resource'
    )
WHERE roles.role_name = 'Moderator';

-- Assign permissions to Regular User
INSERT INTO role_permissions (role_id, permission_id)
SELECT roles.role_id, permissions.permission_id
FROM roles
JOIN permissions ON
    permissions.permission_name IN (
        'create_note', 'edit_own_note', 'delete_own_note', 'view_note',
        'create_resource', 'edit_own_resource', 'delete_own_resource', 'view_resource'
    )
WHERE roles.role_name = 'Regular User';

-- Assign permissions to Guest/Viewer
INSERT INTO role_permissions (role_id, permission_id)
SELECT roles.role_id, permissions.permission_id
FROM roles
JOIN permissions ON
    permissions.permission_name IN ('view_note', 'view_resource')
WHERE roles.role_name = 'Guest/Viewer';
