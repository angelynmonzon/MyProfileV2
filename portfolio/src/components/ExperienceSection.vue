<template>
  <section id="experience" class="section experience-section">
    <div class="container">
      <div class="section-title reveal">
        <span class="script">Work History</span>
        <h2>Experience</h2>
        <div class="divider"></div>
      </div>
      <div class="timeline">
        <div
          v-for="(exp, i) in experiences"
          :key="i"
          class="timeline-item"
          :class="[
            { 'is-right': i % 2 !== 0 },
            i % 2 === 0 ? 'reveal-left' : 'reveal-right',
          ]"
        >
          <div class="timeline-dot"></div>
          <div class="timeline-card">
            <div class="timeline-date">
              {{ formatDate(exp.start_date) }} —
              {{ exp.is_current ? "Present" : formatDate(exp.end_date) }}
            </div>
            <h3 class="timeline-title">{{ exp.job_title }}</h3>
            <p class="timeline-company">
              <span>{{ exp.company }}</span>
              <span v-if="exp.location" class="timeline-location"
                >· {{ exp.location }}</span
              >
            </p>
            <p class="timeline-desc">{{ exp.description }}</p>
          </div>
        </div>

        <div v-if="!experiences.length" class="empty-state">
          No experience entries yet.
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: "ExperienceSection",
  props: ["profile"],
  computed: {
    experiences() {
      return (this.profile?.experiences || []).filter(
        (exp) => exp.is_visible !== false,
      );
    },
  },
  methods: {
    formatDate(dateString) {
      if (!dateString) return "";
      const d = new Date(dateString);
      return d.toLocaleDateString("en-US", { month: "short", year: "numeric" });
    },
  },
};
</script>

<style scoped>
.experience-section {
  background: var(--color-dark-2);
}

.timeline {
  position: relative;
  padding: 1rem 0;
}

.timeline::before {
  content: "";
  position: absolute;
  left: 50%;
  top: 0;
  bottom: 0;
  width: 1px;
  background: linear-gradient(
    to bottom,
    transparent,
    rgba(226, 185, 111, 0.3),
    transparent
  );
  transform: translateX(-50%);
}

.timeline-item {
  display: flex;
  justify-content: flex-end;
  padding-right: calc(50% + 2rem);
  padding-bottom: 2.5rem;
  position: relative;
}

.timeline-item.is-right {
  justify-content: flex-start;
  padding-right: 0;
  padding-left: calc(50% + 2rem);
}

.timeline-dot {
  position: absolute;
  left: 50%;
  top: 1.25rem;
  width: 12px;
  height: 12px;
  background: var(--color-gold);
  border-radius: 50%;
  transform: translateX(-50%);
  box-shadow: 0 0 0 4px rgba(226, 185, 111, 0.2);
  z-index: 1;
}

.timeline-card {
  background: var(--color-dark-3);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 12px;
  padding: 1.5rem;
  max-width: 420px;
  width: 100%;
  transition: border-color 0.3s;
}

.timeline-card:hover {
  border-color: rgba(226, 185, 111, 0.2);
}

.timeline-date {
  font-size: 0.78rem;
  font-weight: 600;
  letter-spacing: 1px;
  color: var(--color-gold);
  text-transform: uppercase;
  margin-bottom: 0.5rem;
}

.timeline-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-white);
  margin-bottom: 0.35rem;
}

.timeline-company {
  color: var(--color-white-60);
  font-size: 0.9rem;
  margin-bottom: 0.75rem;
}

.timeline-location {
  color: rgba(255, 255, 255, 0.4);
}

.timeline-desc {
  color: var(--color-white-60);
  font-size: 0.88rem;
  line-height: 1.7;
}

.empty-state {
  text-align: center;
  color: rgba(255, 255, 255, 0.3);
  padding: 2rem;
}

@media (max-width: 768px) {
  .timeline::before {
    left: 1rem;
  }

  .timeline-item,
  .timeline-item.is-right {
    justify-content: flex-start;
    padding-left: 3rem;
    padding-right: 0;
  }

  .timeline-dot {
    left: 1rem;
  }

  .timeline-card {
    max-width: 100%;
  }
}
</style>
