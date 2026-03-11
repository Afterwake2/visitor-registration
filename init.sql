CREATE TABLE IF NOT EXISTS visitors (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    contact_number VARCHAR(50) NOT NULL,
    company_name VARCHAR(150),
    purpose TEXT NOT NULL,
    contact_person VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);
