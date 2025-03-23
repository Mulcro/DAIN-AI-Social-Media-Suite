import { PythonShell } from 'python-shell';

function runPythonScript(scriptPath: string, args: string[]): Promise<{ code: number; signal: string | null; messages: string[] }> {
    return new Promise((resolve, reject) => {
      const pyshell = new PythonShell(scriptPath, { args, mode: 'text' });
  
      const messages: string[] = [];
  
      pyshell.on('message', (message) => {
        console.log('Python script output:', message);
        messages.push(message);
      });
  
      pyshell.end((err, code, signal) => {
        if (err) {
          reject(err);
        } else {
          resolve({ code: code ?? 0, signal, messages });
        }
      });
    });
  }


export const handleGetVideo = async (
    { url }: { url: any },
    agentInfo: any
  ): Promise<{
    text: string;
    data: any;
    ui: any;
    pleasePay?: any;
    processes?: string[] | { id: string; name: string; description: string; type: "one-time" | "recurring" }[];
  }> => {
    console.log("Python script starting");

    let highlightURls = undefined;

    //Get highlight urls and download clips
    try {
        const result = await runPythonScript("./utilities/generateHighlights.py", [url]);
        console.log(`Python script finished with code: ${result.code}, signal: ${result.signal}`);
        console.log("All messages:", result.messages);
        
        // Assume the final message is the JSON output of highlight URLs
        const lastMessage = result.messages[result.messages.length - 1];
        const output = JSON.parse(lastMessage);
        console.log("Highlight URLs:", output.highlight_urls);
        highlightURls = output.highlight_urls;
        // Now you can use output.highlight_urls in your TS code.
      } catch (err) {
        console.error("Error running Python script:", err);
      }
  
    //Pick the first video and post it to the social media sites
    
    //Youtube shorts
    try {
        console.log("Posting to YouTube Shorts");
        const result = await runPythonScript("./api/youtube/youtube.py", [
          "--file", "/Users/mulero/Documents/Programming/DAIN-AI-Social-Media-Suite/constants/highlights/highlight_1.mp4",
          "--title", "My Awesome Video #shorts",
          "--description", "This is a YouTube Shorts upload from my Python script.",
          "--category", "22",
          "--privacy", "public",
          "--client-secrets", "/Users/mulero/Documents/Programming/DAIN-AI-Social-Media-Suite/api/youtube/client_secrets.json"
        ]);
        console.log(`Python script finished with code: ${result.code}, signal: ${result.signal}`);
        console.log("All messages:", result.messages);
      } catch (err) {
        console.error("Error running Python script:", err);
      }

    // instagram reels
    try {
        const videoUrl = highlightURls[0];

        console.log("I'm in here, here are the highlight urls: ", videoUrl);
        const result = await runPythonScript("./api/instagram/instagram.py", [
          "--video_url", videoUrl,
          "--caption", "Dain did this",
          "--thumb_offset", "2000",
        ]);
        console.log(`Python script finished with code: ${result.code}, signal: ${result.signal}`);
        console.log("All messages:", result.messages);
      } catch (err) {
        console.error("Error running Python script:", err);
      }

    console.log(`Video url received!: ${url}`);
    // Additional logic after Python script completes can go here
  
    return {
      text: "Video URL received and processed successfully.",
      data: {
        success: true,
        message: `Sent ${url} successfully.`
      },
      ui: {}
    };
  };