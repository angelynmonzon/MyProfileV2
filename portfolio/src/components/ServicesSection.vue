<template>
  <section id="services" class="section services-section">
    <div class="container">
      <div class="section-title reveal">
        <span class="script">What I Do</span>
        <h2>Services</h2>
        <div class="divider"></div>
      </div>
      <div class="services-grid">
        <div v-for="(service, i) in serviceCards" :key="i" class="service-card reveal" :class="'reveal-delay-' + Math.min(i+1, 5)">
          <div class="service-icon">{{ service.icon }}</div>
          <h3>{{ service.title }}</h3>
          <p>{{ service.desc }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ServicesSection',
  props: ['profile'],
  computed: {
    serviceCards() {
      const defaultCards = [
        { icon: '�', title: 'Social Media Management', desc: 'Full-cycle social media management across platforms — strategy, posting, engagement, and performance tracking to build your brand.' },
        { icon: '📅', title: 'Content Planning & Scheduling', desc: 'Strategic content calendars and scheduled posts to keep your audience engaged consistently without missing a beat.' },
        { icon: '🎬', title: 'Video Editing (Reels, TikTok, Shorts & YouTube)', desc: 'Eye-catching short-form and long-form video edits optimized for Instagram Reels, TikTok, YouTube Shorts, and full-length YouTube content.' },
        { icon: '🎨', title: 'Canva Graphic Design', desc: 'On-brand graphics, social media templates, story covers, carousels, banners, and marketing materials designed in Canva.' },
        { icon: '✍️', title: 'Scriptwriting & Content Creation', desc: 'Compelling scripts, captions, blog posts, and content pieces crafted to capture your brand voice and engage your audience.' },
        { icon: '🤝', title: 'Community Engagement & Audience Growth', desc: 'Active community management, responding to comments and DMs, fostering relationships, and growing an authentic following.' },
        { icon: '�', title: 'Email Management', desc: 'Inbox organization, drafting responses, newsletter management, and keeping your communications clear and professional.' },
        { icon: '📊', title: 'Data Entry & Administrative Support', desc: 'Accurate data entry, spreadsheet management, file organization, and reliable administrative tasks to keep operations smooth.' },
        { icon: '👥', title: 'Facebook Group Management', desc: 'Moderation, member engagement, post scheduling, and community building within Facebook Groups to grow a loyal audience.' },
        { icon: '📌', title: 'Pinterest Management', desc: 'Creating and scheduling pins, board strategy, keyword optimization, and growing traffic through Pinterest marketing.' },
        { icon: '🔍', title: 'Research & Trend Analysis', desc: 'In-depth research on topics, competitors, trending content, and industry insights to fuel informed decisions and fresh ideas.' },
        { icon: '�️', title: 'Calendar & Project Management', desc: 'Scheduling, task coordination, deadline tracking, and project organization to ensure everything runs on time and on track.' },
      ]
      if (this.profile?.services_offered?.length > 0) {
        return this.profile.services_offered.map((s, i) => {
          if (s && typeof s === 'object') {
            return {
              icon: s.icon || defaultCards[i % defaultCards.length].icon,
              title: s.title || '',
              desc: s.description || ''
            }
          }
          return {
            icon: defaultCards[i % defaultCards.length].icon,
            title: s,
            desc: defaultCards[i % defaultCards.length].desc
          }
        })
      }
      return defaultCards
    }
  }
}
</script>

<style scoped>
.services-section {
  background: var(--color-dark-2);
}

.services-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 1.25rem;
}

.service-card {
  background: var(--color-dark-3);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 2rem 1.5rem;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.service-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0;
  width: 100%;
  height: 3px;
  background: linear-gradient(90deg, var(--color-gold), transparent);
  opacity: 0;
  transition: opacity 0.3s;
}

.service-card:hover {
  border-color: rgba(226,185,111,0.2);
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(0,0,0,0.3);
}

.service-card:hover::before {
  opacity: 1;
}

.service-icon {
  font-size: 2.2rem;
  margin-bottom: 1rem;
}

.service-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--color-white);
  margin-bottom: 0.75rem;
  letter-spacing: 0.5px;
}

.service-card p {
  color: var(--color-white-60);
  font-size: 0.9rem;
  line-height: 1.7;
}
</style>
