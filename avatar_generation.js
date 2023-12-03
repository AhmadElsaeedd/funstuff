const OpenAI = require("openai");
const fs = require("fs");
require('dotenv').config();

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function main() {
    const imageStream = fs.createReadStream('./Mawadda_RGBA.png');
    

    const response = await openai.images.generate({
        // image: imageStream,
        // n: 1,
        model: "dall-e-3",
        prompt: "Generate a pixel art of a 20 years old aged Middle Easter girl with brunette hair and hazel eyes. She is facing forwars and her gaze is direct. She is smiling. The background is transparent. There is enough detail to distinguish her hair and eye color. The pixel art is good resolution to vaguely show her features, but not give away who she is."
    });

    console.log(response.data)

    // Check the format of the response and save the edited image accordingly
    // Assuming the response contains binary data for the image
    // const editedImagePath = './avatar.jpg';
    // fs.writeFileSync(editedImagePath, response.data); // Assuming 'response.data' is the image data

    // console.log('Edited image saved to:', editedImagePath);
}
main();
