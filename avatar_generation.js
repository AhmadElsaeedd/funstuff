const OpenAI = require("openai");
const fs = require("fs");
require('dotenv').config();


const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function main() {
    const imageStream = fs.createReadStream('./ahmad_rgba.png');
    

    const response = await openai.images.createVariation({
        image: imageStream,
        n: 1,
        // prompt: "Create a variation of this person as a cartoon character."
    });

    console.log(response.data)

    // Check the format of the response and save the edited image accordingly
    // Assuming the response contains binary data for the image
    // const editedImagePath = './avatar.jpg';
    // fs.writeFileSync(editedImagePath, response.data); // Assuming 'response.data' is the image data

    // console.log('Edited image saved to:', editedImagePath);
}
main();
