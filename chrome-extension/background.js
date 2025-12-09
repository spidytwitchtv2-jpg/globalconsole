// Background service worker for intercepting network requests

const TARGET_API = 'https://v2.mnitnetwork.com/api/v1/mnitnetworkcom/dashboard/getconsole';
const FIXED_BACKEND_URL = 'https://globalconsole-sthc.onrender.com/api/console-data';
let backendUrl = FIXED_BACKEND_URL;
let isEnabled = true;
let userEmail = 'Aktermamber.00.7@gmail.com';
let userPassword = 'Bd55555$';

// Load settings from storage
chrome.storage.sync.get(['isEnabled', 'email', 'password'], (result) => {
  // Backend URL is now fixed, don't load from storage
  if (result.isEnabled !== undefined) {
    isEnabled = result.isEnabled;
  }
  if (result.email) {
    userEmail = result.email;
  }
  if (result.password) {
    userPassword = result.password;
  }
  console.log('Console Interceptor loaded:', { backendUrl: FIXED_BACKEND_URL, isEnabled, email: userEmail });
});

// Listen for storage changes
chrome.storage.onChanged.addListener((changes, namespace) => {
  if (namespace === 'sync') {
    // Backend URL is fixed, ignore changes
    if (changes.isEnabled) {
      isEnabled = changes.isEnabled.newValue;
      console.log('Interceptor enabled:', isEnabled);
    }
    if (changes.email) {
      userEmail = changes.email.newValue;
      console.log('Email updated:', userEmail);
    }
    if (changes.password) {
      userPassword = changes.password.newValue;
      console.log('Password updated');
    }
  }
});

// Listen for messages from content script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'API_RESPONSE') {
    if (!isEnabled) {
      console.log('Interceptor disabled, skipping...');
      sendResponse({ success: false, message: 'Interceptor is disabled' });
      return;
    }

    console.log('Intercepted API response:', request.data);
    
    // Forward to backend
    forwardToBackend(request.data)
      .then(result => {
        console.log('Successfully forwarded to backend:', result);
        sendResponse({ success: true, result });
      })
      .catch(error => {
        console.error('Error forwarding to backend:', error);
        sendResponse({ success: false, error: error.message });
      });
    
    return true; // Keep message channel open for async response
  }
  
  if (request.type === 'GET_STATUS') {
    sendResponse({ isEnabled, backendUrl: FIXED_BACKEND_URL, email: userEmail });
    return true;
  }
  
  if (request.type === 'GET_CREDENTIALS') {
    sendResponse({ email: userEmail, password: userPassword });
    return true;
  }
});

// Forward data to backend
async function forwardToBackend(data) {
  try {
    const response = await fetch(backendUrl, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data)
    });

    if (!response.ok) {
      throw new Error(`Backend responded with status: ${response.status}`);
    }

    const result = await response.json();
    
    // Update badge to show success
    chrome.action.setBadgeText({ text: '✓' });
    chrome.action.setBadgeBackgroundColor({ color: '#4CAF50' });
    setTimeout(() => {
      chrome.action.setBadgeText({ text: '' });
    }, 2000);
    
    return result;
  } catch (error) {
    // Update badge to show error
    chrome.action.setBadgeText({ text: '✗' });
    chrome.action.setBadgeBackgroundColor({ color: '#f44336' });
    setTimeout(() => {
      chrome.action.setBadgeText({ text: '' });
    }, 2000);
    
    throw error;
  }
}

// Set initial badge
chrome.action.setBadgeText({ text: '' });

console.log('Console Data Interceptor background script loaded');
