<template>
  <section id="skills" class="section skills-section">
    <div class="container">
      <div class="section-title reveal">
        <span class="script">My Expertise</span>
        <h2>Skills</h2>
        <div class="divider"></div>
      </div>
      <div class="skills-grid">
        <div v-for="(group, i) in skillGroups" :key="i" class="skill-group reveal" :class="'reveal-delay-' + Math.min(i+1, 4)">
          <h3 class="group-title">{{ group.label }}</h3>
          <div class="skill-tags">
            <span v-for="(skill, j) in group.skills" :key="j" class="skill-tag">{{ skill }}</span>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
const DEFAULT_SKILLS = {
  'Virtual Assistance': ['Email Management', 'Calendar Scheduling', 'Data Entry', 'Research', 'CRM Tools', 'Google Workspace', 'Microsoft Office'],
  'Social Media': ['Facebook', 'Instagram', 'TikTok', 'LinkedIn', 'Content Creation', 'Canva', 'Buffer', 'Hootsuite'],
  'Video & Photo': ['Adobe Premiere Pro', 'CapCut', 'Lightroom', 'Photoshop', 'Canva', 'Color Grading', 'Reels Editing'],
  'Tools & Software': ['Trello', 'Asana', 'Slack', 'Zoom', 'Notion', 'Airtable', 'Loom'],
}

export default {
  name: 'SkillsSection',
  props: ['profile'],
  computed: {
    skillGroups() {
      if (this.profile?.skills?.length > 0) {
        const first = this.profile.skills[0]
        if (first && typeof first === 'object' && first.category) {
          return this.profile.skills.map(g => ({
            label: g.category,
            skills: Array.isArray(g.skills) ? g.skills : []
          }))
        }
        return [{ label: 'Skills', skills: this.profile.skills }]
      }
      return Object.entries(DEFAULT_SKILLS).map(([label, skills]) => ({ label, skills }))
    }
  }
}
</script>

<style scoped>
.skills-section {
  background: var(--color-dark);
}

.skills-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 2rem;
}

.skill-group {
  background: var(--color-dark-3);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 1.75rem;
}

.group-title {
  font-size: 0.85rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  color: var(--color-gold);
  margin-bottom: 1.25rem;
  padding-bottom: 0.75rem;
  border-bottom: 1px solid rgba(226,185,111,0.15);
}

.skill-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.skill-tag {
  background: rgba(255,255,255,0.05);
  color: var(--color-white-80);
  border: 1px solid rgba(255,255,255,0.1);
  padding: 0.3rem 0.75rem;
  border-radius: 20px;
  font-size: 0.82rem;
  font-weight: 500;
  transition: all 0.2s;
}

.skill-tag:hover {
  background: rgba(226,185,111,0.12);
  border-color: rgba(226,185,111,0.3);
  color: var(--color-gold);
}
</style>
