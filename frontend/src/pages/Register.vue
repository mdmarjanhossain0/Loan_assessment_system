<template>
  <div class="w-1/3 mx-auto mt-10">
    <el-card>
      <h2>Register</h2>
      <el-form :model="form" @submit.prevent="onSubmit">
        <el-form-item label="Username">
          <el-input v-model="form.username" />
        </el-form-item>
        <el-form-item label="Email">
          <el-input v-model="form.email" />
        </el-form-item>
        <el-form-item label="Password">
          <el-input type="password" v-model="form.password" />
        </el-form-item>
        <el-button type="primary" @click="onSubmit">Register</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const form = reactive({ username: "", email: "", password: "" });
const router = useRouter();
const auth = useAuthStore();

const onSubmit = async () => {
  await auth.register(form);
  router.push("/login");
};
</script>
