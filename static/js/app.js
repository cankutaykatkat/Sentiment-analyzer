const form = document.getElementById("sentiment-form");
const resultDiv = document.getElementById("result");
const textInput = document.getElementById("text-input");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  await analyzeSentiment();
});

textInput.addEventListener("keydown", async (e) => {
  if (e.key === "Enter") {
    e.preventDefault(); // Prevent form submission
    await analyzeSentiment();
  }
});

async function analyzeSentiment() {
  const text = textInput.value;

  // Clear previous result
  resultDiv.innerHTML = "Analyzing...";

  // Check if the input is empty
  if (!text.trim()) {
    resultDiv.innerHTML = "Please enter some text!";
    return;
  }

  try {
    // Send text to the backend for sentiment analysis
    const response = await fetch("/predict", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text }),
    });

    const data = await response.json();
    const sentiment = data.sentiment;

    // Save feedback in the database
    await fetch("/feedback", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ text, sentiment }),
    });

    // Display sentiment result
    let gifUrl;
    if (sentiment === "Positive") gifUrl = "/static/gifs/positive.gif";
    else if (sentiment === "Negative") gifUrl = "/static/gifs/negative.gif";
    else if (sentiment === "Question") gifUrl = "/static/gifs/question.gif";
    else gifUrl = "/static/gifs/neutral.gif";

    resultDiv.innerHTML = `
            <p>Sentiment: ${sentiment}</p>
            <img src="${gifUrl}" alt="${sentiment}" style="max-width: 100%; border-radius: 10px;">
        `;
  } catch (error) {
    resultDiv.innerHTML = "Error: Could not analyze sentiment.";
    console.error(error);
  }
}
