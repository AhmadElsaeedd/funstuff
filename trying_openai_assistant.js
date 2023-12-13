const OpenAI = require("openai");
const fs = require("fs");
require('dotenv').config();

const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY });

async function retrieve_run(thread_id, run_id){
    const run = await openai.beta.threads.runs.retrieve(
        thread_id,
        run_id
      );
    
    console.log("Run status is: ", run.status);

    //if run's status is "completed" return true
    if(run.status === "completed") return true;
    else return false;
}

function periodicallyCheckRun(thread_id, run_id) {
    return new Promise((resolve, reject) => {
      const interval = setInterval(async () => {
        try {
          console.log("Checking run status...");
          const isCompleted = await retrieve_run(thread_id, run_id);
  
          if (isCompleted) {
            console.log("Run completed!");
            clearInterval(interval);
            resolve();
          }
        } catch (error) {
          console.error("Error checking run status:", error);
          clearInterval(interval);
          reject(error);
        }
      }, 1000); // Check every 1000 milliseconds (1 second)
    });
  }
  

async function main() {
  try {
    // // Upload a file with an "assistants" purpose
    // const knowledge_file = await openai.files.create({
    //   file: fs.createReadStream("knowledge.pdf"),
    //   purpose: "assistants",
    // });

    // // Add the file to the assistant
    // const assistant = await openai.beta.assistants.create({
    //   instructions: "You generate images of people to be used in an anonymous social app. You will take an image of them as a file and refer to the files in your knowledge and this instruction to create a pixelated avatar to use for a profile (only face with shoulders, white background).",
    //   model: "gpt-3.5-turbo-1106",
    //   tools: [{"type": "retrieval"}],
    //   file_ids: [knowledge_file.id],
    //   name:"Image generator"
    // });

    // console.log("Assistant created:", assistant);

    const myAssistant = await openai.beta.assistants.retrieve(
        "asst_vea0ryNEyBs7fC5zU7Yayxac"
      );

    console.log("Assistant retrieved:", myAssistant);

    //Uncomment when u want to create a new thread
    const thread = await openai.beta.threads.create();

    const myThread = await openai.beta.threads.retrieve(
        thread.id
      );
    
    console.log("Thread retrieved: ", myThread);

    const message_file = await openai.files.create({
        file: fs.createReadStream("image.pdf"),
        purpose: "assistants",
      });

    console.log("message file: ", message_file);

    const message = await openai.beta.threads.messages.create(
        myThread.id,
        {
          role: "user",
          content: "Can you generate a pixelated avatar to use for a profile (only face with shoulders, white background) using the picture that I give you in the file? Put the image in a pdf so I can extract it later.",
          file_ids: [message_file.id],
        }
      );

    const threadMessages = await openai.beta.threads.messages.list(
        myThread.id
      );
    
    console.log("Messages in the thread before run: ", threadMessages.data);

    //Create run
    const run = await openai.beta.threads.runs.create(
        myThread.id,
        { assistant_id: myAssistant.id }
      );
    console.log("run created");
    
    //periodically run retrieve_run until it returns true
    await periodicallyCheckRun(myThread.id, run.id);

    const messages = await openai.beta.threads.messages.list(
        myThread.id
      );
    console.log("Messages in the thread after run: ", messages.data);


    // const messages = await openai.beta.threads.messages.list(
    //     // myThread.id
    //     "thread_1BmwhHX1QaYP8ZUDv9FiJ3dI"
    //   );
    // console.log("Messages in the run are: ", messages.data[0].id);


    const messageFiles = await openai.beta.threads.messages.files.list(
        myThread.id,
        messages.data[0].id
      );
    console.log("Message files are: ", messageFiles);
    
  } catch (error) {
    console.error("Error:", error);
  }
}

main();

