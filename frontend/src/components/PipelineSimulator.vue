<template>
  <div class="bg-white rounded-xl shadow-sm border border-gray-100 overflow-hidden">
    <div class="px-6 py-5 border-b border-gray-100 bg-gradient-to-r from-indigo-50 to-purple-50">
      <h3 class="text-lg font-semibold text-gray-800">🛠️ Pipeline Simulator — ពិសោធន៍ប៉ារ៉ាម៉ែត្រ STT</h3>
      <p class="text-sm text-gray-500 mt-1">សាកល្បងផ្លាស់ប្តូរតម្លៃដើម្បីមើលផលប៉ះពាល់ដល់ល្បឿន និងភាពត្រឹមត្រូវ</p>
    </div>

    <div class="p-6 space-y-8">

      <!-- Pipeline Flow Visualization -->
      <div class="relative">
        <div class="flex items-center justify-between gap-2">
          <!-- Stage 1: VAD -->
          <div 
            class="flex-1 rounded-xl p-4 border-2 transition-all duration-500 cursor-default"
            :class="vadFilter ? 'border-emerald-400 bg-emerald-50 shadow-lg shadow-emerald-100' : 'border-gray-200 bg-gray-50 opacity-60'"
          >
            <div class="flex items-center gap-2 mb-2">
              <span class="text-2xl">🔊</span>
              <span class="font-semibold text-sm" :class="vadFilter ? 'text-emerald-700' : 'text-gray-400'">Step 1</span>
            </div>
            <h4 class="font-bold text-sm" :class="vadFilter ? 'text-emerald-800' : 'text-gray-500'">VAD Filter</h4>
            <p class="text-xs mt-1" :class="vadFilter ? 'text-emerald-600' : 'text-gray-400'">ត្រងសំឡេងរំខាន</p>
            <div v-if="isSimulating && currentStage >= 1" class="mt-2">
              <div class="h-1.5 bg-emerald-200 rounded-full overflow-hidden">
                <div class="h-full bg-emerald-500 rounded-full animate-pulse" :style="{ width: currentStage > 1 ? '100%' : '60%' }"></div>
              </div>
            </div>
          </div>

          <!-- Arrow 1 -->
          <div class="flex-shrink-0">
            <svg class="w-6 h-6 transition-colors duration-300" :class="isSimulating && currentStage >= 2 ? 'text-indigo-500' : 'text-gray-300'" fill="currentColor" viewBox="0 0 24 24"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"/></svg>
          </div>

          <!-- Stage 2: Mel Spectrogram -->
          <div 
            class="flex-1 rounded-xl p-4 border-2 transition-all duration-500 cursor-default"
            :class="isSimulating && currentStage >= 2 ? 'border-blue-400 bg-blue-50 shadow-lg shadow-blue-100' : 'border-gray-200 bg-gray-50'"
          >
            <div class="flex items-center gap-2 mb-2">
              <span class="text-2xl">📊</span>
              <span class="font-semibold text-sm" :class="isSimulating && currentStage >= 2 ? 'text-blue-700' : 'text-gray-400'">Step 2</span>
            </div>
            <h4 class="font-bold text-sm" :class="isSimulating && currentStage >= 2 ? 'text-blue-800' : 'text-gray-500'">Mel Spectrogram</h4>
            <p class="text-xs mt-1" :class="isSimulating && currentStage >= 2 ? 'text-blue-600' : 'text-gray-400'">បំប្លែងជាក្រាហ្វិក</p>
            <div v-if="isSimulating && currentStage >= 2" class="mt-2">
              <div class="h-1.5 bg-blue-200 rounded-full overflow-hidden">
                <div class="h-full bg-blue-500 rounded-full animate-pulse" :style="{ width: currentStage > 2 ? '100%' : '50%' }"></div>
              </div>
            </div>
          </div>

          <!-- Arrow 2 -->
          <div class="flex-shrink-0">
            <svg class="w-6 h-6 transition-colors duration-300" :class="isSimulating && currentStage >= 3 ? 'text-indigo-500' : 'text-gray-300'" fill="currentColor" viewBox="0 0 24 24"><path d="M12 4l-1.41 1.41L16.17 11H4v2h12.17l-5.58 5.59L12 20l8-8z"/></svg>
          </div>

          <!-- Stage 3: Transformer -->
          <div 
            class="flex-1 rounded-xl p-4 border-2 transition-all duration-500 cursor-default"
            :class="isSimulating && currentStage >= 3 ? 'border-purple-400 bg-purple-50 shadow-lg shadow-purple-100' : 'border-gray-200 bg-gray-50'"
          >
            <div class="flex items-center gap-2 mb-2">
              <span class="text-2xl">🧠</span>
              <span class="font-semibold text-sm" :class="isSimulating && currentStage >= 3 ? 'text-purple-700' : 'text-gray-400'">Step 3</span>
            </div>
            <h4 class="font-bold text-sm" :class="isSimulating && currentStage >= 3 ? 'text-purple-800' : 'text-gray-500'">Transformer</h4>
            <p class="text-xs mt-1" :class="isSimulating && currentStage >= 3 ? 'text-purple-600' : 'text-gray-400'">Encoder → Decoder</p>
            <div v-if="isSimulating && currentStage >= 3" class="mt-2">
              <div class="h-1.5 bg-purple-200 rounded-full overflow-hidden">
                <div class="h-full bg-purple-500 rounded-full animate-pulse" :style="{ width: currentStage > 3 ? '100%' : '40%' }"></div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Parameter Controls -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6">

        <!-- Beam Size -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <label class="text-sm font-semibold text-gray-700">🔍 Beam Size</label>
            <span class="text-lg font-bold text-indigo-600 bg-indigo-50 px-3 py-0.5 rounded-lg">{{ beamSize }}</span>
          </div>
          <input 
            type="range" 
            v-model.number="beamSize" 
            min="1" max="10" step="1"
            class="w-full h-2 bg-indigo-100 rounded-full appearance-none cursor-pointer accent-indigo-500"
          />
          <div class="flex justify-between text-xs text-gray-400">
            <span>១ (លឿន)</span>
            <span>១០ (ត្រឹមត្រូវ)</span>
          </div>
          <p class="text-xs text-gray-500 leading-relaxed bg-gray-50 rounded-lg p-3">
            <strong>Beam Search</strong> គឺជាចំនួនផ្លូវដែល AI ព្យាយាមដើរស្វែងរកក្នុងពេលតែមួយ។ 
            បើតម្លៃ <strong>ខ្ពស់</strong> = ត្រឹមត្រូវជាង ប៉ុន្តែយឺត។ 
            បើតម្លៃ <strong>ទាប</strong> = រហ័សជាង ប៉ុន្តែអាចមានកំហុស។
          </p>
        </div>

        <!-- Temperature -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <label class="text-sm font-semibold text-gray-700">🌡️ Temperature</label>
            <span class="text-lg font-bold px-3 py-0.5 rounded-lg" :class="tempColorClass">{{ temperature.toFixed(1) }}</span>
          </div>
          <input 
            type="range" 
            v-model.number="temperature" 
            min="0" max="1" step="0.1"
            class="w-full h-2 bg-orange-100 rounded-full appearance-none cursor-pointer accent-orange-500"
          />
          <div class="flex justify-between text-xs text-gray-400">
            <span>0.0 (ច្បាស់លាស់)</span>
            <span>1.0 (ច្នៃប្រឌិត)</span>
          </div>
          <p class="text-xs text-gray-500 leading-relaxed bg-gray-50 rounded-lg p-3">
            <strong>Temperature</strong> គ្រប់គ្រងភាពចៃដន្យនៃការទាយពាក្យ។ 
            <strong>0.0</strong> = ប្រើពាក្យដែលប្រាកដបំផុត។ 
            <strong>1.0</strong> = អាចទាយពាក្យថ្មីប៉ុន្តែអាចខុស។
          </p>
        </div>

        <!-- VAD Filter -->
        <div class="space-y-3">
          <div class="flex items-center justify-between">
            <label class="text-sm font-semibold text-gray-700">🔇 VAD Filter</label>
            <button 
              @click="vadFilter = !vadFilter"
              class="relative inline-flex h-7 w-14 items-center rounded-full transition-colors duration-300 focus:outline-none"
              :class="vadFilter ? 'bg-emerald-500' : 'bg-gray-300'"
            >
              <span 
                class="inline-block h-5 w-5 transform rounded-full bg-white shadow-md transition-transform duration-300"
                :class="vadFilter ? 'translate-x-8' : 'translate-x-1'"
              ></span>
            </button>
          </div>
          <div class="text-center py-2">
            <span 
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-sm font-medium transition-all duration-300"
              :class="vadFilter ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'"
            >
              {{ vadFilter ? '✅ បើក (កាត់សំឡេងរំខាន)' : '❌ បិទ (រក្សាសំឡេងទាំងអស់)' }}
            </span>
          </div>
          <p class="text-xs text-gray-500 leading-relaxed bg-gray-50 rounded-lg p-3">
            <strong>Voice Activity Detection</strong> កាត់ចោលផ្នែកស្ងាត់ ឬសំឡេងរំខាន។
            បើក = បំប្លែង<strong>លឿន</strong>ជាង និង<strong>ត្រឹមត្រូវ</strong>ជាង។
          </p>
        </div>

      </div>

      <!-- Estimated Performance Metrics -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
        <div class="bg-gradient-to-br from-blue-50 to-indigo-50 rounded-xl p-4 text-center border border-blue-100">
          <p class="text-xs text-blue-500 font-medium mb-1">⏱️ ល្បឿនប៉ាន់ស្មាន</p>
          <p class="text-xl font-bold text-blue-700">{{ estimatedSpeed }}</p>
        </div>
        <div class="bg-gradient-to-br from-emerald-50 to-green-50 rounded-xl p-4 text-center border border-emerald-100">
          <p class="text-xs text-emerald-500 font-medium mb-1">🎯 ភាពត្រឹមត្រូវ</p>
          <p class="text-xl font-bold text-emerald-700">{{ estimatedAccuracy }}%</p>
        </div>
        <div class="bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl p-4 text-center border border-amber-100">
          <p class="text-xs text-amber-500 font-medium mb-1">💾 Memory (RAM)</p>
          <p class="text-xl font-bold text-amber-700">{{ estimatedMemory }}</p>
        </div>
        <div class="bg-gradient-to-br from-purple-50 to-pink-50 rounded-xl p-4 text-center border border-purple-100">
          <p class="text-xs text-purple-500 font-medium mb-1">🔄 ផ្លូវ Beam</p>
          <p class="text-xl font-bold text-purple-700">{{ beamSize }} ផ្លូវ</p>
        </div>
      </div>

      <!-- Simulate Button + Output -->
      <div class="flex flex-col items-center gap-4">
        <button 
          @click="runSimulation"
          :disabled="isSimulating"
          class="px-8 py-3 rounded-xl font-semibold text-white shadow-lg transition-all duration-300 flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
          :class="isSimulating ? 'bg-gray-400' : 'bg-gradient-to-r from-indigo-500 to-purple-600 hover:from-indigo-600 hover:to-purple-700 hover:shadow-xl hover:-translate-y-0.5'"
        >
          <svg v-if="isSimulating" class="w-5 h-5 animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
          </svg>
          <span v-if="isSimulating">កំពុងដំណើរការ... (Stage {{ currentStage }}/3)</span>
          <span v-else>▶️ ដំណើរការ Pipeline Simulation</span>
        </button>

        <!-- Simulation Output -->
        <div v-if="simulationResult" class="w-full bg-gray-900 rounded-xl p-5 font-mono text-sm space-y-1 overflow-x-auto">
          <p class="text-gray-400">$ whisper_pipeline.run()</p>
          <p class="text-emerald-400">✓ VAD Filter: {{ vadFilter ? 'ENABLED — ត្រង់សំឡេងរំខានរួច' : 'DISABLED — រក្សាសំឡេងទាំងអស់' }}</p>
          <p class="text-blue-400">✓ Mel Spectrogram: បំប្លែង {{ vadFilter ? '3.2s' : '5.0s' }} audio → 80-dim features</p>
          <p class="text-purple-400">✓ Transformer Decode: beam_size={{ beamSize }}, temp={{ temperature.toFixed(1) }}</p>
          <p class="text-yellow-400 mt-2">📝 Output: "{{ simulatedOutput }}"</p>
          <p class="text-gray-500 mt-1">⏱️ Simulated time: {{ simulatedTime }}ms | Accuracy: {{ estimatedAccuracy }}%</p>
        </div>
      </div>

      <!-- Code Preview -->
      <div class="bg-gray-900 rounded-xl overflow-hidden">
        <div class="flex items-center gap-2 px-4 py-3 bg-gray-800">
          <div class="w-3 h-3 rounded-full bg-red-500"></div>
          <div class="w-3 h-3 rounded-full bg-yellow-500"></div>
          <div class="w-3 h-3 rounded-full bg-green-500"></div>
          <span class="ml-2 text-xs text-gray-400 font-mono">transcription.py — ការកំណត់បច្ចុប្បន្ន</span>
        </div>
        <pre class="p-5 text-sm font-mono text-gray-300 overflow-x-auto leading-relaxed"><code><span class="text-purple-400">from</span> <span class="text-blue-300">faster_whisper</span> <span class="text-purple-400">import</span> <span class="text-yellow-300">WhisperModel</span>

