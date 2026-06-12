// expertise.js

document.addEventListener("DOMContentLoaded", () => {
  const skillsGrid = document.getElementById("skills-grid");
  const technicalBtn = document.getElementById("technical-btn");
  const softBtn = document.getElementById("soft-btn");

  const technicalSkills = {
    Python: "Building automated data pipelines, orchestrating workflows, cleaning and transforming datasets, and integrating external systems through API interactions.",
    Django: "Developing full‑stack web applications from scratch and deploying to cloud environments.",
    Dagster: "Enhancing business‑critical pipelines with data quality checks, asset‑based orchestration, and modular, testable workflows.",
    SQL: "Leveraging window functions, recursive CTEs, and delta logic to drive analytical insights and support complex ad‑hoc analyses.",
    BigQuery: "Designing performant SQL models, optimizing warehouse queries, and scheduling automated jobs for large‑scale analytics.",
    VBA: "Building standalone data‑cleaning and reporting tools using ODBC integrations and Google Cloud SDK automation.",
    "Google Cloud Platform": "Utilizing Cloud Storage, and BigQuery for data processing, storage, and automation.",
    "CI/CD Automation": "Coming soon, check my ongoing projects for examples of my work in this area."
  };

  const softSkills = {
    "Cross‑Functional Communication": "Collaborating effectively across technical and non-technical teams.",
    "Technical Leadership": "Guiding engineering decisions and mentoring team members.",
    "Analytical Problem Solving": "Breaking down complex challenges into actionable solutions.",
    "Stakeholder Alignment": "Ensuring technical goals align with business objectives.",
    "Project Ownership": "Taking responsibility for project outcomes and delivery.",
    "Strategic Thinking": "Planning long-term solutions that scale with organizational needs."
  };

    function renderSkills(skills) {
    skillsGrid.innerHTML = Object.keys(skills)
        .map(skill => `
        <div class="col-md-3">
            <div class="skill-wrapper">
            <button class="skill-card" data-skill="${skill}">
                ${skill}
            </button>
            <div class="skill-detail" id="detail-${skill.replace(/\s+/g, '-')}">
                ${skills[skill]}
            </div>
            </div>
        </div>
        `)
        .join("");

    document.querySelectorAll(".skill-card").forEach(card => {
        card.addEventListener("click", () => {
        const skillName = card.dataset.skill;
        const detailBox = document.getElementById(
            `detail-${skillName.replace(/\s+/g, '-')}`
        );

        document.querySelectorAll(".skill-detail").forEach(box => {
            if (box !== detailBox) box.classList.remove("open");
        });

        detailBox.classList.toggle("open");
        });
    });
    }

  technicalBtn.addEventListener("click", () => {
    renderSkills(technicalSkills);
    technicalBtn.classList.add("active");
    softBtn.classList.remove("active");
  });

  softBtn.addEventListener("click", () => {
    renderSkills(softSkills);
    softBtn.classList.add("active");
    technicalBtn.classList.remove("active");
  });

  renderSkills(technicalSkills);
});
