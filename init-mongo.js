const user =  process.env.MONGO_INITDB_ROOT_USERNAME;
const password = process.env.MONGO_INITDB_ROOT_PASSWORD;
const database = process.env.MONGO_INITDB_DATABASE;

db = db.getSiblingDB(database);

const databases = db.adminCommand({ listDatabases: 1 }).databases;
const dbExists = databases.some((db) => db.name === database);

if (!dbExists) {
    const newDb = db.getSiblingDB(database);

    newDb.createUser({
        user: user,
        pwd: password,
        roles: [{ role: "readWrite", db: database }],
    });


    newDb.books.insertMany([
        {
            title: 'The Great Gatsby',
            author: 'F. Scott Fitzgerald',
            published_date: new Date('1925-04-10'),
            genre: 'Fiction',
            description: 'Description of The Great Gatsby',
            price: 10.99
        },
        {
            title: 'An American Tragedy',
            author: 'Theodore Dreiser',
            published_date: new Date('1925-12-17'),
            genre: 'Drama',
            description: 'Description of An American Tragedy',
            price: 12.99
        },
        {
            title: 'Arrowsmith',
            author: 'Sinclair Lewis',
            published_date: new Date('1925-01-01'),
            genre: 'Fiction',
            description: 'Description of Arrowsmith',
            price: 11.99
        },
        {
            title: 'To Kill a Mockingbird',
            author: 'Harper Lee',
            published_date: new Date('1960-07-11'),
            genre: 'Fiction',
            description: 'Description of To Kill a Mockingbird',
            price: 8.99
        },
        {
            title: 'Green Eggs and Ham',
            author: 'Dr. Seuss',
            published_date: new Date('1960-08-12'),
            genre: 'Children',
            description: 'Description of Green Eggs and Ham',
            price: 6.99
        },
        {
            title: '1984',
            author: 'George Orwell',
            published_date: new Date('1949-06-08'),
            genre: 'Dystopian',
            description: 'Description of 1984',
            price: 9.99
        },
        {
            title: 'Pride and Prejudice',
            author: 'Jane Austen',
            published_date: new Date('1813-01-28'),
            genre: 'Romance',
            description: 'Description of Pride and Prejudice',
            price: 7.99
        },
        {
            title: 'Moby-Dick',
            author: 'Herman Melville',
            published_date: new Date('1851-10-18'),
            genre: 'Adventure',
            description: 'Description of Moby-Dick',
            price: 11.49
        },
        {
            title: 'War and Peace',
            author: 'Leo Tolstoy',
            published_date: new Date('1869-01-01'),
            genre: 'Historical',
            description: 'Description of War and Peace',
            price: 13.99
        },
        {
            title: 'The Catcher in the Rye',
            author: 'J.D. Salinger',
            published_date: new Date('1951-07-16'),
            genre: 'Fiction',
            description: 'Description of The Catcher in the Rye',
            price: 10.49
        }
    ]);
}