<span class="text-gray-500"># ទាញយកម៉ូដែលមកទុកក្នុង Memory</span>
model = <span class="text-yellow-300">WhisperModel</span>(<span class="text-emerald-300">"medium"</span>, device=<span class="text-emerald-300">"cuda"</span>)

segments, info = model.<span class="text-blue-300">transcribe</span>(
    <span class="text-emerald-300">"audio.ogg"</span>,
    beam_size=<span class="text-orange-300">{{ beamSize }}</span>,          <span class="text-gray-500"># ← ផ្លាស់ប្តូរខាងលើ</span>
    temperature=<span class="text-orange-300">{{ temperature.toFixed(1) }}</span>,      <span class="text-gray-500"># ← ផ្លាស់ប្តូរខាងលើ</span>
    vad_filter=<span class="text-orange-300">{{ vadFilter }}</span>       <span class="text-gray-500"># ← ផ្លាស់ប្តូរខាងលើ</span>
)</code></pre>
      </div>

    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue';

const beamSize = ref(5);
const temperature = ref(0.0);
const vadFilter = ref(true);
const isSimulating = ref(false);
const currentStage = ref(0);
const simulationResult = ref(false);

const tempColorClass = computed(() => {
  if (temperature.value <= 0.3) return 'text-blue-600 bg-blue-50';
  if (temperature.value <= 0.6) return 'text-orange-600 bg-orange-50';
  return 'text-red-600 bg-red-50';
});

