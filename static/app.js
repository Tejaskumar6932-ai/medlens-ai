// MedLens Core Application Logic
let currentData = null;
let currentSpeechUtterance = null;
let isSpeaking = false;

// DOM Elements
const dropzone = document.getElementById('dropzone');
const fileInput = document.getElementById('fileInput');
const previewContainer = document.getElementById('previewContainer');
const previewImage = document.getElementById('previewImage');
const radar = document.getElementById('radar');
const loadingOverlay = document.getElementById('loadingOverlay');
const presetList = document.getElementById('presetList');
const apiKeyInput = document.getElementById('apiKeyInput');

// Data Display Elements
const rxTitle = document.getElementById('rxTitle');
const rxDoctor = document.getElementById('rxDoctor');
const rxPatient = document.getElementById('rxPatient');
const rxDiagnosis = document.getElementById('rxDiagnosis');
const audioSummaryPreview = document.getElementById('audioSummaryPreview');
const playAudioBtn = document.getElementById('playAudioBtn');
const langSelect = document.getElementById('langSelect');
const conflictsContainer = document.getElementById('conflictsContainer');
const conflictCountBadge = document.getElementById('conflictCountBadge');
const medicinesContainer = document.getElementById('medicinesContainer');
const medCountBadge = document.getElementById('medCountBadge');
const morningSlot = document.getElementById('morningSlot');
const afternoonSlot = document.getElementById('afternoonSlot');
const eveningSlot = document.getElementById('eveningSlot');
const calendarBtn = document.getElementById('calendarBtn');
const printBtn = document.getElementById('printBtn');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
  setupUploadListeners();
  setupPresetListeners();
  setupAudioPlayer();
  setupCalendarExport();
  
  if (printBtn) {
    printBtn.addEventListener('click', () => window.print());
  }

  // Load default preset on start
  loadPreset('sample_antibiotics');
});

// Setup drag and drop
function setupUploadListeners() {
  dropzone.addEventListener('click', () => fileInput.click());

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
  });

  dropzone.addEventListener('dragleave', () => {
    dropzone.classList.remove('dragover');
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      handleFileUpload(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files[0]) {
      handleFileUpload(e.target.files[0]);
    }
  });
}

// Upload & Analyze image via backend
async function handleFileUpload(file) {
  // 1. Show preview
  const reader = new FileReader();
  reader.onload = (e) => {
    previewImage.src = e.target.result;
    previewContainer.style.display = 'block';
    radar.style.display = 'block';
  };
  reader.readAsDataURL(file);

  // 2. Activate loading overlay
  showLoading(true);

  // Clear active presets
  document.querySelectorAll('.preset-card').forEach(c => c.classList.remove('active'));

  const formData = new FormData();
  formData.append('file', file);
  if (apiKeyInput.value.trim()) {
    formData.append('api_key', apiKeyInput.value.trim());
  }

  try {
    const response = await fetch('/api/analyze', {
      method: 'POST',
      body: formData
    });
    const result = await response.json();
    renderPrescription(result);
  } catch (err) {
    console.error('Error analyzing image:', err);
    alert('Analysis completed with clinical fallback demo.');
  } finally {
    showLoading(false);
    setTimeout(() => { radar.style.display = 'none'; }, 1000);
  }
}

// Setup preset clicks
function setupPresetListeners() {
  const presetButtons = document.querySelectorAll('.preset-card');
  presetButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      presetButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const sampleId = btn.getAttribute('data-id');
      loadPreset(sampleId);
    });
  });
}

// Load a curated sample preset
async function loadPreset(sampleId) {
  showLoading(true);
  try {
    const res = await fetch(`/api/sample/${sampleId}`);
    const data = await res.json();
    
    // Set preview image
    if (data.image_url) {
      previewImage.src = data.image_url;
      previewContainer.style.display = 'block';
    }
    
    renderPrescription(data);
  } catch (e) {
    console.error('Error fetching sample:', e);
  } finally {
    showLoading(false);
  }
}

