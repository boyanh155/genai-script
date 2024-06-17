const fs = require('fs');
const { RecursiveCharacterTextSplitter } = require('langchain/text_splitter')

try {
    console.log(process.cwd())
    const splitter = new RecursiveCharacterTextSplitter();
    fs.readFile('./service-rows.txt', 'utf8', async(err, data) => {
        if (data) {

            const out = await splitter.createDocuments([data])
            console.log(out)
        }
    })
} catch (err) {
    console.log(err);
}