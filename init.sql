CREATE TABLE IF NOT EXISTS visitors (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    contact_number VARCHAR(50),
    company_name VARCHAR(150),
    purpose_of_visit TEXT,
    contact_person VARCHAR(150),
    visit_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);