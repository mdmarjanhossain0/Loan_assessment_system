<template>
  <div class="font-sans text-gray-800 bg-white">
    <HeroSection />
    <FeaturesSection />
    <CalculatorPreview />
    <Testimonials />
  </div>
</template>

<script setup>
import HeroSection from '../components/home/HeroSection.vue'
import FeaturesSection from '../components/home/FeaturesSection.vue'
import CalculatorPreview from '../components/home/CalculatorPreview.vue'
import Testimonials from '../components/home/Testimonials.vue'
import FooterSection from '../components/home/FooterSection.vue'
</script>
