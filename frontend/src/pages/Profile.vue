<template>
  <div class="max-w-2xl mx-auto mt-10">
    <el-card>
      <h2>My Profile</h2>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="Username">{{ auth.user?.username }}</el-descriptions-item>
        <el-descriptions-item label="Email">{{ auth.user?.email }}</el-descriptions-item>
        <el-descriptions-item label="Role">{{ auth.user?.role }}</el-descriptions-item>
      </el-descriptions>
      <el-button type="primary" class="mt-4" @click="$router.push('/profile/update')">
        Edit Profile
      </el-button>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted } from "vue";
import { useAuthStore } from "../stores/auth";
const auth = useAuthStore();

onMounted(() => {
  if (!auth.user) auth.fetchProfile();
});
</script>
