CREATE TABLE servers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    hostname VARCHAR(255),
    ip VARCHAR(50),
    os VARCHAR(100),
    agent_version VARCHAR(50),
    last_seen TIMESTAMP
);

CREATE TABLE scans (
    id INT AUTO_INCREMENT PRIMARY KEY,
    server_id INT,
    scan_time TIMESTAMP,
    status VARCHAR(50),
    FOREIGN KEY (server_id) REFERENCES servers(id)
);

CREATE TABLE crypto_components (
    id INT AUTO_INCREMENT PRIMARY KEY,
    scan_id INT,
    library_name VARCHAR(255),
    version VARCHAR(50),
    file_path TEXT,
    risk_level VARCHAR(50),
    FOREIGN KEY (scan_id) REFERENCES scans(id)
);
