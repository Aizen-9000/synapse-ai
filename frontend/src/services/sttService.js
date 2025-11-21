export async function startListening() {
  return new Promise((resolve, reject) => {
    if (!("webkitSpeechRecognition" in window)) {
      alert("Speech recognition not supported in this browser.");
      return reject("Speech recognition not supported");
    }

    const recognition = new window.webkitSpeechRecognition();
    recognition.lang = "en-IN"; // You can change this
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    recognition.onresult = (event) => {
      const text = event.results[0][0].transcript;
      resolve(text);
    };

    recognition.onerror = (event) => reject(event.error);
    recognition.onend = () => console.log("Speech recognition ended");

    recognition.start();
  });
}