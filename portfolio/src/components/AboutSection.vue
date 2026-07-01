<template>
  <section id="about" class="section about-section">
    <div class="container">
      <div class="section-title reveal">
        <span class="script">About Me</span>
        <h2>Who I Am</h2>
        <div class="divider"></div>
      </div>
      <div class="about-wrapper">
        <div class="about-image-wrap reveal-left">
          <div class="about-img-frame">
            <img v-if="profile?.profile_image" :src="'http://localhost:8000/media/' + profile.profile_image" alt="About photo" />
            <div v-else class="about-img-placeholder">
              <span class="script">Ging</span>
            </div>
          </div>
          <div class="about-card floating-card">
            <span class="floating-number">{{ yearsActive }}+</span>
            <span class="floating-label">Years of Experience</span>
          </div>
        </div>
        <div class="about-content reveal-right">
          <h3 class="about-name">{{ profile?.full_name || 'Angelyn Monzon' }}</h3>
          <p class="about-title-label">{{ profile?.title || 'Virtual Assistant & Creative Professional' }}</p>
          <p class="about-bio">{{ profile?.bio || 'I am a dedicated and detail-oriented professional specializing in virtual assistance, social media management, administrative support, data annotation, and creative content production. I bring efficiency, creativity, and reliability to every project.' }}</p>
          <div class="about-stats">
            <div class="stat">
              <span class="stat-num">{{ (profile?.services_offered || []).length || 6 }}</span>
              <span class="stat-label">Services</span>
            </div>
            <div class="stat">
              <span class="stat-num">{{ (profile?.projects || []).length || 0 }}</span>
              <span class="stat-label">Projects</span>
            </div>
            <div class="stat">
              <span class="stat-num">{{ (profile?.experiences || []).length || 0 }}</span>
              <span class="stat-label">Experience</span>
            </div>
          </div>
          <div class="about-details">
            <div v-if="profile?.location" class="detail-item">
              <span class="detail-icon">📍</span>
              <span>{{ profile.location }}</span>
            </div>
            <div v-if="profile?.email" class="detail-item">
              <span class="detail-icon">✉️</span>
              <a :href="'mailto:' + profile.email">{{ profile.email }}</a>
            </div>
            <div v-if="profile?.website_url" class="detail-item">
              <span class="detail-icon">🌐</span>
              <a :href="profile.website_url" target="_blank">{{ profile.website_url }}</a>
            </div>
          </div>
          <div class="about-actions">
            <a href="#contact" @click.prevent="scrollTo('#contact')" class="btn-gold">Work With Me</a>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'AboutSection',
  props: ['profile'],
  computed: {
    yearsActive() {
      const experiences = this.profile?.experiences || []
      if (!experiences.length) return 2
      const oldest = experiences.reduce((min, e) => {
        const d = new Date(e.start_date)
        return d < min ? d : min
      }, new Date())
      return Math.max(1, new Date().getFullYear() - oldest.getFullYear())
    }
  },
  methods: {
    scrollTo(hash) {
      const el = document.querySelector(hash)
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    }
  }
}
</script>

<style scoped>
.about-section {
  background: var(--color-dark);
}

.about-wrapper {
  display: grid;
  grid-template-columns: 1fr 1.3fr;
  gap: 5rem;
  align-items: center;
}

.about-image-wrap {
  position: relative;
}

.about-img-frame {
  width: 100%;
  aspect-ratio: 3/4;
  border-radius: 16px;
  overflow: hidden;
  border: 2px solid rgba(226,185,111,0.2);
}

.about-img-frame img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.about-img-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, #1a1a2e, #16213e);
  display: flex;
  align-items: center;
  justify-content: center;
}

.about-img-placeholder .script {
  font-family: 'Playlist-Script', cursive;
  font-size: 5rem;
  color: var(--color-gold);
  opacity: 0.5;
}

.floating-card {
  position: absolute;
  bottom: -1.5rem;
  right: -1.5rem;
  background: linear-gradient(135deg, #e2b96f, #c9993a);
  color: #0d0d0d;
  border-radius: 12px;
  padding: 1.25rem 1.5rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(226,185,111,0.3);
}

.floating-number {
  display: block;
  font-size: 2rem;
  font-weight: 800;
}

.floating-label {
  display: block;
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  opacity: 0.8;
}

.about-name {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--color-white);
  margin-bottom: 0.35rem;
}

.about-title-label {
  color: var(--color-gold);
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 1px;
  margin-bottom: 1.25rem;
}

.about-bio {
  color: var(--color-white-60);
  line-height: 1.9;
  margin-bottom: 2rem;
}

.about-stats {
  display: flex;
  gap: 2rem;
  margin-bottom: 2rem;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255,255,255,0.06);
}

.stat {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.stat-num {
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-gold);
}

.stat-label {
  font-size: 0.75rem;
  color: rgba(255,255,255,0.4);
  text-transform: uppercase;
  letter-spacing: 1px;
}

.about-details {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.detail-item {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--color-white-60);
  font-size: 0.9rem;
}

.detail-icon {
  font-size: 1rem;
}

.detail-item a {
  color: var(--color-white-60);
  transition: color 0.2s;
}

.detail-item a:hover {
  color: var(--color-gold);
}

@media (max-width: 900px) {
  .about-wrapper {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }

  .about-img-frame {
    aspect-ratio: 4/3;
    max-width: 400px;
    margin: 0 auto;
  }

  .floating-card {
    right: 0;
  }

  .about-stats {
    justify-content: center;
  }
}
</style>
