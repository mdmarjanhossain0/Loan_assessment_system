<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useLoanStore } from "../stores/loan";

const loanStore = useLoanStore();
const loading = ref(false);
const error = ref("");
const currentPage = ref(1);

// Modal state
const showModal = ref(false);
const showEditModal = ref(false);

// Edit form state
const editForm = ref({
  id: null as number | null,
  applicant_name: "",
  email: "",
  phone_number: "",
  type: "",
  loan_amount: 0,
  monthly_income: 0,
  status: "Pending",
});

async function loadLoans(page = 1) {
  loading.value = true;
  error.value = "";
  try {
    await loanStore.fetchLoans(page);
    currentPage.value = page;
  } catch (err: any) {
    error.value = err.response?.data?.message || "Failed to fetch loans.";
  } finally {
    loading.value = false;
  }
}

async function viewLoanDetail(id: number) {
  try {
    await loanStore.getLoanDetail(id);
    showModal.value = true;
  } catch (err) {
    console.error("Failed to load loan detail:", err);
  }
}

function closeModal() {
  showModal.value = false;
}

function editLoan(id: number) {
  const loan = loanStore.loans.find((l: any) => l.id === id);
  if (loan) {
    editForm.value = { ...loan };
    showEditModal.value = true;
  }
}

function closeEditModal() {
  showEditModal.value = false;
}

async function saveEdit() {
  console.log("Edited loan data:", editForm.value);
  const data = editForm.value;
  await loanStore.updateLoan(data);
  showEditModal.value = false;
}

onMounted(() => {
  loadLoans();
});
</script>

