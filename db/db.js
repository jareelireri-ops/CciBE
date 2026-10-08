const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.join(__dirname, 'cci.db');
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error connecting to the database:', err.message);
  } else {
    console.log('Connected to the SQLite database at cci.db');
  }
});

// For testing purposes, since members_data.json exists, we can seed the database if it's empty or we can just use the DB directly.
// We'll create the members table if it doesn't exist
db.serialize(() => {
  db.run(`CREATE TABLE IF NOT EXISTS members (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    phone_no TEXT NOT NULL,
    groups TEXT NOT NULL,
    share BOOLEAN DEFAULT 1
  )`);
});

module.exports = db;