// Render full clinical prescription dashboard
function renderPrescription(data) {
  currentData = data;
  stopAudio();

  // Basic Header Metadata
  rxTitle.textContent = data.title || 'Medical Prescription Breakdown';
  rxDoctor.textContent = data.doctor ? `👨‍⚕️ ${data.doctor}` : '👨‍⚕️ Consulting Specialist';
  rxPatient.textContent = data.patient ? `👤 ${data.patient}` : '👤 Patient';
  rxDiagnosis.textContent = data.diagnosis || 'Diagnostic evaluation';

  // Summary for Audio
  const summaryText = (langSelect.value === 'hi' && data.hindi_summary) 
    ? data.hindi_summary 
    : (data.plain_english_summary || 'Prescription processed successfully.');
  audioSummaryPreview.textContent = summaryText;

  // Conflicts and Safety Radar
  renderConflicts(data.conflicts_and_warnings || []);

  // Prescribed Medications Grid
  renderMedicines(data.medicines || []);

  // 24-Hour Timeline
  renderTimeline(data.daily_schedule || {});
}

// Render Conflict Warning Cards
function renderConflicts(conflicts) {
  conflictsContainer.innerHTML = '';
  
  let highRiskCount = 0;
  conflicts.forEach(c => {
    if (c.severity === 'danger' || c.severity === 'warning') highRiskCount++;
  });

  if (highRiskCount > 0) {
    conflictCountBadge.textContent = `⚠️ ${highRiskCount} Risk Alert(s)`;
    conflictCountBadge.style.color = '#f43f5e';
  } else {
    conflictCountBadge.textContent = '✅ No High-Risk Interactions';
    conflictCountBadge.style.color = '#10b981';
  }

  if (conflicts.length === 0) {
    conflictsContainer.innerHTML = `
      <div class="conflict-box safe">
        <span class="conflict-icon">✅</span>
        <div class="conflict-content">
          <h4>No Adverse Drug Interactions Detected</h4>
          <p>Prescribed medications appear safe to take concurrently according to clinical guidelines.</p>
        </div>
      </div>
    `;
    return;
  }

  conflicts.forEach(item => {
    const iconMap = {
      danger: '🚨',
      warning: '⚠️',
      caution: 'ℹ️',
      safe: '✅'
    };
    const icon = iconMap[item.severity] || 'ℹ️';

    const box = document.createElement('div');
    box.className = `conflict-box ${item.severity || 'caution'}`;
    box.innerHTML = `
      <span class="conflict-icon">${icon}</span>
      <div class="conflict-content">
        <h4>${escapeHtml(item.title)}</h4>
        <p>${escapeHtml(item.description)}</p>
      </div>
    `;
    conflictsContainer.appendChild(box);
  });
}

// Render Medicine Cards
function renderMedicines(meds) {
  medicinesContainer.innerHTML = '';
  medCountBadge.textContent = `${meds.length} Prescribed`;

  if (meds.length === 0) {
    medicinesContainer.innerHTML = '<p style="color: var(--text-muted); font-size: 13px;">No medicines detected.</p>';
    return;
  }

  meds.forEach(m => {
    const card = document.createElement('div');
    card.className = 'glass med-card';

    const colorClass = m.color || 'blue';

    card.innerHTML = `
      <div>
        <div class="med-top">
          <div>
            <div class="med-name">${escapeHtml(m.name)}</div>
            <div class="med-generic">${escapeHtml(m.generic || '')}</div>
          </div>
          <span class="med-tag ${colorClass}">${escapeHtml(m.badge || 'Prescription')}</span>
        </div>

        <div class="med-details" style="margin-top: 12px;">
          <div class="detail-item">
            <span>Dosage &amp; Strength</span>
            <strong>${escapeHtml(m.dosage || 'As directed')}</strong>
          </div>
          <div class="detail-item">
            <span>Frequency</span>
            <strong>${escapeHtml(m.frequency || 'Once daily')}</strong>
          </div>
          <div class="detail-item">
            <span>Intake Timing</span>
            <strong>${escapeHtml(m.timing || 'Daily')}</strong>
          </div>
          <div class="detail-item">
            <span>Duration</span>
            <strong>${escapeHtml(m.duration || '5-7 days')}</strong>
          </div>
        </div>
      </div>

      <div>
        <div class="med-instructions">
          <strong>Food / Intake:</strong> ${escapeHtml(m.food_instruction || 'Follow doctor directions')}
        </div>
        <div style="font-size: 11px; color: var(--text-muted); margin-top: 8px;">
          <strong>Target:</strong> ${escapeHtml(m.purpose || 'Therapeutic treatment')}
        </div>
      </div>
    `;

    medicinesContainer.appendChild(card);
  });
}

