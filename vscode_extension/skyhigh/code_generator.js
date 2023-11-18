const { CohereClient } = require('cohere-ai');
const fs = require('fs');


// userSnippetStart variable contains what the person has started typing , then it is fed into the model to be autocompleted
// Read the JSON file
const jsonFilePath = '../../data-scrapper/unique_snippets.json'; // path with all tokens

const jsonData = JSON.parse(fs.readFileSync(jsonFilePath, 'utf-8'));

// Retrieve the uniqueWords array from the JSON data
const uniqueWordsArray = jsonData.uniqueWords


// Add the unique subtokens to the wordsList array
const wordsList = uniqueWordsArray

const allSnippets = {}; // Array to store all generated snippets

// Iterate through the list of words
// I am reducing the size because cohere breaks the connection because of too many requests.
// TODO COHERE is not able to check all our word lists... for now I am iterating ..
// through only ten words each time e.g for (let i = 10; i < 10; i++) { to avoid errors

for (let i = 0; i < wordsList.length; i++) {

    let userSnippetStart = wordsList[i];

    const PROMPT = `You are a helpful code assistant that helps in writing useful code snippets in python. Your language of choice is Python. Don't explain the code, just generate the code block itself
${userSnippetStart}
`

    const cohere = new CohereClient({
        token: "K3P7ftTGY9vkkGreskxCXBYXgGAqIFtk4OihSFcE",
    });


    async function code_generator() {
        const prediction = await cohere.generate({
            prompt: PROMPT,
            maxTokens: 300,
        });

        let outputdd = prediction.generations[0].text.toString();
        let output = normalizePythonCode(outputdd);


        // Remove comments from the Python code
        output = output.replace(/#[^\n\r]*[\n\r]/g, ''); // Removes single-line comments
        output = output.replace(/""".*?"""/gs, ''); // Removes multi-line comments

        let jsonSnippet = {
            "prefix": userSnippetStart,
            "body": [output],
            "description": "Python"
        };

        allSnippets[`skyHigh:${userSnippetStart}`] = jsonSnippet;

        console.log(JSON.stringify(jsonSnippet, null, 2));
        const allSnippetsFileName = './snippets/snippets.json';
        // fs.writeFileSync(allSnippetsFileName, JSON.stringify(allSnippets, null, 2));
        // console.log(`All snippets saved to: ${allSnippetsFileName}`);

        // Read existing data from the file
let existingData = {};
try {
    const existingContent = fs.readFileSync(allSnippetsFileName, 'utf-8');
    existingData = JSON.parse(existingContent);
} catch (error) {
    // Handle the case where the file does not exist or is not valid JSON
}

// Merge the new snippets into the existing data object
const updatedData = { ...existingData, ...allSnippets };

// Write the updated data back to the file
fs.writeFileSync(allSnippetsFileName, JSON.stringify(updatedData, null, 2));



        return jsonSnippet;
    };
    code_generator()

    function normalizePythonCode(output) {
        output = output.toString();

        output = output.toString();
        const codeMatch = /```python([\s\S]*?)```/g.exec(output);
        const codeSnippet = codeMatch ? codeMatch[1].trim() : '';

        return codeSnippet;
    }

    function generateUniquewords() {
        const tokenpath = '../../data-scrapper/tokenized_code_snippets.json'; // Replace with your actual file path
        const tokenjson = JSON.parse(fs.readFileSync(tokenpath, 'utf-8'));

        // Extract unique words from the 'subtokens' key
        const uniqueWords = Array.from(new Set(tokenjson.flatMap(item => item.subtokens)));

        // Create a new JSON object with unique words
        const uniqueWordsObject = { uniqueWords };

        // Save the new JSON object to a new file
        const outputFilePath = '../../data-scrapper/unique_snippets.json'; // Replace with your desired output file path
        fs.writeFileSync(outputFilePath, JSON.stringify(uniqueWordsObject, null, 2));

        console.log(`Unique words saved to: ${outputFilePath}`);
    }
    // Uncomment this to generate the unique snippets json file
    // generateUniquewords()
}