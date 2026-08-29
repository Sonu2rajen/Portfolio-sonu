// ──────────────────────────────────────────────
// SONU RAJENDRAN PORTFOLIO — INTERACTIVE ENGINE (V2.0 UPGRADE)
// ──────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {

  // State Management
  let currentCategory = "All";
  let visibleCount = 9;
  let cardSliderTimers = [];

  // DOM Elements
  const heroFloatCardsContainer = document.getElementById("hero-float-cards");
  const heroAchieveBar = document.getElementById("hero-achievements-bar");
  const timelineContainer = document.getElementById("timeline-container");
  const filterBar = document.getElementById("filter-bar");
  const projectsGrid = document.getElementById("projects-grid");
  const loadMoreBtn = document.getElementById("load-more-btn");
  const loadMoreWrapper = document.getElementById("load-more-wrapper");
  const eduGrid = document.getElementById("edu-grid");
  const certsGrid = document.getElementById("certs-grid");
  const menuToggle = document.getElementById("menu-toggle");
  const navLinks = document.querySelector(".nav-links");
  const caseStudyOverlay = document.getElementById("case-study-overlay");
  const caseStudyContent = document.getElementById("case-study-content");
  const lightboxModal = document.getElementById("lightbox-modal");
  const lightboxImg = document.getElementById("lightbox-img");
  const lightboxClose = document.getElementById("lightbox-close");

  // Helper to resolve fallback SVG icon per category
  function getFallbackCategoryIcon(category) {
    const map = {
      "AI & ML Models": "assets/thumbnails/python.svg",
      "Automation & Bots": "assets/thumbnails/automation.svg",
      "Advanced Data Engineering": "assets/thumbnails/cloud.svg",
      "Docker & SQL Pipelines": "assets/thumbnails/cloud.svg",
      "Excel Analytics": "assets/thumbnails/excel.svg",
      "Excel & Power Pivot": "assets/thumbnails/excel.svg",
      "Full-Stack Development": "assets/thumbnails/appdev.svg",
      "Power BI & Snowflake": "assets/thumbnails/powerbi.svg",
      "Power BI & SQL EDA": "assets/thumbnails/powerbi.svg",
      "Python EDA": "assets/thumbnails/python.svg",
      "Python Scraper Bots": "assets/thumbnails/python.svg",
      "SQL EDA & Data Handling": "assets/thumbnails/sql.svg",
      "SQL, T-SQL & MySQL": "assets/thumbnails/sql.svg",
      "Tableau Analytics": "assets/thumbnails/tableau.svg",
      "Website Development": "assets/thumbnails/appdev.svg"
    };
    return map[category] || "assets/thumbnails/powerbi.svg";
  }

  // 1. Render FIVE Floating Expertise Cards (Hero Section)
  function renderHeroFloatCards() {
    if (!heroFloatCardsContainer || typeof FLOATING_HERO_CARDS === "undefined") return;

    heroFloatCardsContainer.innerHTML = FLOATING_HERO_CARDS.map(card => `
      <div class="hero-float-card ${card.positionClass}">
        <div class="hero-float-title">${card.title}</div>
        <div class="hero-float-stack">${card.stack}</div>
      </div>
    `).join('');
  }

  // 2. Render Hero Achievements Bar
  function renderHeroAchievements() {
    if (!heroAchieveBar || typeof ACHIEVEMENTS === "undefined") return;

    heroAchieveBar.innerHTML = ACHIEVEMENTS.map(item => `
      <div class="hero-achieve-item">
        <div class="hero-achieve-val">${item.val}</div>
        <div class="hero-achieve-label">${item.label}</div>
      </div>
    `).join('');
  }

  // 3. Render Experience Timeline (With Complete Resume Bullets & Case Study Links)
  function renderTimeline() {
    if (!timelineContainer || typeof EXPERIENCE === "undefined") return;

    timelineContainer.innerHTML = EXPERIENCE.map(exp => `
      <div class="timeline-item reveal">
        <div class="timeline-card">
          <div class="timeline-header">
            <div>
              <h3 class="role-title">${exp.role}</h3>
              <div class="company-name">${exp.company} ${exp.location ? `• ${exp.location}` : ''}</div>
            </div>
            <span class="period-badge">${exp.period}</span>
          </div>
          <ul class="timeline-bullets">
            ${exp.highlights.map(h => `<li>${h}</li>`).join('')}
          </ul>
          ${exp.relatedProject ? `
            <div style="margin-top: 1.2rem;">
              <a href="#case-study-${exp.relatedProject}" class="card-link">
                View Related Case Study →
              </a>
            </div>
          ` : ''}
        </div>
      </div>
    `).join('');
  }

  // 4. Render Dynamic Filter Tabs with Dynamic Counts (STEP 6)
  function renderFilterTabs() {
    if (!filterBar || typeof CATEGORIES === "undefined" || typeof PROJECTS === "undefined") return;

    // Calculate dynamic counts
    const categoryCounts = {};
    categoryCounts["All"] = PROJECTS.length;

    PROJECTS.forEach(p => {
      categoryCounts[p.category] = (categoryCounts[p.category] || 0) + 1;
    });

    filterBar.innerHTML = CATEGORIES.map(cat => {
      const count = categoryCounts[cat] || 0;
      return `
        <button class="filter-tab ${cat === currentCategory ? 'active' : ''}" data-category="${cat}">
          ${cat} (${count})
        </button>
      `;
    }).join('');

    filterBar.querySelectorAll('.filter-tab').forEach(btn => {
      btn.addEventListener('click', () => {
        filterBar.querySelectorAll('.filter-tab').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        currentCategory = btn.getAttribute('data-category');
        visibleCount = 9;
        renderProjects();
      });
    });
  }

  // Clear background timers for card image sliders
  function clearCardSliderTimers() {
    cardSliderTimers.forEach(t => clearInterval(t));
    cardSliderTimers = [];
  }

  // 5. Render Projects Grid (With Card Preview Slider)
  function renderProjects() {
    if (!projectsGrid || typeof PROJECTS === "undefined") return;

    clearCardSliderTimers();

    // Render category description if available
    const categoryDescEl = document.getElementById("category-description");
    if (categoryDescEl) {
      if (typeof CATEGORY_DESCRIPTIONS !== "undefined" && CATEGORY_DESCRIPTIONS[currentCategory]) {
        categoryDescEl.textContent = CATEGORY_DESCRIPTIONS[currentCategory];
        categoryDescEl.style.display = "block";
      } else {
        categoryDescEl.style.display = "none";
      }
    }

    const filtered = currentCategory === "All" 
      ? PROJECTS 
      : PROJECTS.filter(p => p.category === currentCategory);

    const visibleProjects = filtered.slice(0, visibleCount);

    if (visibleProjects.length === 0) {
      projectsGrid.innerHTML = `
        <div style="grid-column: 1/-1; text-align: center; padding: 3rem; color: var(--text-secondary);">
          No projects found in this category.
        </div>
      `;
      loadMoreWrapper.style.display = "none";
      return;
    }

    projectsGrid.innerHTML = visibleProjects.map((proj, idx) => {
      const slides = (proj.images && proj.images.length > 0) ? proj.images : [proj.thumbnail || getFallbackCategoryIcon(proj.category)];
      const cardId = `project-card-${idx}`;

      return `
        <div class="project-card reveal" id="${cardId}" onclick="openCaseStudy('${proj.id}')">
          <div class="card-thumb-wrapper">
            <span class="tier-badge ${proj.tier.toLowerCase()}">${proj.tier}</span>
            <div class="card-slides-container" id="slides-${cardId}">
              ${slides.map((imgSrc, slideIdx) => `
                <div class="card-slide ${slideIdx === 0 ? 'active' : ''}">
                  <img src="${imgSrc}" alt="${proj.title} Preview ${slideIdx + 1}" loading="lazy" onerror="this.onerror=null; this.src='${getFallbackCategoryIcon(proj.category)}';">
                </div>
              `).join('')}
            </div>
            ${slides.length > 1 ? `
              <div class="card-slider-dots" id="dots-${cardId}">
                ${slides.map((_, dotIdx) => `
                  <span class="card-dot ${dotIdx === 0 ? 'active' : ''}"></span>
                `).join('')}
              </div>
            ` : ''}
          </div>
          <div class="card-body">
            <h3 class="card-title">${proj.title}</h3>
            <div class="card-outcome">${proj.outcome}</div>
            <p class="card-desc">${proj.description}</p>
            <div class="card-footer">
              <div class="card-tools">
                ${proj.tools.map(tool => `<span class="card-tool-tag">${tool}</span>`).join('')}
              </div>
              <span class="card-link">
                Case Study →
              </span>
            </div>
          </div>
        </div>
      `;
    }).join('');

    // Initialize Card Preview Auto-Slider
    visibleProjects.forEach((proj, idx) => {
      const slides = (proj.images && proj.images.length > 0) ? proj.images : [proj.thumbnail || getFallbackCategoryIcon(proj.category)];
      if (slides.length <= 1) return;

      const cardId = `project-card-${idx}`;
      const cardElement = document.getElementById(cardId);
      const slideElements = document.querySelectorAll(`#slides-${cardId} .card-slide`);
      const dotElements = document.querySelectorAll(`#dots-${cardId} .card-dot`);

      if (!slideElements.length) return;

      let currentSlide = 0;

      function goToSlide(nextIdx) {
        if (!slideElements[currentSlide]) return;
        slideElements[currentSlide].classList.remove('active');
        if (dotElements[currentSlide]) dotElements[currentSlide].classList.remove('active');

        currentSlide = nextIdx % slides.length;

        if (slideElements[currentSlide]) slideElements[currentSlide].classList.add('active');
        if (dotElements[currentSlide]) dotElements[currentSlide].classList.add('active');
      }

      let timer = setInterval(() => {
        goToSlide(currentSlide + 1);
      }, 3500);

      cardSliderTimers.push(timer);

      if (cardElement) {
        cardElement.addEventListener('mouseenter', () => clearInterval(timer));
        cardElement.addEventListener('mouseleave', () => {
          clearInterval(timer);
          timer = setInterval(() => goToSlide(currentSlide + 1), 3500);
          cardSliderTimers.push(timer);
        });
      }
    });

    if (visibleCount >= filtered.length) {
      loadMoreWrapper.style.display = "none";
    } else {
      loadMoreWrapper.style.display = "block";
    }

    initScrollReveal();
  }

  // Load More Button Event Listener
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', () => {
      visibleCount += 9;
      renderProjects();
    });
  }

  // 6. Render Dedicated Case Study Page Overlay
  window.openCaseStudy = function(projId) {
    window.location.hash = `case-study-${projId}`;
  };

  window.closeCaseStudy = function() {
    window.location.hash = "projects";
  };

  function handleHashRouting() {
    const hash = window.location.hash;
    if (hash.startsWith("#case-study-")) {
      const projId = hash.replace("#case-study-", "");
      const project = PROJECTS.find(p => p.id === projId);

      if (project) {
        renderCaseStudyView(project);
        caseStudyOverlay.classList.add("active");
        document.body.style.overflow = "hidden";
      }
    } else {
      caseStudyOverlay.classList.remove("active");
      document.body.style.overflow = "auto";
    }
  }

  window.addEventListener("hashchange", handleHashRouting);

  function renderCaseStudyView(proj) {
    if (!caseStudyContent) return;

    const mediaItems = [];

    if (proj.video) {
      mediaItems.push({ type: 'video', src: proj.video, label: 'Project Video Walkthrough' });
    }

    if (proj.images && proj.images.length > 0) {
      proj.images.forEach((imgSrc, i) => {
        mediaItems.push({ type: 'image', src: imgSrc, label: `Project Screenshot ${i + 1}` });
      });
    }

    if (mediaItems.length === 0) {
      mediaItems.push({ type: 'image', src: proj.thumbnail, label: 'Category Visual' });
    }

    // Prepare docx sections HTML
    let docxHtml = "";
    if (proj.docxSections && proj.docxSections.length > 0) {
      docxHtml = proj.docxSections.map(sec => `
        <div class="cs-section">
          <h2 class="cs-section-title">${sec.heading}</h2>
          <div class="cs-text">
            ${sec.content.map(p => {
              if (p.startsWith('•') || p.startsWith('✔') || p.startsWith('-')) {
                return `<li class="cs-bullet-item">${p.replace(/^[•✔-]\s*/, '')}</li>`;
              }
              return `<p class="cs-paragraph">${p}</p>`;
            }).join('')}
          </div>
        </div>
      `).join('');
    } else {
      // Fallback if legacy object keys
      if (proj.objective) docxHtml += `<div class="cs-section"><h2 class="cs-section-title">OBJECTIVE</h2><div class="cs-text">${proj.objective}</div></div>`;
      if (proj.problem) docxHtml += `<div class="cs-section"><h2 class="cs-section-title">PROBLEM</h2><div class="cs-text">${proj.problem}</div></div>`;
      if (proj.solution) docxHtml += `<div class="cs-section"><h2 class="cs-section-title">SOLUTION</h2><div class="cs-text">${proj.solution}</div></div>`;
      if (proj.result) docxHtml += `<div class="cs-section"><h2 class="cs-section-title">RESULT</h2><div class="cs-text">${proj.result}</div></div>`;
    }

    // Prepare code snippet HTML
    let codeHtml = "";
    if (proj.codeSnippet && proj.codeSnippet.code) {
      codeHtml = `
        <div class="cs-section">
          <h2 class="cs-section-title">SOURCE CODE PREVIEW (${proj.codeSnippet.language.toUpperCase()})</h2>
          <div class="code-editor-box">
            <div class="code-editor-header">
              <div class="code-editor-dots">
                <span class="code-dot-red"></span>
                <span class="code-dot-yellow"></span>
                <span class="code-dot-green"></span>
              </div>
              <span class="code-editor-title">📄 ${proj.codeSnippet.filename}</span>
              <button class="code-copy-btn" onclick="copyCodeSnippet(this)">Copy Code</button>
            </div>
            <pre class="code-editor-body"><code>${escapeHtml(proj.codeSnippet.code)}</code></pre>
          </div>
        </div>
      `;
    }

    // Prepare SQL file viewer HTML (for SQL, T-SQL & MySQL category)
    let sqlViewerHtml = "";
    if (proj.allSqlFiles && proj.allSqlFiles.length > 0) {
      sqlViewerHtml = `
        <div class="cs-section">
          <h2 class="cs-section-title">SQL SCRIPTS LIBRARY (${proj.allSqlFiles.length} FILES)</h2>
          <div class="sql-files-nav">
            ${proj.allSqlFiles.map((sf, i) => `
              <button class="sql-file-tab ${i === 0 ? 'active' : ''}" data-sql-idx="${i}">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                ${sf.filename}
              </button>
            `).join('')}
          </div>
          <div class="sql-files-viewer">
            ${proj.allSqlFiles.map((sf, i) => `
              <div class="sql-file-panel ${i === 0 ? 'active' : ''}" data-sql-panel="${i}">
                <div class="code-editor-box">
                  <div class="code-editor-header">
                    <div class="code-editor-dots">
                      <span class="code-dot-red"></span>
                      <span class="code-dot-yellow"></span>
                      <span class="code-dot-green"></span>
                    </div>
                    <span class="code-editor-title">📄 ${sf.filename}</span>
                    <button class="code-copy-btn" onclick="copyCodeSnippet(this)">Copy Code</button>
                  </div>
                  <pre class="code-editor-body"><code>${escapeHtml(sf.code)}</code></pre>
                </div>
              </div>
            `).join('')}
          </div>
        </div>
      `;
    }

    caseStudyContent.innerHTML = `
      <div class="cs-action-bar">
        <button class="cs-back-btn" onclick="closeCaseStudy()">
          ← ALL WORK
        </button>
        <div class="cs-links-group">
          ${proj.githubUrl ? `
            <a href="${proj.githubUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-outline cs-action-link">
              <svg class="btn-icon" viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
              </svg>
              GitHub Repository
            </a>
          ` : ''}
          ${proj.researchPaperUrl ? `
            <a href="${proj.researchPaperUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-primary cs-action-link">
              📄 Research Paper
            </a>
          ` : ''}
        </div>
      </div>

      <div class="cs-category-tier">${proj.category} • ${proj.tier}</div>
      <h1 class="cs-title">${proj.title}</h1>
      <p class="cs-summary">${proj.description}</p>

      <div class="cs-tech-stack">
        ${proj.tools.map(tool => `<span class="cs-tech-pill">${tool}</span>`).join('')}
      </div>

      <div class="cs-media-showcase">
        <div class="cs-media-stage" id="cs-media-stage">
          ${mediaItems.map((item, i) => {
            if (item.type === 'video') {
              return `
                <div class="cs-media-item ${i === 0 ? 'active' : ''}" data-idx="${i}">
                  <video controls class="cs-video-player" poster="${proj.thumbnail}">
                    <source src="${item.src}" type="video/mp4">
                    Your browser does not support the video tag.
                  </video>
                </div>
              `;
            } else {
              return `
                <img src="${item.src}" alt="${item.label}" class="cs-media-item ${i === 0 ? 'active' : ''}" data-idx="${i}" onclick="openLightbox('${item.src}')" style="cursor: zoom-in;" onerror="this.onerror=null; this.src='${getFallbackCategoryIcon(proj.category)}';">
              `;
            }
          }).join('')}

          ${mediaItems.length > 1 ? `
            <div class="cs-carousel-nav">
              <button class="cs-nav-btn" onclick="prevCsMedia()">&lt;</button>
              <button class="cs-nav-btn" onclick="nextCsMedia()">&gt;</button>
            </div>
          ` : ''}
        </div>

        <div class="cs-carousel-footer">
          <div id="cs-media-caption">${mediaItems[0].label}</div>
          ${mediaItems.length > 1 ? `
            <div class="cs-thumb-strip">
              ${mediaItems.map((_, i) => `
                <span class="cs-thumb-dot ${i === 0 ? 'active' : ''}" onclick="setCsMedia(${i})"></span>
              `).join('')}
            </div>
          ` : ''}
        </div>
      </div>

      <!-- ANIMATED QUICK ACTIONS BOX BELOW PROJECT MEDIA -->
      <div class="cs-quick-actions-bar">
        <div class="cs-action-box-card">
          <div class="cs-action-box-info">
            <span class="cs-action-box-badge">PROJECT REPOSITORY &amp; RESOURCES</span>
            <h4 class="cs-action-box-title">Explore Project Source &amp; Documentation</h4>
          </div>
          <div class="cs-action-box-buttons">
            ${proj.githubUrl ? `
              <a href="${proj.githubUrl}" target="_blank" rel="noopener noreferrer" class="cs-box-btn cs-btn-github">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/>
                </svg>
                GitHub Repository
              </a>
            ` : ''}
            <a href="${proj.docxFilePath || proj.researchPaperUrl || '#cs-content-grid'}" ${proj.docxFilePath ? 'download' : (proj.researchPaperUrl ? 'target="_blank" rel="noopener noreferrer"' : 'onclick="document.querySelector(\'.cs-content-grid\')?.scrollIntoView({behavior: \'smooth\'}); return false;"')} class="cs-box-btn cs-btn-casestudy">
              📥 Download Case Study Specs
            </a>
            ${proj.codeSnippet ? `
              <a href="#cs-code" class="cs-box-btn cs-btn-code" onclick="document.querySelector('.code-editor-box')?.scrollIntoView({behavior: 'smooth'})">
                ⚡ Interactive Code Viewer
              </a>
            ` : ''}
          </div>
        </div>
      </div>

      <div class="cs-content-grid">
        ${docxHtml}
        ${codeHtml}
        ${sqlViewerHtml}
      </div>

      <!-- Existing Portfolio Footer Component -->
      <footer class="contact-section cs-footer" style="margin-top: 5rem; border-radius: var(--radius-lg);">
        <div class="container">
          <div class="footer-grid">
            <div class="footer-col">
              <h3 class="footer-brand">SONU RAJENDRAN</h3>
              <p class="footer-tagline">Data &amp; Technology Professional</p>
              <p class="footer-bio-short">Specializing in Power BI, SQL, Python ETL, Star Schema Modeling, Process Automation, and Full-Stack Data Applications.</p>
            </div>
            <div class="footer-col">
              <h4 class="footer-col-title">NAVIGATION</h4>
              <ul class="footer-links">
                <li><a href="#hero" onclick="closeCaseStudy()">Home</a></li>
                <li><a href="#projects" onclick="closeCaseStudy()">Projects</a></li>
                <li><a href="#contact" onclick="closeCaseStudy()">Contact</a></li>
              </ul>
            </div>
            <div class="footer-col">
              <h4 class="footer-col-title">CONTACT &amp; PROFILES</h4>
              <ul class="footer-links">
                <li><a href="mailto:sonurajendran2@gmail.com">📧 sonurajendran2@gmail.com</a></li>
                <li><a href="https://wa.me/919136800446" target="_blank" rel="noopener noreferrer">💬 +91 9136800446</a></li>
                <li><a href="https://linkedin.com/in/sonu-rajendran" target="_blank" rel="noopener noreferrer">💼 LinkedIn Profile</a></li>
                <li><a href="https://github.com/Sonu2rajen" target="_blank" rel="noopener noreferrer">🐙 GitHub Repositories</a></li>
              </ul>
            </div>
          </div>
          <div class="footer-bottom">
            <div>© 2026 Sonu Rajendran. All rights reserved.</div>
            <div>Built with HTML5, CSS3 &amp; Vanilla JavaScript</div>
          </div>
        </div>
      </footer>
    `;

    let csCurrentIdx = 0;

    window.setCsMedia = function(idx) {
      const items = document.querySelectorAll('#cs-media-stage .cs-media-item');
      const dots = document.querySelectorAll('.cs-thumb-dot');
      const caption = document.getElementById('cs-media-caption');

      if (!items.length) return;

      items.forEach(el => {
        if (el.tagName === 'DIV' && el.querySelector('video')) {
          el.querySelector('video').pause();
        }
        el.classList.remove('active');
      });

      dots.forEach(d => d.classList.remove('active'));

      csCurrentIdx = (idx + items.length) % items.length;

      items[csCurrentIdx].classList.add('active');
      if (dots[csCurrentIdx]) dots[csCurrentIdx].classList.add('active');
      if (caption && mediaItems[csCurrentIdx]) caption.innerText = mediaItems[csCurrentIdx].label;
    };

    window.nextCsMedia = function() {
      setCsMedia(csCurrentIdx + 1);
    };

    window.prevCsMedia = function() {
      setCsMedia(csCurrentIdx - 1);
    };

    // SQL file tab switching
    const sqlFileTabs = document.querySelectorAll('.sql-file-tab');
    if (sqlFileTabs.length > 0) {
      sqlFileTabs.forEach(tab => {
        tab.addEventListener('click', () => {
          const idx = tab.getAttribute('data-sql-idx');
          sqlFileTabs.forEach(t => t.classList.remove('active'));
          tab.classList.add('active');
          document.querySelectorAll('.sql-file-panel').forEach(p => p.classList.remove('active'));
          const panel = document.querySelector(`.sql-file-panel[data-sql-panel="${idx}"]`);
          if (panel) panel.classList.add('active');
        });
      });
    }
  }

  // Lightbox Modal for Screenshots
  window.openLightbox = function(src) {
    if (lightboxModal && lightboxImg) {
      lightboxImg.src = src;
      lightboxModal.classList.add("active");
    }
  };

  if (lightboxClose) {
    lightboxClose.addEventListener("click", () => {
      lightboxModal.classList.remove("active");
    });
  }

  if (lightboxModal) {
    lightboxModal.addEventListener("click", (e) => {
      if (e.target === lightboxModal) {
        lightboxModal.classList.remove("active");
      }
    });
  }

  // 7. Render Credentials: Education & Certifications (STEP 7)
  function renderEducationAndCerts() {
    // Render Education Grid
    if (eduGrid && typeof EDUCATION !== "undefined") {
      eduGrid.innerHTML = EDUCATION.map(edu => `
        <div class="formal-edu-card reveal active">
          <h4 class="edu-title">${edu.degree}</h4>
          <div class="edu-institution-link">${edu.institution}</div>
          <div class="edu-meta-line">${edu.period} &nbsp;|&nbsp; CGPA: ${edu.grade.replace('CGPA ', '')}</div>
          <p class="edu-desc-text">${edu.details}</p>
        </div>
      `).join('');
    }

    // Render Certifications Grid
    if (certsGrid && typeof CERTIFICATIONS !== "undefined") {
      certsGrid.innerHTML = CERTIFICATIONS.map(cert => `
        <div class="cert-bar-card reveal active">
          <div class="cert-bar-title">${cert.name}</div>
          <span class="cert-issuer-badge ${cert.status.includes('Progress') ? 'status-in-progress' : ''}">${cert.issuer}${cert.status.includes('Progress') ? ' (In Progress)' : ''}</span>
        </div>
      `).join('');
    }

    initScrollReveal();
  }

  // 8. Mobile Menu Toggle
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }

  // 9. Scroll Reveal Observer & Fallback
  function initScrollReveal() {
    const reveals = document.querySelectorAll('.reveal');
    
    if ('IntersectionObserver' in window) {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('active');
          }
        });
      }, { threshold: 0.05 });

      reveals.forEach(el => observer.observe(el));
    } else {
      reveals.forEach(el => el.classList.add('active'));
    }
  }

  // 10. Active Nav Link on Scroll
  function initActiveNav() {
    const sections = document.querySelectorAll('section, footer');
    const navItems = document.querySelectorAll('.nav-link');

    window.addEventListener('scroll', () => {
      let current = '';
      sections.forEach(section => {
        const sectionTop = section.offsetTop - 120;
        if (pageYOffset >= sectionTop) {
          current = section.getAttribute('id');
        }
      });

      navItems.forEach(item => {
        item.classList.remove('active');
        if (item.getAttribute('href') === `#${current}`) {
          item.classList.add('active');
        }
      });
    });
  }

  // Helper: Escape HTML
  function escapeHtml(text) {
    if (!text) return '';
    return text
      .replace(/&/g, "&amp;")
      .replace(/</g, "&lt;")
      .replace(/>/g, "&gt;")
      .replace(/"/g, "&quot;")
      .replace(/'/g, "&#039;");
  }

  // Helper: Copy Code Snippet to Clipboard
  window.copyCodeSnippet = function(btn) {
    const box = btn.closest('.code-editor-box');
    if (!box) return;
    const codeEl = box.querySelector('code');
    if (!codeEl) return;
    
    navigator.clipboard.writeText(codeEl.innerText).then(() => {
      const originalText = btn.innerText;
      btn.innerText = 'Copied! ✓';
      btn.style.background = '#10B981';
      btn.style.color = '#FFFFFF';
      setTimeout(() => {
        btn.innerText = originalText;
        btn.style.background = '';
        btn.style.color = '';
      }, 2000);
    }).catch(err => {
      console.error('Failed to copy code snippet: ', err);
    });
  };

  // Initial Execution
  renderHeroFloatCards();
  renderHeroAchievements();
  renderTimeline();
  renderFilterTabs();
  renderProjects();
  renderEducationAndCerts();
  initScrollReveal();
  initActiveNav();
  handleHashRouting();
});