<template>
  <div class="min-h-screen bg-gray-100 py-10 px-4">
    <div class="max-w-6xl mx-auto bg-white shadow rounded-lg p-6">
      <h2 class="text-2xl font-semibold mb-6 text-gray-800">My Loan Applications</h2>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-10 text-gray-500">Loading loans...</div>

      <!-- Error -->
      <div v-if="error" class="text-center py-4 text-red-500">{{ error }}</div>

      <!-- Loan Table -->
      <div v-if="!loading && loanStore.loans?.length">
        <div class="overflow-x-auto">
          <table class="min-w-full border border-gray-200 text-sm text-gray-700">
            <thead class="bg-gray-100">
              <tr>
                <th class="py-3 px-4 border-b text-left">#</th>
                <th class="py-3 px-4 border-b text-left">Applicant Name</th>
                <th class="py-3 px-4 border-b text-left">Email</th>
                <th class="py-3 px-4 border-b text-left">Phone</th>
                <th class="py-3 px-4 border-b text-left">Type</th>
                <th class="py-3 px-4 border-b text-right">Amount</th>
                <th class="py-3 px-4 border-b text-left">Status</th>
                <th class="py-3 px-4 border-b text-left">Created At</th>
                <th class="py-3 px-4 border-b text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr
                v-for="(loan, index) in loanStore.loans"
                :key="loan.id"
                class="hover:bg-gray-50"
              >
                <td class="py-2 px-4 border-b">{{ index + 1 + (currentPage - 1) * loanStore.loans.length }}</td>
                <td class="py-2 px-4 border-b font-medium">{{ loan.applicant_name }}</td>
                <td class="py-2 px-4 border-b">{{ loan.email }}</td>
                <td class="py-2 px-4 border-b">{{ loan.phone_number }}</td>
                <td class="py-2 px-4 border-b capitalize">{{ loan.type.replace('_', ' ') }}</td>
                <td class="py-2 px-4 border-b text-right">{{ loan.loan_amount.toLocaleString() }}</td>
                <td class="py-2 px-4 border-b">
                  <span
                    class="px-2 py-1 rounded text-xs font-semibold"
                    :class="{
                      'bg-yellow-100 text-yellow-700': loan.status === 'Pending',
                      'bg-green-100 text-green-700': loan.status === 'Approved',
                      'bg-red-100 text-red-700': loan.status === 'Rejected',
                    }"
                  >
                    {{ loan.status }}
                  </span>
                </td>
                <td class="py-2 px-4 border-b text-sm text-gray-500">{{ loan.created_at }}</td>
                <td class="py-2 px-4 border-b text-center">
                  <button
                    @click="viewLoanDetail(loan.id)"
                    class="px-3 py-1 bg-blue-500 text-white text-xs rounded hover:bg-blue-600 mr-2"
                  >
                    View
                  </button>
                  <button
                    @click="editLoan(loan.id)"
                    class="px-3 py-1 bg-yellow-400 text-white text-xs rounded hover:bg-yellow-500"
                  >
                    Edit
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Pagination -->
        <div class="flex justify-between items-center mt-6">
          <button
            :disabled="!loanStore.loans.previous"
            @click="loadLoans(currentPage - 1)"
            class="px-4 py-2 bg-gray-200 rounded disabled:opacity-50 hover:bg-gray-300"
          >
            Previous
          </button>
          <span class="text-gray-600 text-sm">Page {{ currentPage }}</span>
          <button
            :disabled="!loanStore.loans.next"
            @click="loadLoans(currentPage + 1)"
            class="px-4 py-2 bg-blue-600 text-white rounded disabled:opacity-50 hover:bg-blue-700"
          >
            Next
          </button>
        </div>
      </div>

      <!-- Empty -->
      <div v-else-if="!loading && !error" class="text-center text-gray-500 py-10">
        No loans found.
      </div>
    </div>

    <!-- Loan Detail Modal -->
    <transition name="fade" style="background-color: rgba(0, 0, 0, 0.5);">
      <div
        v-if="showModal"
        class="fixed inset-0 flex items-center justify-center z-50 p-4"
        
      >
        <div
          class="bg-white bg-opacity-90 backdrop-blur-md rounded-lg shadow-lg w-full max-w-2xl relative overflow-y-auto max-h-[90vh] p-6"
          style="background: white;"
        >
          <button
            @click="closeModal"
            class="absolute top-3 right-3 text-gray-500 hover:text-gray-700 text-xl"
          >
            ✕
          </button>
          <h3 class="text-xl font-semibold mb-4 text-gray-800">Loan Details</h3>

          <div v-if="loanStore.loanDetail" class="space-y-2 text-sm text-gray-700">
            <p><strong>Applicant:</strong> {{ loanStore.loanDetail.applicant_name }}</p>
            <p><strong>Email:</strong> {{ loanStore.loanDetail.email }}</p>
            <p><strong>Phone:</strong> {{ loanStore.loanDetail.phone_number }}</p>
            <p><strong>Type:</strong> {{ loanStore.loanDetail.type }}</p>
            <p><strong>Loan Amount:</strong> {{ loanStore.loanDetail.loan_amount.toLocaleString() }}</p>
            <p><strong>Monthly Income:</strong> {{ loanStore.loanDetail.monthly_income }}</p>
            <p><strong>Status:</strong> {{ loanStore.loanDetail.status }}</p>
            <p><strong>Created At:</strong> {{ loanStore.loanDetail.created_at }}</p>
            <br>
            <p><strong>DSR:</strong> {{ loanStore.loanDetail.dsr }}</p>

            <div v-if="loanStore.loanDetail.documents?.length" class="mt-4">
              <h4 class="font-semibold mb-2 text-gray-800">Documents</h4>
              <div class="space-y-3">
                <div
                  v-for="doc in loanStore.loanDetail.documents"
                  :key="doc.id"
                  class="border p-3 rounded bg-gray-50 bg-opacity-70"
                >
                  <p><strong>Type:</strong> {{ doc.document_type }}</p>
                  <p><strong>Uploaded:</strong> {{ doc.created_at }}</p>
                  <p><strong>File:</strong></p>
                  <a
                    :href="doc.file"
                    target="_blank"
                    class="text-blue-600 underline break-words"
                    >{{ doc.file }}</a
                  >

                  <div v-if="doc.parsed_data" class="mt-3">
                    <p class="font-medium text-gray-800">Summary:</p>
                    <pre
                      class="bg-white bg-opacity-80 border p-2 rounded text-xs overflow-auto whitespace-pre-wrap"
                      >GMI: {{ doc.parsed_data.gmi }}</pre
                    >
                    <pre
                      class="bg-white bg-opacity-80 border p-2 rounded text-xs overflow-auto whitespace-pre-wrap"
                      >EMO: {{ doc.parsed_data.emo }}</pre
                    >
                    <pre
                      class="bg-white bg-opacity-80 border p-2 rounded text-xs overflow-auto whitespace-pre-wrap"
                      >DSR: {{ doc.parsed_data.dsr }}</pre
                    >
                  </div>
                  


                  <div v-if="doc.file && doc.file.endsWith('.jpg')" class="mt-3">
                    <img
                      :src="doc.file"
                      alt="Document preview"
                      class="max-h-64 rounded border"
                    />
                  </div>

                  <!-- <div v-if="doc.extracted_text" class="mt-3">
                    <p class="font-medium text-gray-800">Extracted Text:</p>
                    <pre
                      class="bg-white bg-opacity-80 border p-2 rounded text-xs overflow-auto whitespace-pre-wrap"
                      >{{ doc.extracted_text }}</pre
                    >
                  </div> -->
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </transition>

    <!-- Edit Loan Modal -->
    <transition name="fade" style="background-color: rgba(0, 0, 0, 0.5);">
      <div
        v-if="showEditModal"
        class="fixed inset-0 bg-opacity-60 flex items-center justify-center z-50 p-4"
      >
        <div
          class="bg-white bg-opacity-95 backdrop-blur-md rounded-lg shadow-lg w-full max-w-2xl relative overflow-y-auto max-h-[90vh] p-6"
        >
          <button
            @click="closeEditModal"
            class="absolute top-3 right-3 text-gray-600 hover:text-gray-800 text-xl"
          >
            ✕
          </button>

          <h3 class="text-xl font-semibold mb-4 text-gray-800">Edit Loan</h3>

          <form @submit.prevent="saveEdit" class="space-y-3 text-sm text-gray-700">
            <div>
              <label class="block mb-1 font-medium">Applicant Name</label>
              <input v-model="editForm.applicant_name" type="text" class="w-full p-2 border rounded bg-gray-50" />
            </div>

            <div>
              <label class="block mb-1 font-medium">Email</label>
              <input v-model="editForm.email" type="email" class="w-full p-2 border rounded bg-gray-50" />
            </div>

            <div>
              <label class="block mb-1 font-medium">Phone</label>
              <input v-model="editForm.phone_number" type="text" class="w-full p-2 border rounded bg-gray-50" />
            </div>

            <div>
              <label class="block mb-1 font-medium">Type</label>
              <input v-model="editForm.type" type="text" class="w-full p-2 border rounded bg-gray-50" />
            </div>

            <div>
              <label class="block mb-1 font-medium">Loan Amount</label>
              <input v-model="editForm.loan_amount" type="number" class="w-full p-2 border rounded bg-gray-50" />
            </div>

            <div>
              <label class="block mb-1 font-medium">Monthly Income</label>
              <input v-model="editForm.monthly_income" type="number" class="w-full p-2 border rounded bg-gray-50" />
            </div>

            <div>
              <label class="block mb-1 font-medium">Status</label>
              <select v-model="editForm.status" class="w-full p-2 border rounded bg-gray-50">
                <option>Pending</option>
                <option>Approved</option>
                <option>Rejected</option>
              </select>
            </div>

            <div class="flex justify-end space-x-2 mt-4">
              <button
                type="button"
                @click="closeEditModal"
                class="px-4 py-2 bg-gray-300 rounded hover:bg-gray-400"
              >
                Cancel
              </button>
              <button
                type="submit"
                class="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
              >
                Save
              </button>
            </div>
          </form>
        </div>
      </div>
    </transition>
  </div>
</template>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.25s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
