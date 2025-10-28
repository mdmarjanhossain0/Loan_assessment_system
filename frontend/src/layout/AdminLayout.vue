<template>
  <!-- Navbar -->
  <nav
    class="fixed top-0 z-50 w-full bg-white border-b border-gray-200 dark:bg-gray-800 dark:border-gray-700"
  >
    <div class="px-3 py-3 lg:px-5 lg:pl-3">
      <div class="flex items-center justify-between">
        <!-- Left -->
        <div class="flex items-center justify-start">
          <button
            @click="toggleSidebar"
            type="button"
            class="inline-flex items-center p-2 text-sm text-gray-500 rounded-lg sm:hidden hover:bg-gray-100 
            focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 
            dark:focus:ring-gray-600"
          >
            <span class="sr-only">Open sidebar</span>
            <svg class="w-6 h-6" fill="currentColor" viewBox="0 0 24 24">
              <path
                fill-rule="evenodd"
                d="M3 5h18M3 12h18M3 19h18"
                stroke="currentColor"
                stroke-width="2"
                stroke-linecap="round"
              />
            </svg>
          </button>
          <router-link to="/admin/dashboard" class="flex items-center ms-2 md:me-24">
            <img
              src="https://flowbite.com/docs/images/logo.svg"
              class="h-8 me-3"
              alt="Logo"
            />
            <span class="text-xl font-semibold whitespace-nowrap dark:text-white"
              >Admin Panel</span
            >
          </router-link>
        </div>

        <!-- Right -->
        <div class="flex items-center relative">
          <button
            @click="toggleUserMenu"
            type="button"
            class="flex items-center text-sm bg-gray-800 rounded-full focus:ring-4 focus:ring-gray-300 
            dark:focus:ring-gray-600"
          >
            <span class="sr-only">Open user menu</span>
            <img
              class="w-8 h-8 rounded-full"
              src="https://flowbite.com/docs/images/people/profile-picture-5.jpg"
              alt="user photo"
            />
          </button>

          <!-- User dropdown -->
          <div
            v-show="userMenuOpen"
            class="absolute right-0 mt-10 w-48 z-50 text-base list-none bg-white divide-y divide-gray-100 
            rounded-md shadow dark:bg-gray-700 dark:divide-gray-600"
          >
            <div class="px-4 py-3">
              <p class="text-sm font-medium text-gray-900 dark:text-white">Admin User</p>
              <p class="text-xs text-gray-500 truncate dark:text-gray-400">
                admin@example.com
              </p>
            </div>
            <ul class="py-1">
              <li>
                <router-link
                  to="/admin/settings"
                  class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 
                  dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white"
                >
                  Settings
                </router-link>
              </li>
              <li>
                <button
                  @click="logout"
                  class="block w-full text-left px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 
                  dark:text-gray-300 dark:hover:bg-gray-600 dark:hover:text-white"
                >
                  Logout
                </button>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </nav>

  <!-- Sidebar -->
  <aside
    :class="[
      'fixed top-0 left-0 z-40 w-64 h-screen pt-20 transition-transform bg-white border-r border-gray-200 dark:bg-gray-800 dark:border-gray-700',
      sidebarOpen ? 'translate-x-0' : '-translate-x-full sm:translate-x-0'
    ]"
  >
    <div class="h-full px-3 pb-4 overflow-y-auto">
      <ul class="space-y-1 font-medium">
        <li v-for="item in menuItems" :key="item.label">
          <router-link
            :to="item.to"
            class="flex items-center gap-3 p-2 text-gray-900 rounded-lg dark:text-white 
            hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
            active-class="bg-gray-100 dark:bg-gray-700"
          >
            <component :is="item.icon" class="w-5 h-5 text-gray-500 dark:text-gray-400" />
            <span>{{ item.label }}</span>
          </router-link>
        </li>

        <li>
          <button
            @click="logout"
            class="flex items-center gap-3 w-full p-2 text-gray-900 rounded-lg dark:text-white 
            hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          >
            <LogoutIcon class="w-5 h-5 text-gray-500 dark:text-gray-400" />
            <span>Logout</span>
          </button>
        </li>
      </ul>
    </div>
  </aside>

  <!-- Main -->
  <main class="p-4 sm:ml-64">
    <div class="mt-14">
      <router-view />
    </div>
  </main>
</template>

<script setup>
import { ref } from 'vue'
import { useAuthStore } from "../stores/auth"
import { useRouter } from 'vue-router'


const auth = useAuthStore()
const router = useRouter()

const sidebarOpen = ref(false)
const userMenuOpen = ref(false)
const toggleSidebar = () => (sidebarOpen.value = !sidebarOpen.value)
const toggleUserMenu = () => (userMenuOpen.value = !userMenuOpen.value)
const logout = () => {
  auth.logout()
  router.push("/")
}

const DashboardIcon = {
  template: `<svg fill="none" stroke="currentColor" stroke-width="2"
    viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path stroke-linecap="round" stroke-linejoin="round" d="M3 12l2-2m0 0l7-7 7 7M13 5v6h6"/>
  </svg>`
}
const UsersIcon = {
  template: `<svg fill="none" stroke="currentColor" stroke-width="2"
    viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
    <path stroke-linecap="round" stroke-linejoin="round"
    d="M17 20h5V9l-7-7H5a2 2 0 00-2 2v11h2m0 0a5 5 0 0010 0m-10 0h10"/>
  </svg>`
}
const AppsIcon = {
  template: `<svg fill="none" stroke="currentColor" stroke-width="2"
    viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round"
    d="M4 4h6v6H4zM14 4h6v6h-6zM4 14h6v6H4zM14 14h6v6h-6z"/></svg>`
}
const SettingsIcon = {
  template: `<svg fill="none" stroke="currentColor" stroke-width="2"
    viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round"
    d="M10.325 4.317a1 1 0 011.35-.937l1.937.518a1 1 0 
    00.972-.242l1.367-1.367a1 1 0 011.414 0l1.415 
    1.414a1 1 0 010 1.415l-1.367 1.367a1 1 0 
    00-.242.972l.518 1.937a1 1 0 01-.937 1.35l-1.937.518a1 1 
    0 00-.707.707l-.518 1.937a1 1 0 01-1.35.937l-1.937-.518a1 1 
    0 00-.972.242l-1.367 1.367a1 1 0 01-1.414 0l-1.415-1.414a1 
    1 0 010-1.415l1.367-1.367a1 1 0 00.242-.972l-.518-1.937a1 1 
    0 01.937-1.35l1.937-.518a1 1 0 00.707-.707l.518-1.937zM12 
    15a3 3 0 100-6 3 3 0 000 6z"/></svg>`
}
const LogoutIcon = {
  template: `<svg fill="none" stroke="currentColor" stroke-width="2"
    viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round"
    d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a2 2 0 
    01-2 2H5a2 2 0 01-2-2V7a2 2 0 
    012-2h6a2 2 0 012 2v1"/></svg>`
}

const menuItems = [
  { label: 'Dashboard', to: '/dashboard', icon: DashboardIcon },
  { label: 'Users', to: 'users', icon: UsersIcon },
  { label: 'Applications', to: '/dashboard/loan', icon: AppsIcon },
  { label: 'Settings', to: 'settings', icon: SettingsIcon }
]
</script>
