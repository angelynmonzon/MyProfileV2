<template>
  <div id="app">
    <nav class="navbar" v-if="authStore.isAuthenticated">
      <div class="nav-brand">
        <span class="brand-icon">✦</span>
        <h1>Ging's CMS</h1>
      </div>
      <div class="nav-links">
        <router-link to="/profile-cms">My Profile</router-link>
        <router-link v-if="authStore.isSuperAdmin" to="/users">Users</router-link>
        <div class="user-info">
          <span class="user-badge">{{ authStore.user?.username }}</span>
        </div>
        <button @click="logout" class="logout-btn">Logout</button>
      </div>
    </nav>
    <main :class="authStore.isAuthenticated ? 'main-content' : 'main-content-full'">
      <router-view />
    </main>
  </div>
</template>

<script>
import { useAuthStore } from './stores/auth'
import { useRouter } from 'vue-router'

export default {
  name: 'App',
  setup() {
    const authStore = useAuthStore()
    const router = useRouter()
    
    const logout = () => {
      authStore.logout()
      router.push('/login')
    }
    
    return { authStore, logout }
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

.navbar {
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

.main-content {
  padding: 2rem;
  max-width: 1200px;
  margin: 0 auto;
}

.main-content-full {
  min-height: 100vh;
}
</style>
