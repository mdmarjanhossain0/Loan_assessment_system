<template>
  <div class="max-w-3xl mx-auto mt-10 bg-white p-8 rounded-xl shadow-lg">
    <h2 class="text-3xl font-bold mb-6 text-center text-blue-700">
      Loan Application Form
    </h2>

    <form @submit.prevent="submitForm" class="space-y-6">
      <!-- Applicant Info (unchanged) -->
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

      <!-- Multiple Documents Upload -->
      <div class="space-y-4">
        <label class="block text-gray-700 mb-2">Upload Documents</label>
        <div
          v-for="(doc, index) in documents"
          :key="index"
          class="flex items-center gap-4"
        >
          <input type="file" @change="onFileChange($event, index)" class="border rounded-md p-2" />
          <select v-model="doc.type" class="input w-48">
            <option value="">Select Type</option>
            <option value="job_letter">Job Letter</option>
            <option value="payslip">Payslip</option>
            <option value="bank_statement">Bank Statement</option>
          </select>
          <button type="button" class="text-red-500" @click="removeDocument(index)">Remove</button>
        </div>
        <button type="button" class="text-blue-600 underline mt-2" @click="addDocument">Add Another Document</button>
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
import axios from "axios";

const API_URL = "/api/loan/applications/";
const DOCUMENTS_URL = "/api/loan/applications/upload_document/";

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
  document_ids: [], // to store uploaded document IDs
});

const documents = reactive([{ file: null, type: "" }]);
const errors = reactive({});

// Validation Schema
const schema = yup.object().shape({
  applicant_name: yup.string().required("Full name is required"),
  phone_number: yup.string().matches(/^[0-9+\-()\s]+$/, "Invalid phone number").required("Phone number is required"),
  email: yup.string().email("Invalid email").nullable(),
  type: yup.string().required("Please select a loan type"),
  loan_amount: yup.number().typeError("Loan amount must be a number").positive("Must be greater than 0").required("Loan amount is required"),
});

// Document handlers
const addDocument = () => documents.push({ file: null, type: "" });
const removeDocument = (index) => documents.splice(index, 1);
const onFileChange = (event, index) => { documents[index].file = event.target.files[0]; };

const submitForm = async () => {
  // Reset errors and messages
  Object.keys(errors).forEach((key) => (errors[key] = ""));
  loading.value = true;
  successMessage.value = "";

  try {
    // Validate the form
    await schema.validate(form, { abortEarly: false });

    // Upload documents one by one
    const uploadedIds = [];

    for (const doc of documents) {
      if (doc.file && doc.type) {
        const docFormData = new FormData();
        docFormData.append("file", doc.file);
        docFormData.append("document_type", doc.type);

        try {
          const docResponse = await axios.post(DOCUMENTS_URL, docFormData, {
            headers: { "Content-Type": "multipart/form-data" },
          });
          // Collect uploaded document IDs
          uploadedIds.push(docResponse.data.id);
        } catch (err) {
          console.error("Error uploading document:", err);
        }
      }
    }

    if (uploadedIds.length === 0) {
      console.error("No documents uploaded");
      return;
    }

    // Assign uploaded IDs to form.documents (array of ints)
    form.documents = [...uploadedIds];

    // Submit main application
    const response = await axios.post(API_URL, form, {
      headers: { "Content-Type": "application/json" },
    });

    console.log("Application submitted:", response.data);
    successMessage.value = "Application submitted successfully!";

    // Reset the form and documents
    Object.keys(form).forEach((key) => {
      if (key !== "documents") form[key] = "";
    });
    documents.splice(0, documents.length, { file: null, type: "" });
    form.documents = [];
  } catch (err) {
    // Handle validation errors
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

