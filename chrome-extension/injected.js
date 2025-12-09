// This script runs in the page context (MAIN world)
// It can intercept fetch/XHR before any page scripts run

(function() {
  'use strict';
  
  console.log('%c[Injected] Script loaded in MAIN world', 'color: #FF5722; font-weight: bold');
  
  // Intercept fetch
  const originalFetch = window.fetch;
  window.fetch = async function(...args) {
    const [url, options] = args;
    const urlString = typeof url === 'string' ? url : url.toString();
    
    console.log('%c[Injected] Fetch intercepted:', 'color: #FF5722', urlString);
    
    // Call original
    const response = await originalFetch.apply(this, args);
    
    // Check for getconsole
    if (urlString.includes('getconsole')) {
      console.log('%c[Injected] ✓ MATCHED getconsole!', 'color: #FF5722; font-weight: bold');
      
      const clonedResponse = response.clone();
      try {
        const data = await clonedResponse.json();
        console.log('%c[Injected] ✓ Data:', 'color: #FF5722', data);
        
        // Post message to content script
        window.postMessage({
          type: 'GETCONSOLE_INTERCEPTED',
          data: data,
          url: urlString
        }, '*');
        
      } catch (error) {
        console.error('%c[Injected] ✗ Error:', 'color: #FF5722', error);
      }
    }
    
    return response;
  };
  
  // Intercept XHR
  const originalOpen = XMLHttpRequest.prototype.open;
  const originalSend = XMLHttpRequest.prototype.send;
  
  XMLHttpRequest.prototype.open = function(method, url, ...rest) {
    this._url = url;
    this._method = method;
    console.log('%c[Injected] XHR.open:', 'color: #FF5722', url);
    return originalOpen.apply(this, [method, url, ...rest]);
  };
  
  XMLHttpRequest.prototype.send = function(...args) {
    const url = this._url || '';
    
    if (url.includes('getconsole')) {
      console.log('%c[Injected] ✓ MATCHED XHR getconsole!', 'color: #FF5722; font-weight: bold');
      
      this.addEventListener('load', function() {
        try {
          const data = JSON.parse(this.responseText);
          console.log('%c[Injected] ✓ XHR Data:', 'color: #FF5722', data);
          
          // Post message to content script
          window.postMessage({
            type: 'GETCONSOLE_INTERCEPTED',
            data: data,
            url: url
          }, '*');
          
        } catch (error) {
          console.error('%c[Injected] ✗ XHR Error:', 'color: #FF5722', error);
        }
      });
    }
    
    return originalSend.apply(this, args);
  };
  
  console.log('%c[Injected] ✓ Interceptors installed in MAIN world', 'color: #FF5722; font-weight: bold');
  
})();
