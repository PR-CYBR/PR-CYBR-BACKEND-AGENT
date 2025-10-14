async function fetchWorkflows() {
  const response = await fetch('/api/workflows');
  if (!response.ok) {
    throw new Error('Unable to load workflow registry');
  }
  const payload = await response.json();
  return payload.workflows || [];
}

async function fetchWorkflowDetail(name) {
  const response = await fetch(`/api/workflows/${name}`);
  if (!response.ok) {
    return { error: 'Workflow not found' };
  }
  return response.json();
}

function populateSelect(selectEl, workflows) {
  selectEl.innerHTML = '';
  workflows.forEach((workflow) => {
    const option = document.createElement('option');
    option.value = workflow.name;
    option.textContent = workflow.name;
    selectEl.appendChild(option);
  });
}

function renderJson(targetEl, data) {
  targetEl.textContent = JSON.stringify(data, null, 2);
}

document.addEventListener('DOMContentLoaded', async () => {
  const selectEl = document.getElementById('workflow-select');
  const jsonEl = document.getElementById('workflow-json');

  try {
    const workflows = await fetchWorkflows();
    populateSelect(selectEl, workflows);
    if (workflows.length > 0) {
      const detail = await fetchWorkflowDetail(workflows[0].name);
      renderJson(jsonEl, detail);
    }
  } catch (error) {
    renderJson(jsonEl, { error: error.message });
  }

  selectEl.addEventListener('change', async (event) => {
    const detail = await fetchWorkflowDetail(event.target.value);
    renderJson(jsonEl, detail);
  });
});
