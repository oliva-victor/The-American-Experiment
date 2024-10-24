const express = require('express');
const { Sequelize, DataTypes } = require('sequelize');
const bcrypt = require('bcrypt');
const cors = require('cors');

const app = express();
const port = 3000;

// Middleware to parse JSON
app.use(express.json());
app.use(cors({
    origin: 'http://localhost:8501',  // Adjust according to where your Streamlit app is hosted
    methods: ['POST'],
    allowedHeaders: ['Content-Type'],
}));

// Database setup
const sequelize = new Sequelize('american', 'root', 'password1!', {
    host: 'localhost',
    dialect: 'mysql'
});

// Define the Message model
const Message = sequelize.define('Message', {
    username: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    room: {
        type: DataTypes.STRING,
        allowNull: false,
    },
    text: {
        type: DataTypes.TEXT,
        allowNull: false,
    },
}, {
    timestamps: false,
});

// Define the User model
const User = sequelize.define('User', {
    username: {
        type: DataTypes.STRING,
        allowNull: false,
        unique: true
    },
    password: {
        type: DataTypes.STRING,
        allowNull: false
    },
    createdAt: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
    },
    updatedAt: {
        type: DataTypes.DATE,
        defaultValue: DataTypes.NOW
    },
    day: {
        type: DataTypes.INTEGER,
        defaultValue: 0
    },
    user2: {
        type: DataTypes.STRING(50), // Change this to STRING(50) if it's for usernames
        allowNull: true
    },
    room: {
        type: DataTypes.INTEGER,
        defaultValue: -1
    }
});

// Define the Presurvey model without an ID column
const Presurvey = sequelize.define('presurvey', {
    username: {
        type: DataTypes.STRING(50),
        allowNull: false,
    },
    philosophy: {
        type: DataTypes.ENUM('LL', 'L', 'M', 'R', 'RR'),
        allowNull: true,
    },
    differences: {
        type: DataTypes.INTEGER,
        defaultValue: -1
    },
    question1: {
        type: DataTypes.STRING(50),
        allowNull: true,
    },
    question2: {
        type: DataTypes.STRING(50),
        allowNull: true,
    },
    question3: {
        type: DataTypes.STRING(50),
        allowNull: true,
    },
    question4: {
        type: DataTypes.STRING(50),
        allowNull: true,
    },
    question5: {
        type: DataTypes.STRING(50),
        allowNull: true,
    },
    question6: {
        type: DataTypes.STRING(50),
        allowNull: true,
    },
    question7: {
        type: DataTypes.STRING(50),
        allowNull: true,
    },
    question8: {
        type: DataTypes.STRING(50),
        allowNull: true,
    },
    question9: {
        type: DataTypes.STRING(50),
        allowNull: true,
    },
    question10: {
        type: DataTypes.STRING(50),
        allowNull: true,
    },
}, {
    timestamps: false,
    freezeTableName: true,
    indexes: []
});

const Postsurvey = sequelize.define('postsurvey', {
    username: {
        type: DataTypes.STRING(50),
        allowNull: false,
    },
    differences: {
        type: DataTypes.INTEGER,
        defaultValue: -1,
    },
    tolerance: {
        type: DataTypes.INTEGER,
        defaultValue: -1,
    },
}, {
    timestamps: false,
    freezeTableName: true,
    indexes: []
})

// Sync the database without dropping existing tables
sequelize.sync({ force: false })
    .then(() => {
        console.log('Database synced');
    })
    .catch(err => {
        console.error('Error syncing database:', err);
    });

// Handle incoming messages via POST
app.post('/messages', async (req, res) => {
    const { username, room, text } = req.body;

    try {
        const message = await Message.create({ username, room, text });
        res.status(201).json(message);
    } catch (error) {
        console.error("Failed to save message:", error);
        res.status(500).json({ error: "Failed to save message" });
    }
});

// Get chat history
app.get('/messages', async (req, res) => {
    const { room } = req.query;

    try {
        const messages = await Message.findAll({
            where: { room },
            order: [['createdAt', 'ASC']]
        });
        res.json(messages);
    } catch (error) {
        console.error("Failed to fetch messages:", error);
        res.status(500).json({ error: "Failed to fetch messages" });
    }
});

