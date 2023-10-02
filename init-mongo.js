// Connect to the admin database as an admin user
var adminDb = db.getSiblingDB("admin");
adminDb.auth("adminUsername", "adminPassword");

// Create a new database and user for your application
var newDb = db.getSiblingDB("mydb");
newDb.createUser({
  user: "myuser",
  pwd: "mypassword",
  roles: [
    { role: "readWrite", db: "mydb" },
    { role: "dbAdmin", db: "mydb" },
  ],
});

// Switch to your application's database
db = newDb;

// Create collections and perform other setup as needed
db.createCollection("mycollection");

// Insert sample data
db.mycollection.insert([
  { name: "John", age: 30 },
  { name: "Jane", age: 25 },
]);
