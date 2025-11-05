<template>
  <div class="max-w-3xl mx-auto mt-10 bg-white p-8 rounded-xl shadow-lg">
    <h2 class="text-3xl font-bold mb-6 text-center text-blue-700">
      Loan Application Form
    </h2>

    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- Applicant Info -->
      <div class="grid md:grid-cols-2 gap-6">
        <div>
          <label class="block text-gray-700 mb-2">Full Name</label>
          <input v-model="form.applicant_name" type="text" class="input" placeholder="Enter your full name" />
          <p v-if="errors.applicant_name" class="text-red-500 text-sm mt-1">{{ errors.applicant_name }}</p>
        </div>
        <div>
          <label class="block text-gray-700 mb-2">Phone Number</label>
          <input v-model="form.phone_number" type="text" class="input" placeholder="Enter your phone number" />
          <p v-if="errors.phone_number" class="text-red-500 text-sm mt-1">{{ errors.phone_number }}</p>
        </div>
      </div>

      <div class="grid md:grid-cols-2 gap-6">
        <div>
          <label class="block text-gray-700 mb-2">Email</label>
          <input v-model="form.email" type="email" class="input" placeholder="example@mail.com" />
          <p v-if="errors.email" class="text-red-500 text-sm mt-1">{{ errors.email }}</p>
        </div>
        <div>
          <label class="block text-gray-700 mb-2">Loan Type</label>
          <select v-model="form.type" class="input">
            <option value="">Select Loan Type</option>
            <option value="home_lone">Home Loan</option>
            <option value="car_lone">Car Loan</option>
            <option value="sme_lone">SME Loan</option>
            <option value="personal_lone">Personal Loan</option>
          </select>
          <p v-if="errors.type" class="text-red-500 text-sm mt-1">{{ errors.type }}</p>
        </div>
      </div>

      <!-- Financial Details -->
      <div class="grid md:grid-cols-2 gap-6">
        <div>
          <label class="block text-gray-700 mb-2">Loan Amount</label>
          <input v-model="form.loan_amount" type="number" class="input" placeholder="Loan amount" />
          <p v-if="errors.loan_amount" class="text-red-500 text-sm mt-1">{{ errors.loan_amount }}</p>
        </div>

        <div>
          <label class="block text-gray-700 mb-2">Monthly Income</label>
          <input v-model="form.monthly_income" type="number" class="input" placeholder="Monthly income" />
        </div>

        <div>
          <label class="block text-gray-700 mb-2">Total Monthly Debt</label>
          <input v-model="form.total_monthly_debt" type="number" class="input" placeholder="Monthly debt (optional)" />
        </div>
      </div>

      <!-- Credit Summary -->
      <div>
        <label class="block text-gray-700 mb-2">Credit Summary</label>
        <textarea v-model="form.credit_summary" rows="3" class="input" placeholder="Describe your financial background (optional)"></textarea>
      </div>

      <!-- Single Document Upload -->
      <div class="space-y-4">
        <label class="block text-gray-700 mb-2">Upload Document</label>
        <input type="file" @change="onFileChange" class="border rounded-md p-2 w-full" />
      </div>

      <!-- Submit Button -->
      <div class="text-center mt-8">
        <button
          type="submit"
          :disabled="loading"
          class="bg-gradient-to-r from-blue-700 to-indigo-700 text-white px-8 py-3 rounded-full font-semibold hover:from-blue-600 hover:to-indigo-600 transition transform hover:scale-105 shadow-lg disabled:opacity-50"
        >
          {{ loading ? "Submitting..." : "Submit Application" }}
        </button>
      </div>

      <!-- Success Message -->
      <p v-if="successMessage" class="text-green-600 text-center mt-4 font-medium">{{ successMessage }}</p>
    </form>
  </div>
</template>

<script setup>
import { reactive, ref } from "vue";
import * as yup from "yup";
import api from "../utils/axios";

const API_URL = "loan/applications/";

const loading = ref(false);
const successMessage = ref("");

const form = reactive({
  applicant_name: "",
  phone_number: "",
  email: "",
  type: "",
  loan_amount: "",
  monthly_income: "",
  total_monthly_debt: "",
  credit_summary: "",
});

const file = ref(null);
const errors = reactive({});

// Validation Schema
const schema = yup.object().shape({
  applicant_name: yup.string().required("Full name is required"),
  phone_number: yup.string().matches(/^[0-9+\-()\s]+$/, "Invalid phone number").required("Phone number is required"),
  email: yup.string().email("Invalid email").nullable(),
  type: yup.string().required("Please select a loan type"),
  loan_amount: yup.number().typeError("Loan amount must be a number").positive("Must be greater than 0").required("Loan amount is required"),
});

// File handler
const onFileChange = (event) => {
  file.value = event.target.files[0];
};

const submitForm = async () => {
  // Reset errors and messages
  Object.keys(errors).forEach((key) => (errors[key] = ""));
  successMessage.value = "";
  loading.value = true;

  try {
    // Validate form
    await schema.validate(form, { abortEarly: false });

    if (!file.value) {
      alert("Please upload a document file");
      loading.value = false;
      return;
    }

    // Prepare FormData with file and form fields
    const formData = new FormData();
    Object.keys(form).forEach((key) => formData.append(key, form[key]));
    formData.append("file", file.value);

    const response = await api.post(API_URL, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    console.log("Application submitted:", response.data);
    successMessage.value = "Application submitted successfully!";

    // Reset form
    Object.keys(form).forEach((key) => (form[key] = ""));
    file.value = null;
  } catch (err) {
    if (err.inner) {
      err.inner.forEach((e) => (errors[e.path] = e.message));
    } else {
      console.error(err);
    }
  } finally {
    loading.value = false;
  }
};
</script>