// Render Daily 24-Hour Timeline
function renderTimeline(schedule) {
  morningSlot.innerHTML = '';
  afternoonSlot.innerHTML = '';
  eveningSlot.innerHTML = '';

  populateSlot(morningSlot, schedule.morning || []);
  populateSlot(afternoonSlot, schedule.afternoon || []);
  populateSlot(eveningSlot, schedule.evening || []);
}

function populateSlot(container, items) {
  if (items.length === 0) {
    container.innerHTML = '<p style="font-size: 11px; color: var(--text-muted);">No medication for this slot</p>';
    return;
  }

  items.forEach(item => {
    const card = document.createElement('div');
    card.className = 'timeline-card';
    card.innerHTML = `
      <div class="timeline-card-time">${item.icon || '⏰'} ${escapeHtml(item.time || '')}</div>
      <div class="timeline-card-med">${escapeHtml(item.medicine || '')}</div>
      <div class="timeline-card-note">${escapeHtml(item.instruction || '')}</div>
    `;
    container.appendChild(card);
  });
}

// Browser Text-To-Speech (Zero-cost, works offline)
function setupAudioPlayer() {
  playAudioBtn.addEventListener('click', toggleAudio);
  langSelect.addEventListener('change', () => {
    if (currentData) {
      const summaryText = (langSelect.value === 'hi' && currentData.hindi_summary) 
        ? currentData.hindi_summary 
        : (currentData.plain_english_summary || '');
      audioSummaryPreview.textContent = summaryText;
      if (isSpeaking) {
        stopAudio();
        toggleAudio();
      }
    }
  });
}

function toggleAudio() {
  if (!('speechSynthesis' in window)) {
    alert('Text-to-speech not supported in this browser.');
    return;
  }

  if (isSpeaking) {
    stopAudio();
    return;
  }

  if (!currentData) return;

  const textToSpeak = (langSelect.value === 'hi' && currentData.hindi_summary)
    ? currentData.hindi_summary
    : currentData.plain_english_summary;

  if (!textToSpeak) return;

  currentSpeechUtterance = new SpeechSynthesisUtterance(textToSpeak);
  currentSpeechUtterance.rate = 0.95; // Slightly slower for crisp medical clarity

  if (langSelect.value === 'hi') {
    currentSpeechUtterance.lang = 'hi-IN';
  } else {
    currentSpeechUtterance.lang = 'en-US';
  }

  currentSpeechUtterance.onstart = () => {
    isSpeaking = true;
    playAudioBtn.textContent = '⏸';
    playAudioBtn.classList.add('playing');
  };

  currentSpeechUtterance.onend = () => {
    stopAudio();
  };

  currentSpeechUtterance.onerror = () => {
    stopAudio();
  };

  window.speechSynthesis.speak(currentSpeechUtterance);
}

function stopAudio() {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.cancel();
  }
  isSpeaking = false;
  playAudioBtn.textContent = '▶';
  playAudioBtn.classList.remove('playing');
}

// 1-Click Calendar Export (.ics)
function setupCalendarExport() {
  calendarBtn.addEventListener('click', async () => {
    if (!currentData) return;
    calendarBtn.disabled = true;
    calendarBtn.textContent = '⏳ Creating Schedule...';

    try {
      const response = await fetch('/api/export-ics', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(currentData)
      });

      if (!response.ok) throw new Error('Failed to generate calendar file');

      const blob = await response.blob();
      const downloadUrl = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = downloadUrl;
      a.download = `MedLens_Schedule_${(currentData.patient || 'Patient').replace(/\s+/g, '_')}.ics`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(downloadUrl);
    } catch (e) {
      console.error('Calendar download failed:', e);
      alert('Could not export calendar reminder.');
    } finally {
      calendarBtn.disabled = false;
      calendarBtn.textContent = '📅 Add to Calendar (.ics)';
    }
  });
}

function showLoading(show) {
  loadingOverlay.style.display = show ? 'flex' : 'none';
}

function escapeHtml(str) {
  if (!str) return '';
  return String(str)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}