const estimatedSpeed = computed(() => {
  let base = 1.0;
  base += (beamSize.value - 1) * 0.15;
  if (!vadFilter.value) base += 0.5;
  if (base < 1.0) return 'វេគមាន';
  if (base < 1.5) return 'លឿន';
  if (base < 2.0) return 'មធ្យម';
  return 'យឺត';
});

const estimatedAccuracy = computed(() => {
  let accuracy = 85;
  accuracy += Math.min(beamSize.value * 1.2, 12);
  if (temperature.value > 0.5) accuracy -= temperature.value * 8;
  if (vadFilter.value) accuracy += 2;
  return Math.min(99, Math.max(60, Math.round(accuracy)));
});

const estimatedMemory = computed(() => {
  let mem = 2.5;
  mem += beamSize.value * 0.1;
  return mem.toFixed(1) + ' GB';
});

const sampleOutputs = [
  'សួស្តី តើអ្នកសុខសប្បាយជាទេ?',
  'ថ្ងៃនេះអាកាសធាតុល្អណាស់។',
  'ខ្ញុំចង់រៀនភាសា Python។',
  'តើកម្ពុជាមានខេត្តប៉ុន្មាន?',
];

const simulatedOutput = ref('');
const simulatedTime = ref(0);

const runSimulation = async () => {
  isSimulating.value = true;
  simulationResult.value = false;
  currentStage.value = 0;

  // Stage 1: VAD
  currentStage.value = 1;
  await delay(vadFilter.value ? 800 : 400);

  // Stage 2: Mel Spectrogram
  currentStage.value = 2;
  await delay(1000);

  // Stage 3: Transformer
  currentStage.value = 3;
  await delay(600 + beamSize.value * 150);

  // Complete
  currentStage.value = 4;
  simulatedOutput.value = sampleOutputs[Math.floor(Math.random() * sampleOutputs.length)];
  simulatedTime.value = Math.round(800 + beamSize.value * 120 + (vadFilter.value ? 0 : 400) + temperature.value * 200);
  simulationResult.value = true;
  
  await delay(500);
  isSimulating.value = false;
  currentStage.value = 0;
};

const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));
</script>
