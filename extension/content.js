
// Listen for requests from the extension popup
chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {

        if (request.action === "getVideoInfo") {

            const url = new URL(window.location.href);

            // Get YouTube video ID
            const videoId = url.searchParams.get("v");

            // Get video title
            const videoTitle =
                document.querySelector("h1 yt-formatted-string")
                ?.textContent ||
                document.title.replace(" - YouTube", "");

            if (videoId) {
                sendResponse({
                    videoId: videoId,
                    videoTitle: videoTitle
                });
            } else {
                sendResponse({
                    videoId: null,
                    videoTitle: "No video detected"
                });
            }
        }
    }
);