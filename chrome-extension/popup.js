// Popup script for managing settings

const backendUrlInput = document.getElementById('backendUrl');
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const toggleEnabled = document.getElementById('toggleEnabled');
const saveBtn = document.getElementById('saveBtn');
const testBtn = document.getElementById('testBtn');
const messageDiv = document.getElementById('message');
const interceptCount = document.getElementById('interceptCount');
const successCount = document.getElementById('successCount');

// Load saved settings
chrome.storage.sync.get(['backendUrl', 'isEnabled', 'stats', 'email', 'password'], (result) => {
  if (result.backendUrl) {
    backendUrlInput.value = result.backendUrl;
  }
  if (result.email) {
    emailInput.value = result.email;
  }
  if (result.password) {
    passwordInput.value = result.password;
  }
  if (result.isEnabled !== undefined) {
    toggleEnabled.checked = result.isEnabled;
  }
  if (result.stats) {
    interceptCount.textContent = result.stats.intercepted || 0;
    successCount.textContent = result.stats.forwarded || 0;
  }
});

// Save settings
saveBtn.addEventListener('click', () => {
  const url = backendUrlInput.value.trim();
  const email = emailInput.value.trim();
  const password = passwordInput.value.trim();
  
  if (!url) {
    showMessage('Please enter a backend URL', 'error');
    return;
  }

  // Validate URL format
  try {
    new URL(url);
  } catch (e) {
    showMessage('Invalid URL format', 'error');
    return;
  }

  // Validate email format
  if (email && !email.includes('@')) {
    showMessage('Please enter a valid email', 'error');
    return;
  }

  chrome.storage.sync.set({
    backendUrl: url,
    email: email,
    password: password,
    isEnabled: toggleEnabled.checked
  }, () => {
    showMessage('Settings saved successfully!', 'success');
  });
});

// Toggle enabled state
toggleEnabled.addEventListener('change', () => {
  chrome.storage.sync.set({
    isEnabled: toggleEnabled.checked
  }, () => {
    const status = toggleEnabled.checked ? 'enabled' : 'disabled';
    showMessage(`Interceptor ${status}`, 'success');
  });
});

// Test connection
testBtn.addEventListener('click', async () => {
  const url = backendUrlInput.value.trim();
  
  if (!url) {
    showMessage('Please enter a backend URL', 'error');
    return;
  }

  showMessage('Testing connection...', 'success');
  testBtn.disabled = true;
  testBtn.textContent = 'Testing...';

  try {
    // Send test payload
    const testPayload = {
      meta: {
        status: "success",
        timestamp: new Date().toISOString()
      },
      data: {
        messages: [
          {
            app_name: "Test",
            carrier: "000000XXX",
            sms: "This is a test message from the Chrome extension",
            time: "just now",
            color: "#4CAF50"
          }
        ]
      },
      message: "Test message from Chrome extension"
    };

    const response = await fetch(url, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(testPayload)
    });

    if (response.ok) {
      const result = await response.json();
      showMessage(`✓ Connection successful! ${result.count || 0} messages posted`, 'success');
    } else {
      showMessage(`✗ Connection failed: ${response.status} ${response.statusText}`, 'error');
    }
  } catch (error) {
    showMessage(`✗ Connection error: ${error.message}`, 'error');
  } finally {
    testBtn.disabled = false;
    testBtn.textContent = 'Test Connection';
  }
});

// Show message
function showMessage(text, type) {
  messageDiv.textContent = text;
  messageDiv.className = `message ${type}`;
  
  setTimeout(() => {
    messageDiv.className = 'message';
  }, 3000);
}

// Listen for updates from background script
chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  if (request.type === 'STATS_UPDATE') {
    interceptCount.textContent = request.stats.intercepted || 0;
    successCount.textContent = request.stats.forwarded || 0;
  }
});

// Update stats periodically
setInterval(() => {
  chrome.storage.sync.get(['stats'], (result) => {
    if (result.stats) {
      interceptCount.textContent = result.stats.intercepted || 0;
      successCount.textContent = result.stats.forwarded || 0;
    }
  });
}, 2000);
