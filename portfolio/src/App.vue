<template>
  <div id="app">
    <template v-if="isAdminRoute">
      <nav class="admin-navbar">
        <div class="nav-brand">
          <span class="brand-icon">✦</span>
          <h1>Ging's CMS</h1>
        </div>
        <div class="nav-links">
          <router-link to="/admin/profile-cms">Profile</router-link>
          <router-link v-if="authStore.isSuperAdmin" to="/admin/users">Users</router-link>
          <div class="user-info">
            <span class="user-badge">{{ authStore.user?.username }}</span>
          </div>
          <button @click="logout" class="logout-btn">Logout</button>
        </div>
      </nav>
    </template>
    <template v-else>
      <NavBar :profile="profile" />
    </template>
    <router-view :profile="profile" :loading="loading" />
    <FooterSection v-if="!isAdminRoute" :profile="profile" />
  </div>
</template>

<script>
import { ref, onMounted, onUnmounted, nextTick, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import NavBar from './components/NavBar.vue'
import FooterSection from './components/FooterSection.vue'
import { fetchPublicProfile } from './api/profile.js'

export default {
  name: 'App',
  components: { NavBar, FooterSection },
  setup() {
    const route = useRoute()
    const router = useRouter()
    const authStore = useAuthStore()
    const profile = ref(null)
    const loading = ref(true)

    const isAdminRoute = computed(() => route.path.startsWith('/admin'))

    const initReveal = () => {
      const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible')
            observer.unobserve(entry.target)
          }
        })
      }, { threshold: 0, rootMargin: '0px 0px -40px 0px' })

      document.querySelectorAll('.reveal, .reveal-left, .reveal-right').forEach(el => {
        const rect = el.getBoundingClientRect()
        if (rect.top < window.innerHeight && rect.bottom > 0) {
          el.classList.add('visible')
        } else {
          observer.observe(el)
        }
      })
    }

    const checkVisible = () => {
      document.querySelectorAll('.reveal:not(.visible), .reveal-left:not(.visible), .reveal-right:not(.visible)').forEach(el => {
        const rect = el.getBoundingClientRect()
        if (rect.top < window.innerHeight - 40 && rect.bottom > 0) {
          el.classList.add('visible')
        }
      })
    }

    const logout = () => {
      authStore.logout()
      router.push('/admin/login')
    }

    onMounted(async () => {
      try {
        const data = await fetchPublicProfile()
        profile.value = data.length > 0 ? data[0] : null
      } catch (err) {
        console.error('Failed to load profile:', err)
      } finally {
        loading.value = false
        await nextTick()
        if (!isAdminRoute.value) {
          initReveal()
          setTimeout(checkVisible, 100)
        }
      }
      window.addEventListener('scroll', checkVisible, { passive: true })
    })

    onUnmounted(() => {
      window.removeEventListener('scroll', checkVisible)
    })

    return { profile, loading, isAdminRoute, authStore, logout }
  }
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  background-color: #f5f5f5;
}

.admin-navbar {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
  color: white;
  padding: 1rem 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  box-shadow: 0 2px 10px rgba(0,0,0,0.3);
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.brand-icon {
  color: #e2b96f;
  font-size: 1.4rem;
}

.nav-brand h1 {
  font-size: 1.4rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.nav-links {
  display: flex;
  gap: 1rem;
  align-items: center;
}

.nav-links a {
  color: rgba(255,255,255,0.85);
  text-decoration: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  transition: all 0.3s;
  font-size: 0.95rem;
}

.nav-links a:hover,
.nav-links a.router-link-active {
  background-color: rgba(255,255,255,0.15);
  color: white;
}

.user-info {
  display: flex;
  align-items: center;
}

.user-badge {
  background: rgba(226,185,111,0.2);
  color: #e2b96f;
  border: 1px solid rgba(226,185,111,0.4);
  padding: 0.3rem 0.8rem;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 600;
}

.logout-btn {
  background-color: rgba(231,76,60,0.8);
  color: white;
  border: none;
  padding: 0.5rem 1rem;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s;
  font-size: 0.95rem;
}

.logout-btn:hover {
  background-color: #c0392b;
}
</style>
