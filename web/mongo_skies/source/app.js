const express = require('express');
const bodyParser = require('body-parser');
const { MongoClient } = require('mongodb');
const app = express();
const port = 3000;

app.use(express.static(__dirname + '/public'));

app.use(bodyParser.urlencoded({ extended: true }));
app.set('view engine', 'ejs');

const uri = 'mongodb://localhost:27017';
const client = new MongoClient(uri);


const path = require('path');

app.get('/package.json', (req, res) => {
    const filePath = path.join(__dirname, 'package.json');
    res.download(filePath, 'package.json', (err) => {
        if (err) {
            console.error('Download error:', err);
            res.status(500).send('Failed to download package.json');
        }
    });
});

app.get('/', (req, res) => {
    res.render('index');
});

app.post('/login', async (req, res) => {
    const { user, pass } = req.body;

    try {
        await client.connect();
        const db = client.db('rja');
        const users = db.collection('users');

        const found = await users.findOne({ user: user, pass: pass });

        if (found) {
            res.send(`Welcome, Captain ${found.user}!<br>Flag: ${process.env.FLAG}`);
        } else {
            res.status(401).render('access-denied');
        }

    } catch (err) {
        console.error(err);
        res.send("Internal server error.");
    }
});

app.listen(port, () => {
    console.log(`App flying at http://localhost:${port}`);
});
