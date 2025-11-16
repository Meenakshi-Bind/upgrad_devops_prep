const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const app = express();
const PORT = process.env.PORT || 3010;

app.use(cors());
app.use(bodyParser.json());
app.use(express.static(path.join(__dirname, 'public')));

const db = new sqlite3.Database('./parking.db', (err) => {
    if (err) {
        console.error('Error opening database:', err.message);
    } else {
        console.log('Connected to SQLite database.');
        initializeDatabase();
    }
});

function initializeDatabase() {
    db.run(`CREATE TABLE IF NOT EXISTS vehicles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        vehicle_number TEXT UNIQUE,
        vehicle_type TEXT,
        vehicle_model TEXT,
        customer_name TEXT,
        phone_number TEXT,
        checkin_time DATETIME DEFAULT CURRENT_TIMESTAMP,
        checkout_time DATETIME,
        duration_hours REAL,
        is_checked_out BOOLEAN DEFAULT FALSE
    )`);
}

app.get('/api/vehicles', (req, res) => {
    const sql = `SELECT * FROM vehicles WHERE is_checked_out = FALSE ORDER BY checkin_time DESC`;
    db.all(sql, [], (err, rows) => {
        if (err) {
            res.status(400).json({ error: err.message });
            return;
        }
        res.json({ data: rows });
    });
});

app.post('/api/vehicles/checkin', (req, res) => {
    const { vehicleNumber, vehicleType, vehicleModel, customerName, phoneNumber } = req.body;
    
    const sql = `INSERT INTO vehicles (vehicle_number, vehicle_type, vehicle_model, customer_name, phone_number) 
                 VALUES (?, ?, ?, ?, ?)`;
    
    db.run(sql, [vehicleNumber, vehicleType, vehicleModel, customerName, phoneNumber], function(err) {
        if (err) {
            if (err.message.includes('UNIQUE constraint failed')) {
                res.status(400).json({ error: 'Vehicle already parked' });
            } else {
                res.status(400).json({ error: err.message });
            }
            return;
        }
        res.json({ message: 'Vehicle checked in successfully', id: this.lastID });
    });
});

app.put('/api/vehicles/checkout/:id', (req, res) => {
    const vehicleId = req.params.id;
    const checkoutTime = new Date().toISOString();
    
    const sql = `UPDATE vehicles 
                 SET checkout_time = ?, 
                     is_checked_out = TRUE,
                     duration_hours = ROUND((julianday(?) - julianday(checkin_time)) * 24, 2)
                 WHERE id = ?`;
    
    db.run(sql, [checkoutTime, checkoutTime, vehicleId], function(err) {
        if (err) {
            res.status(400).json({ error: err.message });
            return;
        }
        res.json({ message: 'Vehicle checked out successfully' });
    });
});

app.get('/api/vehicles/search/:query', (req, res) => {
    const query = `%${req.params.query}%`;
    const sql = `SELECT * FROM vehicles WHERE vehicle_number LIKE ? AND is_checked_out = FALSE`;
    
    db.all(sql, [query], (err, rows) => {
        if (err) {
            res.status(400).json({ error: err.message });
            return;
        }
        res.json({ data: rows });
    });
});

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});