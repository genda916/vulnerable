function toggleLanguage() {
  const isKannada = document.body.classList.toggle('kn');

  document.getElementById('title').innerText = isKannada ? "ಡಿಬಿಟಿ ಯೋಜನೆ - ಅರ್ಜಿ ನಮೂನೆ" : "DBT Scheme - Application Form";
  document.getElementById('mobileLabel').innerText = isKannada ? "ಮೊಬೈಲ್ ಸಂಖ್ಯೆ" : "Mobile Number";
  document.getElementById('aadharLabel').innerText = isKannada ? "ಆಧಾರ್ ಸಂಖ್ಯೆ" : "Aadhar Number";
  document.getElementById('submitBtn').innerText = isKannada ? "ಮುಂದೆ ಸಾಗು" : "Proceed";
  document.getElementById('payMsg').innerText = isKannada ? "ದಯವಿಟ್ಟು ₹100 ಪಾವತಿಸಿ ಪಾವತಿ ದೃಢೀಕರಣಕ್ಕಾಗಿ" : "Please pay ₹100 for verification";
  document.getElementById('success-popup').innerText = isKannada ? "ಅರ್ಹತೆ ದೃಢಪಟ್ಟಿದೆ. ₹3500 3–5 ದಿನಗಳಲ್ಲಿ ಜಮೆ ಆಗುತ್ತದೆ." : "Eligibility confirmed. ₹3500 will be credited in 3–5 days.";
}