const {CohereClient} = require('cohere-ai');

// userSnippetStart variable contains what the person has started typing , then it is fed into the model to be autocompleted

let userSnippetStart = 'import'; 


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
    
    let output = prediction.generations[0];
    // const new_json = JSON.parse('"{'+output+'}')
    console.log(output)
    return output;
};
code_generator()