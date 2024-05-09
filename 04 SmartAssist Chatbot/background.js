// Add event listener for tab updates
chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
  // Check if the tab update is complete and the URL includes '.amazon.com'
  if (changeInfo.status === 'complete' && tab.url.includes('.amazon.com')) {
    // Show the extension icon in the browser's toolbar for the corresponding tab
    chrome.pageAction.show(tabId);
  }
});
