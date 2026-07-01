<template>
  <section id="contact" class="section contact-section">
    <div class="container">
      <div class="section-title reveal">
        <span class="script">Get In Touch</span>
        <h2>Contact</h2>
        <div class="divider"></div>
      </div>
      <div class="contact-wrapper">
        <div class="contact-info reveal-left">
          <p class="contact-intro">
            Ready to work together? Reach out and let's discuss how I can help your business grow.
          </p>
          <div class="contact-items">
            <div v-if="profile?.email" class="contact-item">
              <span class="contact-icon">✉️</span>
              <div>
                <p class="contact-label">Email</p>
                <a :href="'mailto:' + profile.email" class="contact-value">{{ profile.email }}</a>
              </div>
            </div>
            <div v-if="profile?.phone" class="contact-item">
              <span class="contact-icon">📞</span>
              <div>
                <p class="contact-label">Phone</p>
                <a :href="'tel:' + profile.phone" class="contact-value">{{ profile.phone }}</a>
              </div>
            </div>
            <div v-if="profile?.location" class="contact-item">
              <span class="contact-icon">📍</span>
              <div>
                <p class="contact-label">Location</p>
                <p class="contact-value">{{ profile.location }}</p>
              </div>
            </div>
          </div>
          <div class="social-links">
            <a v-if="profile?.linkedin_url" :href="profile.linkedin_url" target="_blank" class="social-btn">LinkedIn</a>
            <a v-if="profile?.facebook_url" :href="profile.facebook_url" target="_blank" class="social-btn">Facebook</a>
            <a v-if="profile?.instagram_url" :href="profile.instagram_url" target="_blank" class="social-btn">Instagram</a>
            <a v-if="profile?.twitter_url" :href="profile.twitter_url" target="_blank" class="social-btn">Twitter</a>
          </div>
        </div>
        <form @submit.prevent="sendMessage" class="contact-form reveal-right">
          <div class="form-group">
            <label>Your Name</label>
            <input v-model="form.name" type="text" placeholder="John Doe" required />
          </div>
          <div class="form-group">
            <label>Your Email</label>
            <input v-model="form.email" type="email" placeholder="john@example.com" required />
          </div>
          <div class="form-group">
            <label>Subject</label>
            <input v-model="form.subject" type="text" placeholder="Project Inquiry" />
          </div>
          <div class="form-group">
            <label>Message</label>
            <textarea v-model="form.message" rows="5" placeholder="Tell me about your project..." required></textarea>
          </div>
          <button type="submit" class="btn-gold" :disabled="sending">
            {{ sending ? 'Sending...' : 'Send Message' }}
          </button>
          <p v-if="successMsg" class="success-msg">{{ successMsg }}</p>
        </form>
      </div>
    </div>
  </section>
</template>

<script>
import { ref } from 'vue'

export default {
  name: 'ContactSection',
  props: ['profile'],
  setup() {
    const form = ref({ name: '', email: '', subject: '', message: '' })
    const sending = ref(false)
    const successMsg = ref('')

    const sendMessage = async () => {
      sending.value = true
      await new Promise(r => setTimeout(r, 1000))
      successMsg.value = "Thank you! I'll get back to you soon."
      form.value = { name: '', email: '', subject: '', message: '' }
      sending.value = false
      setTimeout(() => successMsg.value = '', 5000)
    }

    return { form, sending, successMsg, sendMessage }
  }
}
</script>

<style scoped>
.contact-section {
  background: var(--color-dark);
}

.contact-wrapper {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 4rem;
  align-items: start;
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
}

.contact-item {
  display: flex;
  gap: 1rem;
  align-items: flex-start;
}

.contact-icon {
  font-size: 1.3rem;
  margin-top: 2px;
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
  font-size: 0.95rem;
  transition: color 0.2s;
}

a.contact-value:hover {
  color: var(--color-gold);
}

.social-links {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
}

.social-btn {
  padding: 0.4rem 1.1rem;
  border: 1px solid rgba(255,255,255,0.15);
  border-radius: 20px;
  color: var(--color-white-60);
  font-size: 0.82rem;
  font-weight: 600;
  transition: all 0.2s;
}

.social-btn:hover {
  border-color: var(--color-gold);
  color: var(--color-gold);
}

.contact-form {
  background: var(--color-dark-3);
  border: 1px solid rgba(255,255,255,0.06);
  border-radius: 16px;
  padding: 2.5rem;
  display: flex;
  flex-direction: column;
  gap: 1.25rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.4rem;
}

.form-group label {
  font-size: 0.8rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--color-white-60);
}

.form-group input,
.form-group textarea {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.1);
  border-radius: 8px;
  padding: 0.75rem 1rem;
  color: var(--color-white);
  font-size: 0.95rem;
  font-family: inherit;
  transition: border-color 0.3s;
  resize: vertical;
}

.form-group input::placeholder,
.form-group textarea::placeholder {
  color: rgba(255,255,255,0.25);
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--color-gold);
}

.btn-gold {
  width: 100%;
  padding: 0.9rem;
  background: linear-gradient(135deg, #e2b96f, #c9993a);
  color: #0d0d0d;
  border: none;
  border-radius: 8px;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  cursor: pointer;
  transition: all 0.3s;
}

.btn-gold:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(226,185,111,0.3);
}

.btn-gold:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.success-msg {
  text-align: center;
  color: #27ae60;
  font-size: 0.9rem;
  font-weight: 600;
  animation: fadeIn 0.4s ease;
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}

@media (max-width: 768px) {
  .contact-wrapper {
    grid-template-columns: 1fr;
    gap: 2.5rem;
  }
}
</style>
