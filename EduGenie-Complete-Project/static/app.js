const form = document.querySelector('#study-form');
const task = document.querySelector('#task');
const textInput = document.querySelector('#text');
const submit = document.querySelector('#submit');
const statusBox = document.querySelector('#status');
const resultCard = document.querySelector('#result-card');
const resultBox = document.querySelector('#result');
const modeNote = document.querySelector('#mode-note');
const labels = {qa:'Your question', explain:'What would you like explained?', quiz:'Paste your notes or a topic', summarize:'Paste the text to summarize', 'learn/recommendations':'What would you like to learn?'};
const hints = {qa:'For example: Why do we have seasons?', explain:'For example: How does photosynthesis work?', quiz:'Paste a passage, or enter a topic to practice.', summarize:'Paste a paragraph or your study notes.', 'learn/recommendations':'For example: I want to learn SQL from scratch.'};
const endpoints = {qa:'/qa', explain:'/explain', quiz:'/quiz', summarize:'/summarize', 'learn/recommendations':'/learn/recommendations'};

function updateTask() {
  document.querySelector('#input-label').textContent = labels[task.value];
  textInput.placeholder = hints[task.value];
  const showLevel = task.value === 'learn/recommendations';
  document.querySelector('#level-label').hidden = !showLevel;
  document.querySelector('#level-wrap').hidden = !showLevel;
}
task.addEventListener('change', updateTask);
textInput.addEventListener('input', () => document.querySelector('#char-count').textContent = `${textInput.value.length.toLocaleString()} / 20,000`);

function renderAnswer(data) {
  resultBox.replaceChildren();
  if (Array.isArray(data.result)) {
    data.result.forEach((item, index) => {
      const wrapper = document.createElement('article'); wrapper.className = 'quiz-item';
      const question = document.createElement('p'); question.textContent = `${index + 1}. ${item.question}`;
      const options = document.createElement('ol');
      item.options.forEach(option => { const li = document.createElement('li'); li.textContent = option; options.append(li); });
      const answer = document.createElement('p'); answer.className = 'quiz-answer'; answer.textContent = `Answer: ${item.answer}${item.explanation ? ` — ${item.explanation}` : ''}`;
      wrapper.append(question, options, answer); resultBox.append(wrapper);
    });
  } else {
    const content = document.createElement('div'); content.className = 'result-content'; content.textContent = data.result;
    resultBox.append(content);
  }
  modeNote.textContent = data.mode === 'offline-demo' ? 'Offline demo response · add a Gemini key for AI-generated results.' : 'Generated with Gemini · review important facts with trusted sources.';
  resultCard.hidden = false;
}

form.addEventListener('submit', async event => {
  event.preventDefault();
  statusBox.className = 'status'; statusBox.textContent = 'Working on it…';
  resultCard.hidden = true; submit.disabled = true;
  try {
    const payload = {text: textInput.value.trim(), level: document.querySelector('#level').value};
    const response = await fetch(endpoints[task.value], {method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(payload)});
    const data = await response.json();
    if (!response.ok) throw new Error(data.detail || 'Something went wrong. Please try again.');
    renderAnswer(data); statusBox.textContent = '';
  } catch (error) {
    statusBox.className = 'status error'; statusBox.textContent = error.message || 'Could not reach EduGenie. Check that the app is running.';
  } finally { submit.disabled = false; }
});

document.querySelector('#copy').addEventListener('click', async () => {
  const button = document.querySelector('#copy');
  try { await navigator.clipboard.writeText(resultBox.innerText); button.textContent = 'Copied'; setTimeout(() => button.textContent = 'Copy', 1500); }
  catch { button.textContent = 'Select and copy'; setTimeout(() => button.textContent = 'Copy', 1800); }
});
updateTask();
