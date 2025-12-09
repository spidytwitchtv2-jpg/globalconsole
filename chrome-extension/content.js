// Content script to intercept fetch/XHR requests

const TARGET_API = 'https://v2.mnitnetwork.com/api/v1/mnitnetworkcom/dashboard/getconsole';

console.log('Console Data Interceptor content script loaded on:', window.location.href);

// Intercept fetch requests
const originalFetch = window.fetch;
window.fetch = async function(...args) {
  const [url, options] = args;
  
  console.log('Fetch intercepted:', url);
  
  // Call original fetch
  const response = await originalFetch.apply(this, args);
  
  // Check if this is the target API - check both relative and absolute URLs
  const urlString = typeof url === 'string' ? url : url.toString();
  if (urlString.includes('/dashboard/getconsole') || urlString.includes('getconsole')) {
    console.log('✓ Matched getconsole API call:', urlString);
    
    // Clone the response so we can read it without consuming it
    const clonedResponse = response.clone();
    
    try {
      const data = await clonedResponse.json();
      console.log('✓ Console API data intercepted:', data);
      
      // Send to background script
      chrome.runtime.sendMessage({
        type: 'API_RESPONSE',
        data: data,
        url: urlString,
        timestamp: new Date().toISOString()
      }, (response) => {
        if (chrome.runtime.lastError) {
          console.error('✗ Error sending to background:', chrome.runtime.lastError);
        } else {
          console.log('✓ Data forwarded to backend:', response);
        }
      });
    } catch (error) {
      console.error('✗ Error processing intercepted response:', error);
    }
  }
  
  return response;
};

// Intercept XMLHttpRequest
const originalOpen = XMLHttpRequest.prototype.open;
const originalSend = XMLHttpRequest.prototype.send;

XMLHttpRequest.prototype.open = function(method, url, ...rest) {
  this._url = url;
  this._method = method;
  return originalOpen.apply(this, [method, url, ...rest]);
};

XMLHttpRequest.prototype.send = function(...args) {
  console.log('XHR send intercepted:', this._url);
  
  if (this._url && (this._url.includes('/dashboard/getconsole') || this._url.includes('getconsole'))) {
    console.log('✓ Matched XHR getconsole API call:', this._url);
    
    this.addEventListener('load', function() {
      try {
        const data = JSON.parse(this.responseText);
        console.log('✓ Console API data (XHR) intercepted:', data);
        
        // Send to background script
        chrome.runtime.sendMessage({
          type: 'API_RESPONSE',
          data: data,
          url: this._url,
          timestamp: new Date().toISOString()
        }, (response) => {
          if (chrome.runtime.lastError) {
            console.error('✗ Error sending to background:', chrome.runtime.lastError);
          } else {
            console.log('✓ Data forwarded to backend:', response);
          }
        });
      } catch (error) {
        console.error('✗ Error processing XHR response:', error);
      }
    });
  }
  
  return originalSend.apply(this, args);
};

console.log('✓ Fetch and XHR interceptors installed successfully');

// Log when page is fully loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    console.log('✓ Page loaded, interceptors ready');
  });
} else {
  console.log('✓ Page already loaded, interceptors ready');
}
