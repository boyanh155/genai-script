import { spawn } from "child_process";
import { connectDB } from "./connectDb.js";


async function main() {
    const db = await connectDB()
    const result = await db.collection('services').find({}).toArray()

    result.forEach(doc => {
        const python = spawn('python', ['./embedding.py', doc])

        python.stdout.on('data', (data) => {
            const embeddings = JSON.parse(data);
            console.log(`Embeddings: ${embeddings}`);
            // Here you can save the embeddings back to MongoDB or use them for further processing
        });
        python.stderr.on('data', (data) => {
            console.error(`stderr: ${data}`);
        });

        python.on('close', (code) => {
            console.log(`child process exited with code ${code}`);
        });
    });


}
main()