
const API_URL = "http://127.0.0.1:8000";

let currentVideoId = null;
let videoProcessed = false;

// HTML elements
const videoTitle = document.getElementById("videoTitle");
const videoStatus = document.getElementById("videoStatus");
const processBtn = document.getElementById("processBtn");
const sendBtn = document.getElementById("sendBtn");
const questionInput = document.getElementById("questionInput");
const chatMessages = document.getElementById("chatMessages");
const loading = document.getElementById("loading");
const summarizeBtn = document.getElementById("summarizeBtn");
const summaryContainer = document.getElementById("summaryContainer");
const summaryContent = document.getElementById("summaryContent");

// Display messages
function addMessage(message, type) {
    const div = document.createElement("div");
    div.className = type === "user"
        ? "user-message"
        : "bot-message";

    div.textContent = message;
    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Display AI answer and timestamp sources
function displayAnswer(data) {
    const div = document.createElement("div");
    div.className = "bot-message";

    const answer = document.createElement("p");
    answer.textContent = data.answer || "No answer received.";
    div.appendChild(answer);

    if (data.sources && data.sources.length > 0) {
        const heading = document.createElement("p");
        heading.textContent = "Sources:";
        heading.style.marginTop = "10px";
        div.appendChild(heading);

        data.sources.forEach(source => {
            const link = document.createElement("a");
            const seconds = Math.floor(source.start || 0);

            const minutes = Math.floor(seconds / 60);
            const remainingSeconds = seconds % 60;
            const timestamp =
                `${minutes}:${String(remainingSeconds).padStart(2, "0")}`;

            link.href =
                `https://www.youtube.com/watch?v=${currentVideoId}&t=${seconds}s`;

            link.target = "_blank";
            link.textContent = `▶ ${timestamp} - ${source.text.slice(0, 100)}...`;
            link.style.display = "block";
            link.style.marginTop = "6px";
            link.style.fontSize = "11px";

            div.appendChild(link);
        });
    }

    chatMessages.appendChild(div);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Detect current YouTube video

async function detectVideo() {
    try {
        const tabs = await chrome.tabs.query({
            active: true,
            currentWindow: true
        });

        const tab = tabs[0];

        if (!tab || !tab.url) {
            throw new Error("No active browser tab found.");
        }

        const url = new URL(tab.url);

        if (
            url.hostname !== "www.youtube.com" ||
            url.pathname !== "/watch"
        ) {
            throw new Error("Please open a YouTube video first.");
        }

        currentVideoId = url.searchParams.get("v");

        if (!currentVideoId) {
            throw new Error("Please open a YouTube video first.");
        }

        // Get title directly from Chrome
        videoTitle.textContent = tab.title
            ? tab.title.replace(" - YouTube", "")
            : "YouTube Video";

        videoStatus.textContent =
            "Video detected successfully";

    } catch (error) {
        currentVideoId = null;
        videoTitle.textContent = "No video detected";
        videoStatus.textContent = error.message;
    }
}
// Process YouTube video
processBtn.addEventListener("click", async () => {
    if (!currentVideoId) {
        addMessage("Please open a YouTube video first.", "bot");
        return;
    }

    try {
        processBtn.disabled = true;
        loading.classList.remove("hidden");
        loading.textContent = "Processing video...";

        videoStatus.textContent = "Processing transcript...";

        const response = await fetch(`${API_URL}/ingest`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                video_id: currentVideoId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Video processing failed.");
        }

        videoProcessed = true;

        videoStatus.textContent = "Video processed successfully";

        addMessage(
            `Video processed successfully! ${data.chunks_created} chunks created. You can now ask questions.`,
            "bot"
        );

    } catch (error) {
        videoStatus.textContent = "Processing failed";
        addMessage(`Error: ${error.message}`, "bot");

    } finally {
        processBtn.disabled = false;
        loading.classList.add("hidden");
    }
});

// Ask a question
sendBtn.addEventListener("click", askQuestion);

questionInput.addEventListener("keydown", event => {
    if (event.key === "Enter") {
        askQuestion();
    }
});

async function askQuestion() {
    const question = questionInput.value.trim();

    if (!question) {
        return;
    }

    if (!currentVideoId) {
        addMessage("Please open a YouTube video first.", "bot");
        return;
    }

    if (!videoProcessed) {
        addMessage("Please process this video before asking questions.", "bot");
        return;
    }

    addMessage(question, "user");
    questionInput.value = "";

    sendBtn.disabled = true;
    loading.classList.remove("hidden");
    loading.textContent = "AI is thinking...";

    try {
        const response = await fetch(`${API_URL}/ask`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                video_id: currentVideoId,
                question: question
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Failed to get answer.");
        }

        displayAnswer(data);

    } catch (error) {
        addMessage(`Error: ${error.message}`, "bot");

    } finally {
        sendBtn.disabled = false;
        loading.classList.add("hidden");
    }
}

// Detect video when popup opens
if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", detectVideo, {
        once: true
    });
} else {
    detectVideo();
}


// Summarize the complete YouTube video
summarizeBtn.addEventListener("click", async () => {

    if (!currentVideoId) {
        addMessage("Please open a YouTube video first.", "bot");
        return;
    }

    if (!videoProcessed) {
        addMessage("Please process the video first.", "bot");
        return;
    }

    try {
        summarizeBtn.disabled = true;
        loading.classList.remove("hidden");
        loading.textContent = "Generating complete video summary...";

        const response = await fetch(`${API_URL}/summarize`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                video_id: currentVideoId
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Summary generation failed.");
        }

        summaryContent.textContent = data.summary;
        summaryContainer.classList.remove("hidden");

    } catch (error) {
        addMessage(`Summary error: ${error.message}`, "bot");

    } finally {
        summarizeBtn.disabled = false;
        loading.classList.add("hidden");
    }
});