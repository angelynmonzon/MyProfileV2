<template>
  <section id="hero" class="hero-wrapper">
    <div class="hero-particles">
      <span v-for="n in 18" :key="n" class="particle" :style="particleStyle(n)"></span>
    </div>
    <div class="hero-inner">
      <div class="hero-content">
        <p class="hero-greeting">Hello, I'm</p>
        <h1 class="hero-name script">{{ profile?.full_name || 'Angelyn Monzon' }}</h1>
        <div class="hero-typed">
          <span class="typed-prefix">I'm a </span>
          <span class="typed-text">{{ typedText }}<span class="cursor">|</span></span>
        </div>
        <p class="hero-bio">{{ profile?.hero_description || profile?.bio || 'A dedicated professional delivering excellence across virtual assistance, social media management, and creative services.' }}</p>
        <div class="hero-actions">
          <a href="#contact" @click.prevent="scrollTo('#contact')" class="btn-gold">Hire Me</a>
          <a href="#portfolio" @click.prevent="scrollTo('#portfolio')" class="btn-outline">View Work</a>
        </div>
        <div class="hero-socials">
          <a v-if="profile?.linkedin_url" :href="profile.linkedin_url" target="_blank" class="social-link" title="LinkedIn">
            <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 0 1-2.063-2.065 2.064 2.064 0 1 1 2.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
          </a>
          <a v-if="profile?.facebook_url" :href="profile.facebook_url" target="_blank" class="social-link" title="Facebook">
            <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
          </a>
          <a v-if="profile?.instagram_url" :href="profile.instagram_url" target="_blank" class="social-link" title="Instagram">
            <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838a6.162 6.162 0 1 0 0 12.324 6.162 6.162 0 0 0 0-12.324zM12 16a4 4 0 1 1 0-8 4 4 0 0 1 0 8zm6.406-11.845a1.44 1.44 0 1 0 0 2.881 1.44 1.44 0 0 0 0-2.881z"/></svg>
          </a>
          <a v-if="profile?.github_url" :href="profile.github_url" target="_blank" class="social-link" title="GitHub">
            <svg viewBox="0 0 24 24" fill="currentColor" width="18" height="18"><path d="M12 .297c-6.63 0-12 5.373-12 12 0 5.303 3.438 9.8 8.205 11.385.6.113.82-.258.82-.577 0-.285-.01-1.04-.015-2.04-3.338.724-4.042-1.61-4.042-1.61C4.422 18.07 3.633 17.7 3.633 17.7c-1.087-.744.084-.729.084-.729 1.205.084 1.838 1.236 1.838 1.236 1.07 1.835 2.809 1.305 3.495.998.108-.776.417-1.305.76-1.605-2.665-.3-5.466-1.332-5.466-5.93 0-1.31.465-2.38 1.235-3.22-.135-.303-.54-1.523.105-3.176 0 0 1.005-.322 3.3 1.23.96-.267 1.98-.399 3-.405 1.02.006 2.04.138 3 .405 2.28-1.552 3.285-1.23 3.285-1.23.645 1.653.24 2.873.12 3.176.765.84 1.23 1.91 1.23 3.22 0 4.61-2.805 5.625-5.475 5.92.42.36.81 1.096.81 2.22 0 1.606-.015 2.896-.015 3.286 0 .315.21.69.825.57C20.565 22.092 24 17.592 24 12.297c0-6.627-5.373-12-12-12"/></svg>
          </a>
        </div>
        <div v-if="profile?.is_available" class="availability-badge">
          <span class="pulse"></span>
          Available for new projects
        </div>
      </div>
      <div class="hero-image-wrap">
        <div class="hero-img-dots"></div>
        <div class="hero-img-accent"></div>
        <div class="hero-portrait">
          <img v-if="profile?.profile_image" :src="profile.profile_image" alt="Profile photo" />
          <div v-else class="portrait-placeholder">
            <span class="script">G</span>
          </div>
          <div class="portrait-overlay"></div>
        </div>
      </div>
    </div>
    <a href="#about" @click.prevent="scrollTo('#about')" class="scroll-hint">
      <span class="scroll-mouse"><span class="scroll-wheel"></span></span>
      <p>Scroll</p>
    </a>
  </section>
</template>

<script>
import { ref, onMounted, onUnmounted, computed } from 'vue'

