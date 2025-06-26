const { MongoClient } = require('mongodb');

const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri);

(async () => {
    await client.connect();
    const db = client.db('rja');
    const users = db.collection('users');
    await users.deleteMany({});
    await users.insertOne({ user: 'admin', pass: 'royalsecret' });
    await client.close();
})();
