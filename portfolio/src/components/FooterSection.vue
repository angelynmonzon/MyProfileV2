<template>
  <footer class="footer">
    <div class="container">
      <div class="footer-top">
        <a href="#hero" @click.prevent="scrollToTop" class="footer-logo">
          <span class="script">Ging</span>
        </a>
        <p class="footer-tagline">Virtual Assistant · Social Media Manager · Creative Professional</p>
      </div>
      <div class="footer-divider"></div>
      <div class="footer-bottom">
        <p class="footer-copy">
          © {{ year }} {{ profile?.full_name || 'Angelyn Monzon' }}. All rights reserved.
        </p>
        <a href="/admin" target="_blank" class="admin-link">Admin</a>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'FooterSection',
  props: ['profile'],
  computed: {
    year() {
      return new Date().getFullYear()
    }
  },
  methods: {
    scrollToTop() {
      window.scrollTo({ top: 0, behavior: 'smooth' })
    }
  }
}
</script>

<style scoped>
.footer {
  background: var(--color-dark-2);
  border-top: 1px solid rgba(255,255,255,0.06);
  padding: 3rem 2rem 2rem;
}

.footer-top {
  text-align: center;
  margin-bottom: 1.5rem;
}

.footer-logo .script {
  font-family: 'Playlist-Script', cursive;
  font-size: 2.5rem;
  color: var(--color-gold);
}

.footer-tagline {
  color: rgba(255,255,255,0.35);
  font-size: 0.82rem;
  margin-top: 0.5rem;
  letter-spacing: 1px;
}

.footer-divider {
  height: 1px;
  background: rgba(255,255,255,0.06);
  margin-bottom: 1.5rem;
}

.footer-bottom {
  display: flex;
  justify-content: space-between;
  align-items: center;
  max-width: 1100px;
  margin: 0 auto;
}

.footer-copy {
  color: rgba(255,255,255,0.3);
  font-size: 0.82rem;
}

.admin-link {
  color: rgba(255,255,255,0.2);
  font-size: 0.75rem;
  transition: color 0.2s;
}

.admin-link:hover {
  color: var(--color-gold);
}
</style>