// Check if a user exists and get their room number and user2
app.get('/users/exists', async (req, res) => {
    const { username } = req.query;
    if (!username) {
        return res.status(400).json({ error: 'Username is required.' });
    }

    const user = await User.findOne({ where: { username } });
    if (user) {
        return res.json({ 
            exists: true, 
            day: user.day,
            room: user.room, 
            user2: user.user2 // Include user2 in the response
        });
    } else {
        return res.json({ exists: false });
    }
});

// Create a new user
app.post('/signup', async (req, res) => {
    const { username, password } = req.body;
    try {
        const hashedPassword = await bcrypt.hash(password, 10);
        const user = await User.create({ username, password: hashedPassword });
        
        res.status(201).json({ message: 'User created!', user });
    } catch (error) {
        console.error("Failed to create user:", error);
        res.status(500).json({ error: error.message });
    }
});


// Check if the password matches for a given username
app.post('/check-password', async (req, res) => {
    const { username, password } = req.body;
    if (!username || !password) {
        return res.status(400).json({ error: 'Username and password are required.' });
    }

    try {
        const user = await User.findOne({ where: { username } });
        if (!user) {
            return res.status(404).json({ valid: false });
        }

        console.log("Retrieved user:", user);
        console.log("Provided password:", password);
        console.log("Stored hash:", user.password);

        const isValid = await bcrypt.compare(password, user.password);
        console.log("Password match:", isValid);

        return res.json({ valid: isValid });
    } catch (error) {
        console.error("Error checking password:", error);
        res.status(500).json({ error: "Failed to check password" });
    }
});

app.post('/presurvey', async (req, res) => {
    const { username, philosophy, differences, question1, question2, question3, question4, question5, question6, question7, question8, question9, question10 } = req.body;

    try {
        const presurvey = await Presurvey.create({
            username: username,
            philosophy: philosophy,
            differences: differences,
            question1: question1,
            question2: question2,
            question3: question3,
            question4: question4,
            question5: question5,
            question6: question6,
            question7: question7,
            question8: question8,
            question9: question9,
            question10: question10,

        });

        // Define opposing philosophies
        let opposing_philosophies;
        if (philosophy === "RR" || philosophy === "R") {
            opposing_philosophies = ["LL", "L"];
        } else if (philosophy === "LL" || philosophy === "L") {
            opposing_philosophies = ["RR", "R"];
        } else {
            opposing_philosophies = ["RR", "LL"];
        }

        // Step 1: Find users with opposing philosophies
        const opposingUsers = await Presurvey.findAll({
            where: {
                philosophy: opposing_philosophies,
            },
            attributes: ['username'],
        });

        const opposing_usernames = opposingUsers.map(user => user.username);

        // Step 2: Find a user with NULL user2
        let username2 = null;
        if (opposing_usernames.length > 0) {
            for (const user of opposing_usernames) {
                const foundUser = await User.findOne({
                    where: { username: user, user2: null }
                });
                if (foundUser) {
                    username2 = foundUser.username;
                    break; // Stop after finding the first user with NULL user2
                }
            }
        }

        // Step 3: Prepare response and update user2 fields with room assignment
        if (username2) {
            const currentUser = await User.findOne({ where: { username } });

            // Step 4: Generate a unique room number
            const existingRooms = await User.findAll({
                where: {
                    room: {
                        [Sequelize.Op.ne]: -1 // Exclude unassigned rooms
                    }
                },
                attributes: ['room']
            });
            const existingRoomNumbers = existingRooms.map(user => user.room);
            let roomNumber = 0;

            // Find a unique room number
            while (existingRoomNumbers.includes(roomNumber)) {
                roomNumber++;
            }

            // Update the current user's user2 field, room, and createdAt date
            await User.update(
                { user2: username2, room: roomNumber, createdAt: new Date() },
                { where: { username: username } }
            );

            // Update the user2's user2 field, room, and createdAt date
            await User.update(
                { user2: username, room: roomNumber, createdAt: new Date() },
                { where: { username: username2 } }
            );

            res.status(201).json({
                message: 'Survey submitted successfully!',
                presurvey,
                user2: `user2 has been found! ${username2}`,
                room: roomNumber // Include room number in the response
            });
        } else {
            res.status(201).json({
                message: 'Survey submitted successfully!',
                presurvey,
                user2: 'sorry, no user2'
            });
        }
    } catch (error) {
        console.error("Failed to save survey:", error);
        res.status(500).json({ error: "Failed to save survey" });
    }
});

