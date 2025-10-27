<template>
  <div class="w-1/3 mx-auto mt-10">
    <el-card>
      <h2>Update Profile</h2>
      <el-form :model="form" @submit.prevent="onSubmit">
        <el-form-item label="Username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="Email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-button type="primary" @click="onSubmit">Save</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive, onMounted } from "vue";
import { useAuthStore } from "../stores/auth";
import axios from "axios";

const auth = useAuthStore();
const form = reactive({ username: "", email: "" });

onMounted(() => {
  if (auth.user) {
    form.username = auth.user.username;
    form.email = auth.user.email;
  }
});

const onSubmit = async () => {
  await axios.put("/api/account/update/", form, {
    headers: { Authorization: `Bearer ${auth.token}` },
  });
  await auth.fetchProfile();
};
</script>
