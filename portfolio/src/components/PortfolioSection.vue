<template>
  <section id="portfolio" class="section portfolio-section">
    <div class="container">
      <div class="section-title reveal">
        <span class="script">My Work</span>
        <h2>Portfolio</h2>
        <div class="divider"></div>
      </div>
      <div class="portfolio-grid">
        <a
          v-for="(project, i) in projects"
          :key="i"
          :href="project.project_url || '#'"
          :target="project.project_url ? '_blank' : '_self'"
          class="portfolio-card reveal"
          :class="'reveal-delay-' + Math.min((i % 3)+1, 3)"
        >
          <div class="portfolio-thumb">
            <img v-if="project.image" :src="'http://localhost:8000/media/' + project.image" :alt="project.title" />
            <div v-else class="thumb-placeholder">
              <span>{{ project.title.charAt(0) }}</span>
            </div>
            <div class="portfolio-overlay">
              <span class="view-label">View Project →</span>
            </div>
          </div>
          <div class="portfolio-info">
            <h3>{{ project.title }}</h3>
            <p>{{ project.description }}</p>
            <div v-if="project.technologies?.length" class="tech-tags">
              <span v-for="(tech, j) in project.technologies" :key="j" class="tech-tag">{{ tech }}</span>
            </div>
          </div>
        </a>

        <div v-if="!projects.length" class="empty-state">
          No portfolio projects yet.
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'PortfolioSection',
  props: ['profile'],
  computed: {
    projects() {
      return this.profile?.projects || []
    }
  }
}
</script>

<style scoped>
.portfolio-section {
  background: var(--color-dark-2);
}

.portfolio-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 1.5rem;
}

.portfolio-card {
  background: var(--color-dark-3);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  display: block;
  text-decoration: none;
  color: inherit;
}

.portfolio-card:hover {
  border-color: rgba(226,185,111,0.25);
  transform: translateY(-5px);
  box-shadow: 0 15px 40px rgba(0,0,0,0.4);
}

.portfolio-thumb {
  position: relative;
  height: 200px;
  overflow: hidden;
}

.portfolio-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s ease;
}

.portfolio-card:hover .portfolio-thumb img {
  transform: scale(1.05);
}

.thumb-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a1a2e, #0f3460);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 4rem;
  font-family: 'Playlist-Script', cursive;
  color: var(--color-gold);
  opacity: 0.7;
}

.portfolio-overlay {
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(13,13,13,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: opacity 0.3s;
}

.portfolio-card:hover .portfolio-overlay {
  opacity: 1;
}

.view-label {
  color: var(--color-gold);
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 1px;
  text-transform: uppercase;
}

.portfolio-info {
  padding: 1.5rem;
}

.portfolio-info h3 {
  font-size: 1rem;
  font-weight: 700;
  color: var(--color-white);
  margin-bottom: 0.5rem;
}

.portfolio-info p {
  color: var(--color-white-60);
  font-size: 0.87rem;
  line-height: 1.6;
  margin-bottom: 1rem;
}

.tech-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.4rem;
}

.tech-tag {
  background: rgba(226,185,111,0.1);
  color: var(--color-gold);
  border: 1px solid rgba(226,185,111,0.2);
  padding: 0.2rem 0.6rem;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 600;
}

.empty-state {
  text-align: center;
  color: rgba(255,255,255,0.3);
  padding: 3rem;
  grid-column: 1 / -1;
}
</style>
