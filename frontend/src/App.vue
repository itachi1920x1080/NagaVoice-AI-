<template>
  <div class="min-h-screen bg-gray-50 text-gray-800 font-sans p-8">
    <div class="max-w-6xl mx-auto">
      
      <header class="flex justify-between items-center mb-8">
        <div>
          <h1 class="text-3xl font-bold text-indigo-600">📊 NagaVoice Dashboard</h1>
          <p class="text-gray-500 mt-1">ស្ថិតិប្រព័ន្ធ AI បំប្លែងសំឡេង Telegram</p>
        </div>
        <button @click="fetchAllData" class="bg-indigo-500 hover:bg-indigo-600 text-white px-4 py-2 rounded-lg shadow transition duration-200 flex items-center gap-2">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path></svg>
          Refresh
        </button>
      </header>

      <div v-if="isLoading" class="text-center py-20">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-indigo-600 mx-auto"></div>
        <p class="mt-4 text-gray-500 text-lg">កំពុងទាញយកទិន្នន័យ...</p>
      </div>

      <div v-else>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
          
          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex items-center gap-4">
            <div class="p-3 bg-blue-100 text-blue-600 rounded-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path></svg>
            </div>
            <div>
              <p class="text-sm text-gray-500 font-medium">អ្នកប្រើប្រាស់សរុប</p>
              <h2 class="text-3xl font-bold text-gray-800">{{ stats.total_users }}</h2>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex items-center gap-4">
            <div class="p-3 bg-purple-100 text-purple-600 rounded-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path></svg>
            </div>
            <div>
              <p class="text-sm text-gray-500 font-medium">ចំនួនបំប្លែងសរុប</p>
              <h2 class="text-3xl font-bold text-gray-800">{{ stats.total_transcriptions }}</h2>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex items-center gap-4">
            <div class="p-3 bg-green-100 text-green-600 rounded-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z"></path></svg>
            </div>
            <div>
              <p class="text-sm text-gray-500 font-medium">សារសំឡេង (Voice)</p>
              <h2 class="text-3xl font-bold text-gray-800">{{ stats.voice_count }}</h2>
            </div>
          </div>

          <div class="bg-white rounded-xl shadow-sm border border-gray-100 p-6 flex items-center gap-4">
            <div class="p-3 bg-red-100 text-red-600 rounded-lg">
              <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path></svg>
            </div>
            <div>
              <p class="text-sm text-gray-500 font-medium">សារវីដេអូ (Video)</p>
              <h2 class="text-3xl font-bold text-gray-800">{{ stats.video_count }}</h2>
            </div>
          </div>

        </div>

        <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
          <div class="px-6 py-5 border-b border-gray-100 bg-gray-50/50">
            <h3 class="text-lg font-semibold text-gray-800">📝 ប្រវត្តិនៃការបំប្លែងចុងក្រោយ</h3>
          </div>
          
          <div class="overflow-x-auto">
            <table class="w-full text-left border-collapse">
              <thead>
                <tr class="bg-gray-50 text-gray-500 text-sm uppercase tracking-wider">
                  <th class="px-6 py-4 font-medium">ID</th>
                  <th class="px-6 py-4 font-medium">អ្នកប្រើប្រាស់</th>
                  <th class="px-6 py-4 font-medium">ប្រភេទ</th>
                  <th class="px-6 py-4 font-medium">អត្ថបទដែលបានបំប្លែង</th>
                  <th class="px-6 py-4 font-medium text-right">កាលបរិច្ឆេទ</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-gray-100">
                <tr v-for="item in history" :key="item.id" class="hover:bg-gray-50/50 transition duration-150">
                  <td class="px-6 py-4 text-sm text-gray-500">#{{ item.id }}</td>
                  <td class="px-6 py-4 font-medium text-gray-800">{{ item.full_name }}</td>
                  <td class="px-6 py-4">
                    <span v-if="item.file_type === 'voice'" class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-green-100 text-green-700">
                      🎙️ Voice
                    </span>
                    <span v-else class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-red-100 text-red-700">
                      🎥 Video
                    </span>
                  </td>
                  <td class="px-6 py-4">
                    <p class="text-sm text-gray-600 line-clamp-2 max-w-md" :title="item.text">
                      {{ item.text }}
                    </p>
                  </td>
                  <td class="px-6 py-4 text-sm text-gray-500 text-right whitespace-nowrap">
                    {{ item.created_at }}
                  </td>
                </tr>
                
                <tr v-if="history.length === 0">
                  <td colspan="5" class="px-6 py-10 text-center text-gray-500">
                    មិនមានប្រវត្តិទិន្នន័យនៅឡើយទេ។
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <!-- Pipeline Simulator -->
        <div class="mt-10">
          <PipelineSimulator />
        </div>

      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import PipelineSimulator from './components/PipelineSimulator.vue';

const isLoading = ref(true);
const stats = ref({
  total_users: 0,
  total_transcriptions: 0,
  voice_count: 0,
  video_count: 0
});
const history = ref([]); // បង្កើតកន្លែងផ្ទុកទិន្នន័យតារាង

// មុខងារទាញយកទិន្នន័យពី API ទាំងពីរ
const fetchAllData = async () => {
  isLoading.value = true;
  try {
    // ទាញទិន្នន័យទាំងពីរក្នុងពេលតែមួយដោយប្រើ Promise.all ដើម្បឱ្យលឿន
    const [statsResponse, historyResponse] = await Promise.all([
      fetch('https://nagavoice-api.onrender.com/api/dashboard-stats'),
      fetch('https://nagavoice-api.onrender.com/api/dashboard-history')
    ]);

    if (statsResponse.ok) stats.value = await statsResponse.json();
    if (historyResponse.ok) history.value = await historyResponse.json();
    
  } catch (error) {
    console.error('Failed to fetch data:', error);
  } finally {
    isLoading.value = false;
  }
};

onMounted(() => {
  fetchAllData();
});
</script>

<style>
body {
  margin: 0;
  padding: 0;
}
/* Utility class សម្រាប់កាត់អត្ថបទវែងៗឱ្យមានចំណុច ៣ នៅខាងចុង */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;  
  overflow: hidden;
}
</style>