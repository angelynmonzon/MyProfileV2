<template>
  <section id="education" class="section education-section">
    <div class="container">
      <div class="section-title reveal">
        <span class="script">Academic Background</span>
        <h2>Education</h2>
        <div class="divider"></div>
      </div>
      <div class="edu-grid">
        <div v-for="(edu, i) in education" :key="i" class="edu-card reveal" :class="'reveal-delay-' + Math.min(i+1, 4)">
          <div class="edu-year">
            {{ formatDate(edu.start_date) }} — {{ edu.is_current ? 'Present' : formatDate(edu.end_date) }}
          </div>
          <div class="edu-icon">🎓</div>
          <h3 class="edu-degree">{{ edu.degree }}</h3>
          <p class="edu-institution">{{ edu.institution }}</p>
          <p v-if="edu.location" class="edu-location">{{ edu.location }}</p>
          <p v-if="edu.description" class="edu-desc">{{ edu.description }}</p>
        </div>

        <div v-if="!education.length" class="empty-state">
          No education entries yet.
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'EducationSection',
  props: ['profile'],
  computed: {
    education() {
      return this.profile?.education || []
    }
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return ''
      const d = new Date(dateString)
      return d.toLocaleDateString('en-US', { month: 'short', year: 'numeric' })
    }
  }
}
</script>

<style scoped>
.education-section {
  background: var(--color-dark);
}

.edu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 1.5rem;
}

.edu-card {
  background: var(--color-dark-3);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 2rem 1.5rem;
  text-align: center;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.edu-card::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 3px;
  background: linear-gradient(90deg, var(--color-gold), #c9993a);
  transform: scaleX(0);
  transition: transform 0.3s;
}

.edu-card:hover {
  transform: translateY(-4px);
  border-color: rgba(226,185,111,0.2);
}

.edu-card:hover::after {
  transform: scaleX(1);
}

.edu-year {
  font-size: 0.78rem;
  font-weight: 600;
  color: var(--color-gold);
  letter-spacing: 1px;
  text-transform: uppercase;
  margin-bottom: 1rem;
}

.edu-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
}

.edu-degree {
  font-size: 1.05rem;
  font-weight: 700;
  color: var(--color-white);
  margin-bottom: 0.4rem;
  line-height: 1.4;
}

.edu-institution {
  font-size: 0.9rem;
  color: var(--color-gold);
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.edu-location {
  font-size: 0.82rem;
  color: rgba(255,255,255,0.4);
  margin-bottom: 0.75rem;
}

.edu-desc {
  font-size: 0.85rem;
  color: var(--color-white-60);
  line-height: 1.6;
}

.empty-state {
  text-align: center;
  color: rgba(255,255,255,0.3);
  padding: 2rem;
  grid-column: 1 / -1;
}
</style>
