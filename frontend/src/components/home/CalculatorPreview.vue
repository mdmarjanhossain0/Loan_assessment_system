<template>
  <section class="py-16 px-6 text-center">
    <h2 class="text-3xl font-bold mb-8">Estimate Your Loan</h2>
    <div class="bg-white shadow-lg rounded-2xl p-8 max-w-md mx-auto">
      <label class="block text-left mb-2 font-semibold">Loan Amount ($)</label>
      <input type="number" class="w-full border rounded-lg p-3 mb-4" placeholder="Enter amount" />
      
      <label class="block text-left mb-2 font-semibold">Duration (months)</label>
      <input type="number" class="w-full border rounded-lg p-3 mb-4" placeholder="Enter duration" />

      <button class="bg-blue-700 text-white w-full py-3 rounded-lg hover:bg-blue-800 transition">
        Calculate
      </button>
    </div>
  </section>
</template>
