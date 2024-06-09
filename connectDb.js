import { MongoClient } from "mongodb";

const connection_string = `mongodb+srv://loclh:1@cluster0.rxcryft.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0`
export const connectDB = async() => {
    try {
       const conn = await MongoClient.connect(connection_string);

       console.log(`MongoDB Connected`);
        return conn.db('test_vector');

    } catch (error) {
        console.error(`Error: ${error.message}`);
        process.exit(1);
    }
}