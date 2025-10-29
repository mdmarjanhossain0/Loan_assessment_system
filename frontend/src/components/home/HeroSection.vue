<template>
  <section
    class="relative flex flex-col items-center justify-center min-h-[70vh] bg-gradient-to-r from-blue-700 via-indigo-700 to-purple-800 text-white overflow-hidden">

    <!-- Subtle background circles -->
    <div class="absolute top-0 left-0 w-56 h-56 bg-blue-500 rounded-full mix-blend-multiply filter blur-3xl opacity-25 animate-pulse"></div>
    <div class="absolute bottom-0 right-0 w-72 h-72 bg-indigo-400 rounded-full mix-blend-multiply filter blur-3xl opacity-25 animate-pulse"></div>

    <!-- Main content -->
    <div class="relative z-10 text-center px-6 py-10">
      <h1 class="text-4xl md:text-5xl font-extrabold mb-4">
        Get the <span class="text-yellow-300">Loan</span> You Deserve
      </h1>
      <p class="text-base md:text-lg max-w-xl mx-auto text-gray-100 mb-8">
        Fast approvals, flexible repayments, and competitive interest rates — your financial freedom starts here.
      </p>

      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <!-- Primary Button -->
        <button
          class="bg-yellow-400 text-blue-900 font-semibold px-8 py-3 rounded-full hover:bg-yellow-300 transition transform hover:scale-105 shadow-md" @click="toLoanApplication">
          Apply Now
        </button>

        <!-- Secondary Button -->
        <button
          class="bg-white text-indigo-700 font-semibold px-8 py-3 rounded-full hover:bg-gray-100 transition transform hover:scale-105 shadow-md">
          Learn More
        </button>
      </div>
    </div>

    <!-- Gradient overlay -->
    <div class="absolute inset-0 bg-gradient-to-t from-black/30 to-transparent"></div>
  </section>
</template>


<script setup>
import { useRouter } from 'vue-router'

const router = useRouter();

function toLoanApplication() {
  console.log("toLoanApplication")
  router.push("/loan/apply")
}
</script>