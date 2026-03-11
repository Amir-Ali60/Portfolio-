/**
 * script.js — Portfolio Main JavaScript
 * ========================================
 * All frontend behavior lives here.
 *
 * Features:
 *   1. Navbar scroll effect & active link highlighting
 *   2. Mobile hamburger menu toggle
 *   3. Dark / Light theme toggle (with localStorage)
 *   4. Scroll reveal animations (Intersection Observer)
 *   5. Typing animation in hero section
 *   6. Load & render Skills from Flask API
 *   7. Load & render Projects from Flask API
 *   8. Project filter buttons
 *   9. Contact form AJAX submission
 *  10. Smooth scroll to hash links
 */


// ─── Configuration ────────────────────────────────────────────────────────────
/** Base URL for the Flask API.
 *  When Flask serves index.html at http://localhost:5000/
 *  the API is at /api/...  so this is just "" (empty).
 */
const API_BASE = "";


// ─── DOMContentLoaded ─────────────────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
  initTheme();           // 3. Apply saved theme preference
  initNavbar();          // 1. Navbar scroll & active links
  initMobileMenu();      // 2. Hamburger toggle
  initScrollReveal();    // 4. Animate elements on scroll
  initTypingEffect();    // 5. Hero typing animation
  loadSkills();          // 6. Fetch & render skills
  loadProjects();        // 7. Fetch & render projects
  initContactForm();     // 9. Handle form submission
});


// ══════════════════════════════════════════════
// 1. NAVBAR — scroll effect & active link
// ══════════════════════════════════════════════
function initNavbar() {
  const navbar  = document.getElementById("navbar");
  const navLinks = document.querySelectorAll(".nav-link");

  // Add .scrolled class when user has scrolled down
  window.addEventListener("scroll", () => {
    navbar.classList.toggle("scrolled", window.scrollY > 50);
    updateActiveNavLink();
  });

  // Highlight the nav link whose section is currently in view
  function updateActiveNavLink() {
    const sections = document.querySelectorAll("section[id]");
    let currentId = "";

    sections.forEach(section => {
      const sectionTop = section.offsetTop - 100;
      if (window.scrollY >= sectionTop) {
        currentId = section.id;
      }
    });

    navLinks.forEach(link => {
      link.classList.toggle(
        "active",
        link.getAttribute("href") === `#${currentId}`
      );
    });
  }

  // Run once on page load
  updateActiveNavLink();
}


// ══════════════════════════════════════════════
// 2. MOBILE MENU TOGGLE
// ══════════════════════════════════════════════
function initMobileMenu() {
  const hamburger = document.getElementById("hamburger");
  const navLinks  = document.getElementById("navLinks");

  hamburger.addEventListener("click", () => {
    const isOpen = navLinks.classList.toggle("open");
    hamburger.classList.toggle("open", isOpen);
    hamburger.setAttribute("aria-expanded", isOpen);
  });

  // Close menu when a nav link is clicked
  navLinks.querySelectorAll("a").forEach(link => {
    link.addEventListener("click", () => {
      navLinks.classList.remove("open");
      hamburger.classList.remove("open");
    });
  });

  // Close menu when clicking outside
  document.addEventListener("click", (e) => {
    if (!hamburger.contains(e.target) && !navLinks.contains(e.target)) {
      navLinks.classList.remove("open");
      hamburger.classList.remove("open");
    }
  });
}


// ══════════════════════════════════════════════
// 3. DARK / LIGHT THEME TOGGLE
// ══════════════════════════════════════════════
function initTheme() {
  const btn  = document.getElementById("themeToggle");
  const icon = document.getElementById("themeIcon");
  const html = document.documentElement;

  // Load saved preference (default: dark)
  const saved = localStorage.getItem("portfolio-theme") || "dark";
  html.setAttribute("data-theme", saved);
  updateIcon(saved);

  btn.addEventListener("click", () => {
    const current = html.getAttribute("data-theme");
    const next    = current === "dark" ? "light" : "dark";

    html.setAttribute("data-theme", next);
    localStorage.setItem("portfolio-theme", next);
    updateIcon(next);
  });

  function updateIcon(theme) {
    icon.className = theme === "dark" ? "fas fa-moon" : "fas fa-sun";
  }
}


// ══════════════════════════════════════════════
// 4. SCROLL REVEAL ANIMATIONS
// ══════════════════════════════════════════════
function initScrollReveal() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          // Animate skill bars when they enter view
          animateSkillBarsInView(entry.target);
          observer.unobserve(entry.target); // only animate once
        }
      });
    },
    {
      threshold: 0.12,    // trigger when 12% of element is visible
      rootMargin: "0px 0px -50px 0px"
    }
  );

  // Observe all elements with .reveal class
  document.querySelectorAll(".reveal").forEach(el => observer.observe(el));
}

