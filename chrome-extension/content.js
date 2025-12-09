// Content script to intercept fetch/XHR requests

const TARGET_API = 'https://v2.mnitnetwork.com/api/v1/mnitnetworkcom/dashboard/getconsole';

console.log('Console Data Interceptor content script loaded');

// Intercept fetch requests
const originalFetch = window.fetch;
window.fetch = async function(...args) {
  const [url, options] = args;
  
  // Call original fetch
  const response = await originalFetch.apply(this, args);
  
  // Check if this is the target API
  if (url.includes('/dashboard/getconsole')) {
    console.log('Intercepted getconsole API call');
    
    // Clone the response so we can read it without consuming it
    const clonedResponse = response.clone();
    
    try {
      const data = await clonedResponse.json();
      console.log('Console API data:', data);
      
      // Send to background script
      chrome.runtime.sendMessage({
        type: 'API_RESPONSE',
        data: data,
        url: url,
        timestamp: new Date().toISOString()
      }, (response) => {
        if (chrome.runtime.lastError) {
          console.error('Error sending to background:', chrome.runtime.lastError);
        } else {
          console.log('Data forwarded to backend:', response);
        }
      });
    } catch (error) {
      console.error('Error processing intercepted response:', error);
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
  if (this._url && this._url.includes('/dashboard/getconsole')) {
    console.log('Intercepted XHR getconsole API call');
    
    this.addEventListener('load', function() {
      try {
        const data = JSON.parse(this.responseText);
        console.log('Console API data (XHR):', data);
        
        // Send to background script
        chrome.runtime.sendMessage({
          type: 'API_RESPONSE',
          data: data,
          url: this._url,
          timestamp: new Date().toISOString()
        }, (response) => {
          if (chrome.runtime.lastError) {
            console.error('Error sending to background:', chrome.runtime.lastError);
          } else {
            console.log('Data forwarded to backend:', response);
          }
        });
      } catch (error) {
        console.error('Error processing XHR response:', error);
      }
    });
  }
  
  return originalSend.apply(this, args);
};

console.log('Fetch and XHR interceptors installed');
