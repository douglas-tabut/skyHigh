const {CohereClient} = require('cohere-ai');

// userSnippetStart variable contains what the person has started typing , then it is fed into the model to be autocompleted

let userSnippetStart = 'def reverse_string()'; 


const PROMPT = `You are a helpful code assistant that helps in writing useful code snippets in python. Your language of choice is Python. Don't explain the code, just generate the code block itself
${userSnippetStart}
`

const cohere = new CohereClient({
    token: "K3P7ftTGY9vkkGreskxCXBYXgGAqIFtk4OihSFcE",
});

(async () => {
    const prediction = await cohere.generate({
        prompt: PROMPT,
        maxTokens: 300,
    });
    
    console.log(prediction.generations[0].text); 
})();