/** Animate skill progress bars when the skill card becomes visible */
function animateSkillBarsInView(element) {
  const bars = element.querySelectorAll(".skill-bar-fill[data-level]");
  bars.forEach(bar => {
    const level = bar.getAttribute("data-level");
    // Small delay so the card reveal animation finishes first
    setTimeout(() => {
      bar.style.width = level + "%";
    }, 200);
  });
}


// ══════════════════════════════════════════════
// 5. TYPING EFFECT IN HERO SECTION
// ══════════════════════════════════════════════
function initTypingEffect() {
  const el = document.getElementById("typingText");
  if (!el) return;

  const phrases = [
    "Full Stack Developer",
    "Python Enthusiast",
    "Flask & React Dev",
    "UI/UX Designer",
    "Open Source Lover",
  ];

  let phraseIndex = 0;
  let charIndex   = 0;
  let isDeleting  = false;
  let typingSpeed = 100;

  function type() {
    const current = phrases[phraseIndex];

    if (isDeleting) {
      // Remove one character
      el.textContent = current.substring(0, charIndex - 1);
      charIndex--;
      typingSpeed = 50;
    } else {
      // Add one character
      el.textContent = current.substring(0, charIndex + 1);
      charIndex++;
      typingSpeed = 100;
    }

    if (!isDeleting && charIndex === current.length) {
      // Pause before deleting
      typingSpeed = 2000;
      isDeleting  = true;
    } else if (isDeleting && charIndex === 0) {
      // Move to next phrase
      isDeleting  = false;
      phraseIndex = (phraseIndex + 1) % phrases.length;
      typingSpeed = 400;
    }

    setTimeout(type, typingSpeed);
  }

  type();
}


// ══════════════════════════════════════════════
// 6. LOAD SKILLS FROM FLASK API
// ══════════════════════════════════════════════
async function loadSkills() {
  const grid = document.getElementById("skillsGrid");
  if (!grid) return;

  try {
    const res    = await fetch(`${API_BASE}/api/skills`);
    const skills = await res.json();

    if (!skills.length) {
      grid.innerHTML = `<p class="skills-loading">No skills found in database.</p>`;
      return;
    }

    // Render all skill cards
    grid.innerHTML = skills.map(skill => createSkillCard(skill)).join("");

    // Re-attach scroll observer to new cards
    const observer = new IntersectionObserver(entries => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          entry.target.classList.add("visible");
          animateSkillBarsInView(entry.target);
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });

    grid.querySelectorAll(".skill-card").forEach(card => {
      card.classList.add("reveal");
      observer.observe(card);
    });

  } catch (err) {
    console.error("Failed to load skills:", err);
    grid.innerHTML = `
      <p class="skills-loading" style="color:var(--danger);">
        <i class="fas fa-exclamation-triangle"></i>
        Could not load skills. Make sure Flask is running.
      </p>`;
  }
}

/** Build HTML for one skill card */
function createSkillCard(skill) {
  return `
    <div class="skill-card">
      <div class="skill-card-top">
        <div class="skill-icon"><i class="${escapeHtml(skill.icon)}"></i></div>
        <div>
          <div class="skill-name">${escapeHtml(skill.name)}</div>
          <div class="skill-category">${escapeHtml(skill.category)}</div>
        </div>
      </div>
      <div class="skill-bar-wrap">
        <div class="skill-bar">
          <!-- data-level is read by animateSkillBarsInView() -->
          <div class="skill-bar-fill" data-level="${skill.level}" style="width:0%"></div>
        </div>
        <span class="skill-level">${skill.level}%</span>
      </div>
    </div>
  `;
}


// ══════════════════════════════════════════════
// 7 & 8. LOAD PROJECTS + FILTERING
// ══════════════════════════════════════════════

/** All fetched projects stored here so filtering doesn't need another request */
let allProjects = [];

async function loadProjects() {
  const grid = document.getElementById("projectsGrid");
  if (!grid) return;

  try {
    const res = await fetch(`${API_BASE}/api/projects`);
    allProjects = await res.json();

    if (!allProjects.length) {
      grid.innerHTML = `<p class="projects-loading">No projects found in database.</p>`;
      return;
    }

    renderProjects("all");
    initFilterButtons();

  } catch (err) {
    console.error("Failed to load projects:", err);
    grid.innerHTML = `
      <p class="projects-loading" style="color:var(--danger);">
        <i class="fas fa-exclamation-triangle"></i>
        Could not load projects. Make sure Flask is running.
      </p>`;
  }
}

/**
 * Renders project cards filtered by category.
 * @param {string} filter - "all" | "fullstack" | "frontend" | "backend"
 */
function renderProjects(filter) {
  const grid = document.getElementById("projectsGrid");
  const filtered = filter === "all"
    ? allProjects
    : allProjects.filter(p => p.category === filter);

  if (!filtered.length) {
    grid.innerHTML = `<p class="projects-loading">No ${filter} projects yet.</p>`;
    return;
  }

  grid.innerHTML = filtered.map(p => createProjectCard(p)).join("");

  // Animate new cards in with stagger
  const observer = new IntersectionObserver(entries => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add("visible");
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.08 });

  grid.querySelectorAll(".project-card").forEach((card, i) => {
    card.classList.add("reveal");
    card.style.transitionDelay = `${i * 0.08}s`;
    observer.observe(card);
  });
}

