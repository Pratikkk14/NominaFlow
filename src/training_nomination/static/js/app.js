/**
 * NominaFlow Frontend Client Helper
 */

// Helper to make JSON API calls with cookie / token support
async function apiCall(url, method = "GET", body = null) {
  const options = {
    method,
    headers: {},
  };

  if (body) {
    options.headers["Content-Type"] = "application/json";
    options.body = JSON.stringify(body);
  }

  const response = await fetch(url, options);
  const data = await response.json().catch(() => ({}));

  if (!response.ok) {
    const errorMsg = data.detail || `Request failed with status ${response.status}`;
    throw new Error(errorMsg);
  }

  return data;
}

// Quick Login Demo Helper
function quickLogin(email, password) {
  const emailInput = document.getElementById("loginEmail");
  const passwordInput = document.getElementById("loginPassword");
  if (emailInput && passwordInput) {
    emailInput.value = email;
    passwordInput.value = password;
    const form = document.getElementById("loginForm");
    if (form) form.dispatchEvent(new Event("submit"));
  }
}

// Modal management
function openModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.add("active");
}

function closeModal(modalId) {
  const modal = document.getElementById(modalId);
  if (modal) modal.classList.remove("active");
}

// Global Toast / Message banner
function showToast(message, type = "info") {
  const container = document.getElementById("toastContainer");
  if (!container) {
    alert(message);
    return;
  }
  const alertDiv = document.createElement("div");
  alertDiv.className = `alert alert-${type}`;
  alertDiv.textContent = message;
  container.appendChild(alertDiv);
  setTimeout(() => alertDiv.remove(), 4000);
}