export default {
  name: 'HeroSection',
  props: ['profile'],
  setup(props) {
    const typedText = ref('')
    const cursorVisible = ref(true)
    let typingTimer = null

    const defaultTitles = ['Virtual Assistant', 'Social Media Manager', 'Admin Assistant', 'Data Annotator', 'Video & Photo Editor']

    const titleList = computed(() => {
      if (props.profile?.title) return props.profile.title.split('/').map(t => t.trim())
      return defaultTitles
    })

    const startTyping = () => {
      let titleIdx = 0
      let charIdx = 0
      let deleting = false

      const type = () => {
        const current = titleList.value[titleIdx]
        if (!deleting) {
          typedText.value = current.slice(0, charIdx + 1)
          charIdx++
          if (charIdx === current.length) {
            deleting = true
            typingTimer = setTimeout(type, 1800)
            return
          }
        } else {
          typedText.value = current.slice(0, charIdx - 1)
          charIdx--
          if (charIdx === 0) {
            deleting = false
            titleIdx = (titleIdx + 1) % titleList.value.length
          }
        }
        typingTimer = setTimeout(type, deleting ? 60 : 100)
      }
      type()
    }

    const scrollTo = (hash) => {
      const el = document.querySelector(hash)
      if (el) el.scrollIntoView({ behavior: 'smooth' })
    }

    const particleStyle = (n) => {
      const size = Math.random() * 3 + 1
      return {
        width: size + 'px',
        height: size + 'px',
        left: (n * 5.5) + '%',
        top: (Math.sin(n) * 40 + 50) + '%',
        animationDuration: (Math.random() * 10 + 8) + 's',
        animationDelay: (Math.random() * 5) + 's',
        opacity: Math.random() * 0.4 + 0.1
      }
    }

    onMounted(() => startTyping())
    onUnmounted(() => clearTimeout(typingTimer))

    return { typedText, titleList, scrollTo, particleStyle }
  }
}
</script>

<style scoped>
.hero-wrapper {
  min-height: 100vh;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: radial-gradient(ellipse at 70% 30%, rgba(226,185,111,0.07) 0%, transparent 55%),
              radial-gradient(ellipse at 15% 80%, rgba(80,80,180,0.05) 0%, transparent 50%),
              var(--color-dark);
}

.hero-particles {
  position: absolute;
  inset: 0;
  pointer-events: none;
}

.particle {
  position: absolute;
  background: var(--color-gold);
  border-radius: 50%;
  animation: floatUp linear infinite;
}

@keyframes floatUp {
  0%   { transform: translateY(0) scale(1); opacity: 0.2; }
  50%  { opacity: 0.5; }
  100% { transform: translateY(-100vh) scale(0.5); opacity: 0; }
}

.hero-inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 4rem;
  max-width: 1100px;
  width: 100%;
  padding: 7rem 2rem 5rem;
}

.hero-content {
  flex: 1;
  max-width: 580px;
}

.hero-greeting {
  color: var(--color-gold);
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 4px;
  text-transform: uppercase;
  margin-bottom: 0.75rem;
  opacity: 0;
  animation: fadeSlideUp 0.6s ease 0.2s forwards;
}

.hero-name {
  font-size: 4.2rem;
  font-family: 'Playlist-Script', cursive;
  color: var(--color-white);
  margin-bottom: 1rem;
  line-height: 1.1;
  opacity: 0;
  animation: fadeSlideUp 0.6s ease 0.4s forwards;
}

.hero-typed {
  font-size: 1.1rem;
  font-weight: 600;
  color: var(--color-white-80);
  margin-bottom: 1.5rem;
  min-height: 1.8em;
  opacity: 0;
  animation: fadeSlideUp 0.6s ease 0.6s forwards;
}

.typed-text {
  color: var(--color-gold);
}

.cursor {
  animation: blink 0.8s step-end infinite;
  color: var(--color-gold);
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

.hero-bio {
  color: var(--color-white-60);
  font-size: 1rem;
  line-height: 1.9;
  margin-bottom: 2rem;
  max-width: 480px;
  opacity: 0;
  animation: fadeSlideUp 0.6s ease 0.8s forwards;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  flex-wrap: wrap;
  margin-bottom: 2rem;
  opacity: 0;
  animation: fadeSlideUp 0.6s ease 1s forwards;
}

.hero-socials {
  display: flex;
  gap: 0.75rem;
  margin-bottom: 1.5rem;
  opacity: 0;
  animation: fadeSlideUp 0.6s ease 1.1s forwards;
}

.social-link {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  border: 1px solid rgba(255,255,255,0.12);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-white-60);
  transition: all 0.3s;
}