/** Build HTML for one project card */
function createProjectCard(project) {
  // Split tech string into individual tags
  const techTags = project.technologies
    ? project.technologies.split(",").map(t =>
        `<span class="project-tag">${escapeHtml(t.trim())}</span>`
      ).join("")
    : "";

  const featuredBadge = project.featured
    ? `<span class="featured-badge">⭐ Featured</span>`
    : "";

  const githubBtn = project.github_url && project.github_url !== "#"
    ? `<a href="${project.github_url}" target="_blank" rel="noopener" class="overlay-btn" title="GitHub">
         <i class="fab fa-github"></i>
       </a>`
    : "";

  const liveBtn = project.live_url && project.live_url !== "#"
    ? `<a href="${project.live_url}" target="_blank" rel="noopener" class="overlay-btn" title="Live Demo">
         <i class="fas fa-external-link-alt"></i>
       </a>`
    : "";

  return `
    <div class="project-card ${project.featured ? 'featured' : ''}"
         data-category="${escapeHtml(project.category)}">

      <div class="project-img">
        <img src="${escapeHtml(project.image)}"
             alt="${escapeHtml(project.title)}"
             loading="lazy"
             onerror="this.src='images/placeholder.jpg'"/>
        <div class="project-overlay">
          ${githubBtn}
          ${liveBtn}
        </div>
        ${featuredBadge}
      </div>

      <div class="project-body">
        <div class="project-tags">${techTags}</div>
        <h3 class="project-title">${escapeHtml(project.title)}</h3>
        <p class="project-desc">${escapeHtml(project.description)}</p>
        <div class="project-links">
          ${project.github_url && project.github_url !== "#"
            ? `<a href="${project.github_url}" target="_blank" class="project-link">
                 <i class="fab fa-github"></i> Source Code
               </a>`
            : ""}
          ${project.live_url && project.live_url !== "#"
            ? `<a href="${project.live_url}" target="_blank" class="project-link">
                 <i class="fas fa-external-link-alt"></i> Live Demo
               </a>`
            : ""}
        </div>
      </div>
    </div>
  `;
}

/** Wire up filter button click handlers */
function initFilterButtons() {
  const buttons = document.querySelectorAll(".filter-btn");

  buttons.forEach(btn => {
    btn.addEventListener("click", () => {
      // Update active button
      buttons.forEach(b => b.classList.remove("active"));
      btn.classList.add("active");

      // Re-render projects with selected filter
      const filter = btn.getAttribute("data-filter");
      renderProjects(filter);
    });
  });
}


// ══════════════════════════════════════════════
// 9. CONTACT FORM (AJAX)
// ══════════════════════════════════════════════
function initContactForm() {
  const form      = document.getElementById("contactForm");
  const statusDiv = document.getElementById("formStatus");
  const submitBtn = document.getElementById("submitBtn");

  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();

    // Grab form values
    const name    = document.getElementById("contactName").value.trim();
    const email   = document.getElementById("contactEmail").value.trim();
    const message = document.getElementById("contactMessage").value.trim();

    // Basic client-side validation
    if (!name || !email || !message) {
      showStatus("error", "Please fill in all fields.");
      return;
    }

    // Show loading state on button
    submitBtn.disabled = true;
    submitBtn.innerHTML = `<i class="fas fa-circle-notch fa-spin"></i> Sending...`;

    try {
      const res  = await fetch(`${API_BASE}/api/contact`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, message }),
      });
      const data = await res.json();

      if (data.success) {
        showStatus("success", `✅ ${data.message}`);
        form.reset();
      } else {
        showStatus("error", `❌ ${data.error || "Something went wrong."}`);
      }

    } catch (err) {
      console.error("Contact form error:", err);
      showStatus("error", "❌ Could not send message. Is Flask running?");
    } finally {
      // Restore button
      submitBtn.disabled = false;
      submitBtn.innerHTML = `<i class="fas fa-paper-plane"></i> Send Message`;
    }
  });

  /** Show a success or error message below the form */
  function showStatus(type, message) {
    statusDiv.className  = `form-status ${type}`;
    statusDiv.textContent = message;
    statusDiv.style.display = "flex";

    // Auto-hide after 6 seconds
    setTimeout(() => {
      statusDiv.style.display = "none";
    }, 6000);
  }
}


// ══════════════════════════════════════════════
// UTILITY: Escape HTML to prevent XSS
// ══════════════════════════════════════════════
function escapeHtml(str) {
  if (!str) return "";
  return String(str)
    .replace(/&/g,  "&amp;")
    .replace(/</g,  "&lt;")
    .replace(/>/g,  "&gt;")
    .replace(/"/g,  "&quot;")
    .replace(/'/g,  "&#039;");
}
