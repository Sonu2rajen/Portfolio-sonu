// ──────────────────────────────────────────────
// SONU RAJENDRAN PORTFOLIO — INTERACTIVE ENGINE
// Features:
// 1. Hero Highlights Bar
// 2. Card Preview Animated Image Slider
// 3. Dedicated Case Study Page / Hash Routing
// 4. Video-First Media Carousel with Lightbox
// 5. Contact Mailto & WhatsApp integration
// ──────────────────────────────────────────────

document.addEventListener("DOMContentLoaded", () => {

  // State Management
  let currentCategory = "All";
  let visibleCount = 9;
  let cardSliderTimers = [];

  // DOM Elements
  const heroAchieveBar = document.getElementById("hero-achievements-bar");
  const timelineContainer = document.getElementById("timeline-container");
  const filterBar = document.getElementById("filter-bar");
  const projectsGrid = document.getElementById("projects-grid");
  const loadMoreBtn = document.getElementById("load-more-btn");
  const loadMoreWrapper = document.getElementById("load-more-wrapper");
  const certsGrid = document.getElementById("certs-grid");
  const menuToggle = document.getElementById("menu-toggle");
  const navLinks = document.querySelector(".nav-links");
  const caseStudyOverlay = document.getElementById("case-study-overlay");
  const caseStudyContent = document.getElementById("case-study-content");
  const lightboxModal = document.getElementById("lightbox-modal");
  const lightboxImg = document.getElementById("lightbox-img");
  const lightboxClose = document.getElementById("lightbox-close");

  // 1. Render Hero Achievements Bar
  function renderHeroAchievements() {
    if (!heroAchieveBar || typeof ACHIEVEMENTS === "undefined") return;

    heroAchieveBar.innerHTML = ACHIEVEMENTS.map(item => `
      <div class="hero-achieve-item">
        <div class="hero-achieve-val">${item.val}</div>
        <div class="hero-achieve-label">${item.label}</div>
      </div>
    `).join('');
  }

  // 2. Render Timeline Experience
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
            <div style="margin-top: 1rem;">
              <a href="#case-study-${exp.relatedProject}" class="card-link">
                View Related Case Study →
              </a>
            </div>
          ` : ''}
        </div>
      </div>
    `).join('');
  }

  // 3. Render Filter Tabs
  function renderFilterTabs() {
    if (!filterBar || typeof CATEGORIES === "undefined") return;

    filterBar.innerHTML = CATEGORIES.map(cat => `
      <button class="filter-tab ${cat === currentCategory ? 'active' : ''}" data-category="${cat}">
        ${cat}
      </button>
    `).join('');

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

  // Clear all background timers for card image sliders
  function clearCardSliderTimers() {
    cardSliderTimers.forEach(t => clearInterval(t));
    cardSliderTimers = [];
  }

  // 4. Render Projects Grid (With Animated Preview Slider inside cards)
  function renderProjects() {
    if (!projectsGrid || typeof PROJECTS === "undefined") return;

    clearCardSliderTimers();

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
      // Slides array for card preview: Slide 1 = Category SVG, Slide 2+ = Actual screenshots
      const slides = [proj.thumbnail, ...(proj.images || [])];
      const cardId = `project-card-${idx}`;

      return `
        <div class="project-card reveal" id="${cardId}" onclick="openCaseStudy('${proj.id}')">
          <div class="card-thumb-wrapper">
            <span class="tier-badge ${proj.tier.toLowerCase()}">${proj.tier}</span>
            <div class="card-slides-container" id="slides-${cardId}">
              ${slides.map((imgSrc, slideIdx) => `
                <div class="card-slide ${slideIdx === 0 ? 'active' : ''}">
                  <img src="${imgSrc}" alt="${proj.title} Preview ${slideIdx + 1}" loading="lazy">
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

    // Initialize Card Preview Auto-Slider for cards with multiple images
    visibleProjects.forEach((proj, idx) => {
      const slides = [proj.thumbnail, ...(proj.images || [])];
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

  // 5. Render Dedicated Project Case Study Page
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

    // Media items array: Video is FIRST slide if present, followed by project images
    const mediaItems = [];

    if (proj.video) {
      mediaItems.push({ type: 'video', src: proj.video, label: 'Project Video Walkthrough' });
    }

    if (proj.images && proj.images.length > 0) {
      proj.images.forEach((imgSrc, i) => {
        mediaItems.push({ type: 'image', src: imgSrc, label: `Dashboard Screenshot ${i + 1}` });
      });
    }

    // Fallback if no media exists
    if (mediaItems.length === 0) {
      mediaItems.push({ type: 'image', src: proj.thumbnail, label: 'Category Visual' });
    }

    caseStudyContent.innerHTML = `
      <!-- Back Navigation -->
      <div class="cs-back-btn" onclick="closeCaseStudy()">
        ← ALL WORK
      </div>

      <!-- Header Section -->
      <div class="cs-category-tier">${proj.category} • ${proj.tier}</div>
      <h1 class="cs-title">${proj.title}</h1>
      <p class="cs-summary">${proj.description}</p>

      <div class="cs-tech-stack">
        ${proj.tools.map(tool => `<span class="cs-tech-pill">${tool}</span>`).join('')}
      </div>

      <!-- Media Showcase (Video First, then Images) -->
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
                <img src="${item.src}" alt="${item.label}" class="cs-media-item ${i === 0 ? 'active' : ''}" data-idx="${i}" onclick="openLightbox('${item.src}')" style="cursor: zoom-in;">
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

      <!-- Detailed Case Study Content Grid -->
      <div class="cs-content-grid">
        
        ${proj.objective ? `
          <div class="cs-section">
            <h2 class="cs-section-title">OBJECTIVE</h2>
            <div class="cs-text">${proj.objective}</div>
          </div>
        ` : ''}

        ${proj.requirements ? `
          <div class="cs-section">
            <h2 class="cs-section-title">REQUIREMENTS</h2>
            <div class="cs-text">${proj.requirements}</div>
          </div>
        ` : ''}

        ${proj.purpose ? `
          <div class="cs-section">
            <h2 class="cs-section-title">PURPOSE</h2>
            <div class="cs-text">${proj.purpose}</div>
          </div>
        ` : ''}

        ${proj.problem ? `
          <div class="cs-section">
            <h2 class="cs-section-title">PROBLEM</h2>
            <div class="cs-text">${proj.problem}</div>
          </div>
        ` : ''}

        ${proj.approach ? `
          <div class="cs-section">
            <h2 class="cs-section-title">APPROACH</h2>
            <div class="cs-text">${proj.approach}</div>
          </div>
        ` : ''}

        ${proj.solution ? `
          <div class="cs-section">
            <h2 class="cs-section-title">SOLUTION</h2>
            <div class="cs-text">${proj.solution}</div>
          </div>
        ` : ''}

        ${proj.result ? `
          <div class="cs-section">
            <h2 class="cs-section-title">RESULT</h2>
            <div class="cs-text" style="color: var(--brand-primary); font-weight: 700; font-size: 1.15rem;">${proj.result}</div>
          </div>
        ` : ''}

        ${proj.technicalDetails && proj.technicalDetails.length > 0 ? `
          <div class="cs-section">
            <h2 class="cs-section-title">TECHNICAL IMPLEMENTATION</h2>
            <ul class="cs-bullets">
              ${proj.technicalDetails.map(item => `<li>${item}</li>`).join('')}
            </ul>
          </div>
        ` : ''}

        <!-- GitHub & Research Study Resources -->
        <div class="cs-section">
          <h2 class="cs-section-title">RESOURCES &amp; ARTIFACTS</h2>
          <div class="cs-resources-grid">
            
            <!-- GitHub Box -->
            <div class="cs-resource-card">
              <div class="cs-resource-title">🐙 GitHub Repository</div>
              <div class="cs-resource-desc">
                ${proj.githubUrl ? 'View source code and SQL scripts on GitHub.' : 'Enterprise production repository. Access available upon request.'}
              </div>
              ${proj.githubUrl ? `
                <a href="${proj.githubUrl}" target="_blank" rel="noopener noreferrer" class="btn btn-outline" style="font-size: 0.8rem; padding: 0.6rem 1rem; align-self: flex-start;">
                  VIEW ON GITHUB →
                </a>
              ` : `
                <span style="font-size: 0.8rem; font-weight: 700; color: var(--text-muted);">Repository Private</span>
              `}
            </div>

            <!-- Technical Study PDF Box Placeholder -->
            <div class="cs-resource-card">
              <div class="cs-resource-title">📄 Technical Study / Research Paper</div>
              <div class="cs-resource-desc">
                ${proj.researchPdf ? 'Download complete technical study PDF.' : 'Technical research paper architecture ready. Paper document pending publication.'}
              </div>
              ${proj.researchPdf ? `
                <a href="${proj.researchPdf}" target="_blank" download class="btn btn-primary" style="font-size: 0.8rem; padding: 0.6rem 1rem; align-self: flex-start;">
                  DOWNLOAD PDF ↓
                </a>
              ` : `
                <span style="font-size: 0.8rem; font-weight: 700; color: var(--brand-primary);">Paper Structure Configured</span>
              `}
            </div>

          </div>
        </div>

      </div>
    `;

    // Case Study Media Carousel Navigation Setup
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

  // 6. Render Certifications & Education
  function renderCertifications() {
    if (!certsGrid || typeof CERTIFICATIONS === "undefined") return;

    certsGrid.innerHTML = CERTIFICATIONS.map(cert => `
      <div class="cert-card reveal">
        <div class="cert-icon">${cert.icon}</div>
        <div>
          <h4 class="cert-name">${cert.name}</h4>
          <div class="cert-issuer">${cert.issuer} • <span style="color: var(--brand-primary); font-weight: 700;">${cert.status}</span></div>
        </div>
      </div>
    `).join('');
  }

  // 7. Mobile Menu Toggle
  if (menuToggle && navLinks) {
    menuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }

  // 8. Scroll Reveal Observer & Fallback
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

  // 9. Active Nav Link on Scroll
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

  // Initial Execution
  renderHeroAchievements();
  renderTimeline();
  renderFilterTabs();
  renderProjects();
  renderCertifications();
  initActiveNav();
  handleHashRouting();
});
