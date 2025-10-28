<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
      <h2 class="text-2xl font-semibold text-center mb-6">Login</h2>

      <form @submit.prevent="handleLogin" class="space-y-5">
        <div>
          <label for="email" class="block text-gray-700 font-medium mb-1">Email</label>
          <input
            v-model="email"
            type="email"
            id="email"
            required
            class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            placeholder="you@example.com"
          />
        </div>

        <div>
          <label for="password" class="block text-gray-700 font-medium mb-1">Password</label>
          <input
            v-model="password"
            type="password"
            id="password"
            required
            class="w-full border border-gray-300 rounded px-3 py-2 focus:ring-2 focus:ring-blue-500 focus:outline-none"
            placeholder="Enter your password"
          />
        </div>

        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-2 rounded-md hover:bg-blue-700 transition duration-200"
          :disabled="loading"
        >
          {{ loading ? 'Logging in...' : 'Login' }}
        </button>
      </form>

      <p v-if="errorMessage" class="text-red-500 text-center mt-4">{{ errorMessage }}</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'

const email = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)

const auth = useAuthStore()
const router = useRouter()

const handleLogin = async () => {
  errorMessage.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    await auth.fetchProfile()
    router.push('/dashboard')
  } catch (error: any) {
    errorMessage.value = error.response?.data?.detail || 'Login failed. Please check your credentials.'
  } finally {
    loading.value = false
  }
}
</script>
