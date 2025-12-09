// Content script to intercept fetch/XHR requests
(function() {
  'use strict';

const TARGET_API = 'https://v2.mnitnetwork.com/api/v1/mnitnetworkcom/dashboard/getconsole';

console.log('%c[Interceptor] Content script loaded', 'color: #4CAF50; font-weight: bold');
console.log('%c[Interceptor] URL:', 'color: #2196F3', window.location.href);
console.log('%c[Interceptor] Target API:', 'color: #2196F3', TARGET_API);

// Intercept fetch requests - MUST be synchronous override
const originalFetch = window.fetch;
let fetchCallCount = 0;
window.fetch = async function(...args) {
  const [url, options] = args;
  
  fetchCallCount++;
  const urlString = typeof url === 'string' ? url : url.toString();
  console.log(`%c[Interceptor] Fetch call #${fetchCallCount}:`, 'color: #9E9E9E', urlString);
  
  // Call original fetch
  const response = await originalFetch.apply(this, args);
  
  // Check if this is the target API - check both relative and absolute URLs
  if (urlString.includes('getconsole') || urlString.includes('/dashboard/getconsole')) {
    console.log('%c[Interceptor] ✓ MATCHED getconsole API!', 'color: #4CAF50; font-weight: bold', urlString);
    console.log('%c[Interceptor] Response status:', 'color: #2196F3', response.status);
    
    // Clone the response so we can read it without consuming it
    const clonedResponse = response.clone();
    
    try {
      const data = await clonedResponse.json();
      console.log('%c[Interceptor] ✓ Data intercepted:', 'color: #4CAF50', data);
      
      // Send to background script
      chrome.runtime.sendMessage({
        type: 'API_RESPONSE',
        data: data,
        url: urlString,
        timestamp: new Date().toISOString()
      }, (msgResponse) => {
        if (chrome.runtime.lastError) {
          console.error('%c[Interceptor] ✗ Error sending to background:', 'color: #f44336', chrome.runtime.lastError);
        } else {
          console.log('%c[Interceptor] ✓ Forwarded to backend:', 'color: #4CAF50', msgResponse);
        }
      });
    } catch (error) {
      console.error('%c[Interceptor] ✗ Error processing response:', 'color: #f44336', error);
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

let xhrCallCount = 0;
XMLHttpRequest.prototype.send = function(...args) {
  const url = this._url || '';
  xhrCallCount++;
  console.log(`%c[Interceptor] XHR send #${xhrCallCount}:`, 'color: #9E9E9E', url);
  
  if (url && (url.includes('getconsole') || url.includes('/dashboard/getconsole'))) {
    console.log('%c[Interceptor] ✓ MATCHED XHR getconsole API!', 'color: #4CAF50; font-weight: bold', url);
    
    this.addEventListener('load', function() {
      console.log('%c[Interceptor] XHR Response status:', 'color: #2196F3', this.status);
      try {
        const data = JSON.parse(this.responseText);
        console.log('%c[Interceptor] ✓ XHR Data intercepted:', 'color: #4CAF50', data);
        
        // Send to background script
        chrome.runtime.sendMessage({
          type: 'API_RESPONSE',
          data: data,
          url: url,
          timestamp: new Date().toISOString()
        }, (msgResponse) => {
          if (chrome.runtime.lastError) {
            console.error('%c[Interceptor] ✗ Error sending to background:', 'color: #f44336', chrome.runtime.lastError);
          } else {
            console.log('%c[Interceptor] ✓ Forwarded to backend:', 'color: #4CAF50', msgResponse);
          }
        });
      } catch (error) {
        console.error('%c[Interceptor] ✗ Error processing XHR:', 'color: #f44336', error);
      }
    });
  }
  
  return originalSend.apply(this, args);
};

console.log('%c[Interceptor] ✓ Fetch and XHR interceptors installed', 'color: #4CAF50; font-weight: bold');

// Log when page is fully loaded
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    console.log('%c[Interceptor] ✓ Page loaded, interceptors ready', 'color: #4CAF50');
  });
} else {
  console.log('%c[Interceptor] ✓ Page already loaded, interceptors ready', 'color: #4CAF50');
}

// Monitor all network requests via Performance API
if (window.PerformanceObserver) {
  const observer = new PerformanceObserver((list) => {
    for (const entry of list.getEntries()) {
      console.log('%c[Interceptor] 📡 Network request detected:', 'color: #9E9E9E', entry.name);
      if (entry.initiatorType === 'fetch' || entry.initiatorType === 'xmlhttprequest') {
        if (entry.name.includes('getconsole')) {
          console.log('%c[Interceptor] 🔍 Performance API detected getconsole request:', 'color: #FF9800', entry.name);
        }
      }
    }
  });
  observer.observe({ entryTypes: ['resource'] });
  console.log('%c[Interceptor] ✓ Performance observer installed', 'color: #4CAF50');
}

// Also check existing performance entries
setTimeout(() => {
  const entries = performance.getEntriesByType('resource');
  console.log('%c[Interceptor] 📊 Total network requests so far:', 'color: #2196F3', entries.length);
  const getconsoleEntries = entries.filter(e => e.name.includes('getconsole'));
  if (getconsoleEntries.length > 0) {
    console.log('%c[Interceptor] 🎯 Found existing getconsole requests:', 'color: #FF9800', getconsoleEntries);
  }
}, 2000);

// Add a manual trigger function for testing
window.testInterceptor = function() {
  console.log('%c[Interceptor] 🧪 Testing interceptor...', 'color: #9C27B0');
  fetch('https://v2.mnitnetwork.com/api/v1/mnitnetworkcom/dashboard/getconsole', {
    headers: {
      'mhitauth': 'test-token'
    }
  }).then(r => {
    console.log('%c[Interceptor] 🧪 Test fetch completed', 'color: #9C27B0', r.status);
  }).catch(e => {
    console.log('%c[Interceptor] 🧪 Test fetch failed (expected):', 'color: #9C27B0', e.message);
  });
};

console.log('%c[Interceptor] 💡 TIP: Run testInterceptor() to manually test', 'color: #2196F3');

})();