.social-link:hover {
  border-color: var(--color-gold);
  color: var(--color-gold);
  transform: translateY(-3px);
  background: rgba(226,185,111,0.08);
}

.availability-badge {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(39,174,96,0.1);
  border: 1px solid rgba(39,174,96,0.25);
  color: #2ecc71;
  padding: 0.4rem 1rem;
  border-radius: 20px;
  font-size: 0.82rem;
  font-weight: 600;
  opacity: 0;
  animation: fadeSlideUp 0.6s ease 1.2s forwards;
}

.pulse {
  width: 8px;
  height: 8px;
  background: #2ecc71;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(46,204,113,0.5); }
  50% { box-shadow: 0 0 0 7px rgba(46,204,113,0); }
}

.hero-image-wrap {
  flex-shrink: 0;
  position: relative;
  width: 340px;
  height: 460px;
  opacity: 0;
  animation: fadeIn 0.8s ease 0.5s forwards;
}

.hero-img-dots {
  position: absolute;
  bottom: -20px;
  right: -20px;
  width: 120px;
  height: 120px;
  background-image: radial-gradient(circle, rgba(226,185,111,0.35) 1.5px, transparent 1.5px);
  background-size: 14px 14px;
  z-index: 0;
  border-radius: 4px;
}

.hero-img-accent {
  position: absolute;
  top: -12px;
  left: -12px;
  width: 80px;
  height: 80px;
  border-top: 3px solid var(--color-gold);
  border-left: 3px solid var(--color-gold);
  border-radius: 4px 0 0 0;
  z-index: 3;
  opacity: 0.7;
}

.hero-portrait {
  width: 100%;
  height: 100%;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  z-index: 1;
  box-shadow: 0 30px 80px rgba(0,0,0,0.5), 0 0 0 1px rgba(226,185,111,0.15);
}

.hero-portrait img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: top center;
  display: block;
}

.portrait-overlay {
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 35%;
  background: linear-gradient(to top, rgba(13,13,13,0.6), transparent);
  pointer-events: none;
}

.portrait-placeholder {
  width: 100%;
  height: 100%;
  background: linear-gradient(160deg, #1a1a2e 0%, #0f3460 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.portrait-placeholder .script {
  font-family: 'Playlist-Script', cursive;
  font-size: 10rem;
  color: var(--color-gold);
  opacity: 0.5;
}

.scroll-hint {
  position: absolute;
  bottom: 2rem;
  left: 50%;
  transform: translateX(-50%);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.4rem;
  color: rgba(255,255,255,0.3);
  font-size: 0.7rem;
  letter-spacing: 2px;
  text-transform: uppercase;
  text-decoration: none;
  animation: fadeIn 1s ease 1.5s both;
  transition: color 0.2s;
}

.scroll-hint:hover { color: var(--color-gold); }

.scroll-mouse {
  width: 22px;
  height: 36px;
  border: 2px solid currentColor;
  border-radius: 12px;
  display: flex;
  justify-content: center;
  padding-top: 5px;
}

.scroll-wheel {
  width: 3px;
  height: 7px;
  background: currentColor;
  border-radius: 3px;
  animation: scrollWheel 1.8s ease-in-out infinite;
}

@keyframes scrollWheel {
  0%   { transform: translateY(0); opacity: 1; }
  100% { transform: translateY(12px); opacity: 0; }
}

@keyframes fadeSlideUp {
  from { opacity: 0; transform: translateY(25px); }
  to   { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}

@media (max-width: 900px) {
  .hero-inner {
    flex-direction: column-reverse;
    text-align: center;
    padding: 6rem 1.5rem 4rem;
    gap: 2.5rem;
  }
  .hero-content { max-width: 100%; }
  .hero-bio { margin: 0 auto 2rem; }
  .hero-actions, .hero-socials { justify-content: center; }
  .hero-image-wrap { width: 240px; height: 320px; }
  .hero-img-dots { display: none; }
  .hero-name { font-size: 3rem; }
}
</style>
