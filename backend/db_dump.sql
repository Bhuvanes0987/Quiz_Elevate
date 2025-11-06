
-- Minimal SQL schema for reference. If you already created the 'quizelevate' database, run Flask migrations.
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  username VARCHAR(150),
  password_hash VARCHAR(255),
  class_grade SMALLINT,
  is_admin BOOLEAN DEFAULT FALSE,
  created_at DATETIME
);
CREATE TABLE IF NOT EXISTS otp_codes (
  id INT AUTO_INCREMENT PRIMARY KEY,
  phone_or_email VARCHAR(255),
  code VARCHAR(16),
  expires_at DATETIME,
  used BOOLEAN DEFAULT FALSE,
  created_at DATETIME
);
