<template>
  <section id="contact" class="section contact-section">
    <div class="container">
      <div class="section-title reveal">
        <span class="script">Get In Touch</span>
        <h2>Contact</h2>
        <div class="divider"></div>
      </div>
      <div class="contact-wrapper reveal">
        <p class="contact-intro">
          Ready to work together? Reach out and let's discuss how I can help your business grow.
        </p>
        <div class="contact-items">
          <div v-if="profile?.email" class="contact-item">
            <span class="contact-icon">✉️</span>
            <div>
              <p class="contact-label">Email</p>
              <a :href="'mailto:' + profile.email" target="_blank" class="contact-value">{{ profile.email }}</a>
            </div>
          </div>
        </div>
        <div class="social-links">
          <a v-if="profile?.linkedin_url" :href="profile.linkedin_url" target="_blank" class="social-btn">LinkedIn</a>
          <a v-if="profile?.facebook_url" :href="profile.facebook_url" target="_blank" class="social-btn">Facebook</a>
          <a v-if="profile?.instagram_url" :href="profile.instagram_url" target="_blank" class="social-btn">Instagram</a>
          <a v-if="profile?.twitter_url" :href="profile.twitter_url" target="_blank" class="social-btn">Twitter</a>
          <a v-if="profile?.github_url" :href="profile.github_url" target="_blank" class="social-btn">GitHub</a>
        </div>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'ContactSection',
  props: ['profile']
}
</script>

<style scoped>
.contact-section {
  background: var(--color-dark);
}

.contact-wrapper {
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
}

.contact-intro {
  color: var(--color-white-60);
  font-size: 1rem;
  line-height: 1.8;
  margin-bottom: 2rem;
}

.contact-items {
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
  margin-bottom: 2rem;
  align-items: center;
}

.contact-item {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.contact-icon {
  font-size: 1.5rem;
}

.contact-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--color-gold);
  margin-bottom: 0.15rem;
}

.contact-value {
  color: var(--color-white-80);
  font-size: 1rem;
  transition: color 0.2s;
}

a.contact-value:hover {
  color: var(--color-gold);
}

.social-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
}

.social-btn {
  padding: 0.5rem 1.25rem;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 20px;
  color: var(--color-white-60);
  font-size: 0.85rem;
  font-weight: 600;
  transition: all 0.2s;
}

.social-btn:hover {
  border-color: var(--color-gold);
  color: var(--color-gold);
}
</style>