app.get('/presurveyanswers', async(req, res) => {
    const { username } = req.query;

    try {
        const user2 = await User.findOne({
            where: { username: username },
            attributes: ['user2'],
        });

        const answers = await Presurvey.findAll({
            where: { username: user2.user2 },
            attributes: ['question1', 'question2', 'question3', 'question4', 'question5', 'question6', 'question7', 'question8', 'question9', 'question10'],
        })

        res.status(200).json({ 
            question1: answers[0]?.question1,
            question2: answers[0]?.question2,
            question3: answers[0]?.question3,
            question4: answers[0]?.question4,
            question5: answers[0]?.question5,
            question6: answers[0]?.question6,
            question7: answers[0]?.question7,
            question8: answers[0]?.question8,
            question9: answers[0]?.question9,
            question10: answers[0]?.question10,
        })

    } catch (error) {
        res.status(500).json({error: 'Error!'});
    }
});

// Handle waiting room logic via GET
app.get('/waitingroom', async (req, res) => {
    const { username, philosophy } = req.query;

    if (!username || !philosophy) {
        return res.status(400).json({ error: 'Username and philosophy are required.' });
    }

    try {
        // Define opposing philosophies
        let opposing_philosophies;
        if (philosophy === "RR" || philosophy === "R") {
            opposing_philosophies = ["LL", "L"];
        } else if (philosophy === "LL" || philosophy === "L") {
            opposing_philosophies = ["RR", "R"];
        } else {
            opposing_philosophies = ["RR", "LL"];
        }

        // Step 1: Find users with opposing philosophies
        const opposingUsers = await Presurvey.findAll({
            where: {
                philosophy: opposing_philosophies,
            },
            attributes: ['username'],
        });

        const opposing_usernames = opposingUsers.map(user => user.username);

        // Step 2: Find a user with NULL user2
        let username2 = null;
        if (opposing_usernames.length > 0) {
            for (const user of opposing_usernames) {
                const foundUser = await User.findOne({
                    where: { username: user, user2: null }
                });
                if (foundUser) {
                    username2 = foundUser.username;
                    break; // Stop after finding the first user with NULL user2
                }
            }
        }

        // Step 3: Prepare response and update user2 fields with room assignment
        if (username2) {
            const currentUser = await User.findOne({ where: { username } });

            // Step 4: Generate a unique room number
            const existingRooms = await User.findAll({
                where: {
                    room: {
                        [Sequelize.Op.ne]: -1 // Exclude unassigned rooms
                    }
                },
                attributes: ['room']
            });
            const existingRoomNumbers = existingRooms.map(user => user.room);
            let roomNumber = 0;

            // Find a unique room number
            while (existingRoomNumbers.includes(roomNumber)) {
                roomNumber++;
            }

            // Update the current user's user2 field and room
            await User.update(
                { user2: username2, room: roomNumber, createdAt: new Date() },
                { where: { username: username } }
            );

            // Update the user2's user2 field and room
            await User.update(
                { user2: username, room: roomNumber, createdAt: new Date() },
                { where: { username: username2 } }
            );

            res.status(200).json({
                message: 'Match found!',
                user2: username2,
                room: roomNumber
            });
        } else {
            res.status(200).json({
                message: 'No match found yet. Please wait.'
            });
        }
    } catch (error) {
        console.error("Error in /waitingroom:", error);
        res.status(500).json({ error: 'Failed to check for a match.' });
    }
});

app.get('/postsurvey', async(req, res) => {
    const { username } = req.query;

    try {
        const postsurvey = await Postsurvey.findAll({
            where: { username: username }
        });

        if (postsurvey.length > 0) {
            res.status(200).json({
                message: 'User has already filled out this survey.'
            });
        } else {
            res.status(201).jjjson({
                message: 'User has not filled this form out yet.'
            })
        }    
    } catch (error) {
        res.status(500).json({error: 'Error!'});
    }
});

app.post('/postsurvey', async(req, res) => {
    const { username, differences, tolerance } = req.body

    try {
        await Postsurvey.create({
            username: username,
            differences: differences,
            tolerance: tolerance,
        });

        res.status(200).json({
            message: 'Survey submitted!'
        });
    } catch (error) {
        res.status(500).json({error: 'Can\'t submit'});
    }
});

// Start the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
