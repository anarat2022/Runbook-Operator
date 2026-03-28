async function request(path, options = {}) {
  const response = await fetch(path, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });

  if (!response.ok) {
    const payload = await response.json().catch(() => ({}));
    throw new Error(payload.error || "Request failed");
  }

  return response.json();
}

function statusClass(value) {
  return value.toLowerCase().replaceAll(" ", "-");
}

function renderStats(state) {
  const container = document.getElementById("stats-grid");
  if (!container) return;

  const jobs = state.jobs || [];
  const completed = jobs.filter((job) => job.status === "Completed").length;
  const approvals = jobs.filter((job) => job.approval_status === "Pending").length;
  const stats = [
    { label: "Runbooks", value: state.runbooks.length },
    { label: "Jobs", value: jobs.length },
    { label: "Pending approvals", value: approvals },
    { label: "Completed runs", value: completed },
  ];

  container.innerHTML = stats
    .map(
      (stat) => `
        <article class="stat-card">
          <span class="stat-label">${stat.label}</span>
          <strong class="stat-value">${stat.value}</strong>
        </article>
      `
    )
    .join("");
}

function renderRunbooks(state) {
  const container = document.getElementById("runbooks");
  if (!container) return;

  container.innerHTML = state.runbooks
    .map(
      (runbook) => `
        <article class="runbook-card">
          <div class="card-topline">
            <h3>${runbook.name}</h3>
            <span class="pill ${statusClass(runbook.risk_level)}">${runbook.risk_level}</span>
          </div>
          <p>${runbook.summary}</p>
          <div class="meta-row">
            <span>${runbook.system}</span>
            <span>${runbook.allowed_actions.length} actions</span>
          </div>
          <ul class="compact-list">
            ${runbook.steps.map((step) => `<li>${step}</li>`).join("")}
          </ul>
        </article>
      `
    )
    .join("");
}

function renderJobs(state) {
  const container = document.getElementById("jobs");
  if (!container) return;

  container.innerHTML = state.jobs
    .map((job) => {
      const actions = [];
      if (job.approval_status === "Pending") {
        actions.push(
          `<button class="button button-primary action-button" data-action="approve" data-job="${job.id}">Approve & Execute</button>`
        );
        actions.push(
          `<button class="button button-secondary action-button" data-action="reject" data-job="${job.id}">Reject</button>`
        );
      }

      return `
        <article class="job-card">
          <div class="card-topline">
            <h3>${job.title}</h3>
            <span class="pill ${statusClass(job.status)}">${job.status}</span>
          </div>
          <p class="mono">Runbook: ${job.runbook_name}</p>
          <p>${job.risk_summary}</p>
          <ul class="compact-list">
            ${job.execution_plan.map((step) => `<li>${step}</li>`).join("")}
          </ul>
          ${
            job.result_summary
              ? `<div class="result-box"><strong>Result:</strong> ${job.result_summary}</div>`
              : ""
          }
          ${
            job.evidence && job.evidence.length
              ? `<div class="evidence-list">${job.evidence
                  .map((item) => `<span class="evidence-chip">${item}</span>`)
                  .join("")}</div>`
              : ""
          }
          <div class="meta-row">
            <span>${job.requester}</span>
            <span>${job.notion_sync}</span>
          </div>
          <div class="action-row">
            ${actions.join("")}
          </div>
        </article>
      `;
    })
    .join("");

  container.querySelectorAll(".action-button").forEach((button) => {
    button.addEventListener("click", async () => {
      const jobId = button.dataset.job;
      const action = button.dataset.action;
      try {
        if (action === "reject") {
          await request(`/api/jobs/${jobId}/approve`, {
            method: "POST",
            body: JSON.stringify({
              reviewer: "ops lead",
              decision: "reject",
              notes: "Rejected during live demo review.",
            }),
          });
        } else {
          await request(`/api/jobs/${jobId}/approve`, {
            method: "POST",
            body: JSON.stringify({
              reviewer: "ops lead",
              decision: "approve",
              notes: "Approved for execution.",
            }),
          });
          await request(`/api/jobs/${jobId}/run`, { method: "POST" });
        }
        await loadState();
      } catch (error) {
        alert(error.message);
      }
    });
  });
}

function renderAudit(state) {
  const container = document.getElementById("audit-log");
  if (!container) return;

  container.innerHTML = state.audit_log
    .map(
      (entry) => `
        <article class="audit-entry">
          <div class="audit-head">
            <strong>${entry.step}</strong>
            <span class="pill ${statusClass(entry.outcome)}">${entry.outcome}</span>
          </div>
          <p>${entry.action}</p>
          <div class="meta-row mono">
            <span>${entry.job_id}</span>
            <span>${entry.timestamp}</span>
            <span>${entry.source || "Runbook Operator"}</span>
          </div>
        </article>
      `
    )
    .join("");
}

function renderPortal(state) {
  const container = document.getElementById("portal-customers");
  if (!container) return;

  container.innerHTML = state.customers
    .map(
      (customer) => `
        <article class="portal-card">
          <div class="card-topline">
            <h3>${customer.name}</h3>
            <span class="pill ${statusClass(customer.tier)}">${customer.tier}</span>
          </div>
          <p class="mono">${customer.email}</p>
          <p>${customer.fraud_risk ? "Fraud review required" : "No fraud flags detected"}</p>
          ${customer.orders
            .map(
              (order) => `
                <div class="portal-order">
                  <div class="meta-row">
                    <strong>${order.id}</strong>
                    <span>${order.item}</span>
                    <span>$${order.total}</span>
                  </div>
                  <div class="meta-row">
                    <span>Status: ${order.status}</span>
                    <span>Refunded: ${order.refunded ? "Yes" : "No"}</span>
                    <span>Case: ${order.case_status}</span>
                  </div>
                  <p>${order.internal_note || "No internal note yet."}</p>
                </div>
              `
            )
            .join("")}
        </article>
      `
    )
    .join("");
}

async function loadState() {
  const state = await request("/api/state");
  renderStats(state);
  renderRunbooks(state);
  renderJobs(state);
  renderAudit(state);
  renderPortal(state);
}

function bindForm() {
  const form = document.getElementById("job-form");
  if (!form) return;

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const formData = new FormData(form);
    const payload = Object.fromEntries(formData.entries());
    try {
      await request("/api/jobs", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      await loadState();
    } catch (error) {
      alert(error.message);
    }
  });
}

function bindReset() {
  const button = document.getElementById("reset-demo");
  if (!button) return;

  button.addEventListener("click", async () => {
    await request("/api/reset", { method: "POST" });
    await loadState();
  });
}

document.addEventListener("DOMContentLoaded", async () => {
  bindForm();
  bindReset();
  await loadState();

  if (document.body.dataset.view === "portal") {
    window.setInterval(loadState, 3000);
  }
});

