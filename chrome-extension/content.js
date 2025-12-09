// Content script to receive messages from injected script
(function() {
  'use strict';

const TARGET_API = 'https://v2.mnitnetwork.com/api/v1/mnitnetworkcom/dashboard/getconsole';

console.log('%c[Content] Content script loaded', 'color: #4CAF50; font-weight: bold');
console.log('%c[Content] URL:', 'color: #2196F3', window.location.href);
console.log('%c[Content] Target API:', 'color: #2196F3', TARGET_API);

// Listen for messages from injected script
window.addEventListener('message', (event) => {
  // Only accept messages from same origin
  if (event.source !== window) return;
  
  if (event.data.type === 'GETCONSOLE_INTERCEPTED') {
    console.log('%c[Content] ✓ Received data from injected script!', 'color: #4CAF50; font-weight: bold');
    console.log('%c[Content] Data:', 'color: #4CAF50', event.data.data);
    
    // Forward to background script
    chrome.runtime.sendMessage({
      type: 'API_RESPONSE',
      data: event.data.data,
      url: event.data.url,
      timestamp: new Date().toISOString()
    }, (response) => {
      if (chrome.runtime.lastError) {
        console.error('%c[Content] ✗ Error sending to background:', 'color: #f44336', chrome.runtime.lastError);
      } else {
        console.log('%c[Content] ✓ Forwarded to backend:', 'color: #4CAF50', response);
      }
    });
  }
});

console.log('%c[Content] ✓ Message listener installed', 'color: #4CAF50');

// Log when page is fully loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    console.log('%c[Content] ✓ Page loaded, ready to receive messages', 'color: #4CAF50');
  });
} else {
  console.log('%c[Content] ✓ Page already loaded, ready to receive messages', 'color: #4CAF50');
}

console.log('%c[Content] 💡 Check for [Injected] logs to see interception', 'color: #2196F3');

})();
