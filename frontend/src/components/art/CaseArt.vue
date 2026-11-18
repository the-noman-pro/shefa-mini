<script setup>
import Inked from './Inked.vue'

// Hand-drawn scene per case illustration key (see backend Illustration choices).
defineProps({
  name: { type: String, default: 'medical' },
  label: { type: String, default: '' },
})

const BLOB = 'M28 116C14 82 38 34 98 28c58-6 116 6 120 58 4 46-44 60-104 60-50 0-74-6-86-30Z'
</script>

<template>
  <svg
    viewBox="0 0 240 160"
    class="case-art"
    :class="`case-art--${name}`"
    :role="label ? 'img' : undefined"
    :aria-label="label || undefined"
    :aria-hidden="label ? undefined : 'true'"
    focusable="false"
  >
    <path :d="BLOB" class="blob" />
    <path d="M22 138c40-3 86 3 128-1 26-2 48 0 70-2" class="ln ground" />

    <!-- Medical: a heart with a pulse, a stethoscope and a bottle of medicine -->
    <g v-if="name === 'medical'">
      <path d="M62 40c-8 26-4 54 18 70" class="ln" />
      <path d="M50 38c4-6 18-6 22 0" class="ln" />
      <circle cx="82" cy="112" r="7" fill="var(--sky)" stroke="var(--ink)" stroke-width="2.4" />
      <Inked
        d="M124 120C96 102 78 86 80 64c2-16 20-22 32-14 6 4 10 10 12 14 2-4 6-10 12-14 12-8 30-2 32 14 2 22-16 38-44 56Z"
        fill="var(--clay)"
      />
      <path
        d="M90 80h16l6-12 8 26 8-20 6 8h22"
        fill="none"
        stroke="var(--paper)"
        stroke-width="3.2"
        stroke-linecap="round"
        stroke-linejoin="round"
      />
      <Inked d="M180 96h24v34a4 4 0 0 1-4 4h-16a4 4 0 0 1-4-4Z" fill="var(--sky)" />
      <Inked d="M178 86h28v10h-28Z" fill="var(--saffron)" />
      <path d="M186 108h12M192 102v12" class="ln" />
      <path d="M176 48l6 6M196 40v8M210 54l-7 4" class="ln spark" />
    </g>

    <!-- Education: a stack of books, a pencil and a school bag -->
    <g v-else-if="name === 'education'">
      <Inked d="M54 114l78-3 1 18-78 3Z" fill="var(--palm)" />
      <Inked d="M60 96l66 2-1 15-66-2Z" fill="var(--saffron)" />
      <Inked d="M68 80l52-3 1 17-52 3Z" fill="var(--rose)" />
      <path d="M62 120h56M66 102h46M76 86h34" class="ln thin" />
      <Inked d="M80 70l30-30 6 6-30 30-9 3Z" fill="var(--honey)" />
      <path d="M106 44l6 6" class="ln" />
      <Inked
        d="M148 72c0-10 8-14 20-14h14c12 0 20 4 20 14l2 54c0 6-4 8-10 8h-38c-6 0-10-2-10-8Z"
        fill="var(--clay)"
      />
      <path d="M162 58c0-12 24-12 24 0" class="ln" />
      <path d="M148 80c16 10 40 10 54 0" class="ln" />
      <Inked d="M160 100h30v20a4 4 0 0 1-4 4h-22a4 4 0 0 1-4-4Z" fill="var(--saffron-soft)" />
      <path d="M168 108h14" class="ln thin" />
    </g>

    <!-- Housing: a house under a new roof, a key and a rain cloud moving away -->
    <g v-else-if="name === 'housing'">
      <Inked d="M72 128V86l48-32 48 32v42Z" fill="var(--saffron-soft)" />
      <Inked d="M60 92l60-44 60 44-10 4-50-36-50 36Z" fill="var(--clay)" />
      <Inked d="M146 64V50h10v22" fill="var(--rose)" />
      <Inked d="M108 128v-26c0-8 24-8 24 0v26" fill="var(--palm)" />
      <Inked d="M82 98h18v16H82Z" fill="var(--sky)" />
      <Inked d="M140 98h18v16h-18Z" fill="var(--sky)" />
      <path d="M91 98v16M82 106h18M149 98v16M140 106h18" class="ln thin" />
      <circle cx="126" cy="116" r="1.8" fill="var(--paper)" />
      <Inked d="M196 82a9 9 0 1 1 0 .1Z" fill="var(--saffron)" :offset="2" />
      <path d="M196 91v34M196 114h8M196 122h6" class="ln" />
      <path
        d="M30 52c0-8 10-12 16-6 4-8 18-6 18 4 8 0 8 10 0 10H34c-6 0-8-6-4-8Z"
        class="ln cloud"
      />
      <path d="M38 70l-3 6M50 70l-3 6" class="ln thin" />
    </g>

    <!-- Food: a basket with bread, oil and dates, and a stalk of wheat -->
    <g v-else-if="name === 'food'">
      <path d="M50 128c4-24 8-44 18-60" class="ln" />
      <path
        d="M66 80c-6-2-8-8-6-12 6 0 8 6 6 12ZM62 92c-6-2-8-8-6-12 6 0 8 6 6 12ZM70 74c6-2 10-6 8-12-6 2-8 6-8 12ZM66 86c6-2 10-6 8-12-6 2-8 6-8 12Z"
        fill="var(--honey)"
        stroke="var(--ink)"
        stroke-width="1.8"
        stroke-linejoin="round"
      />
      <Inked d="M86 98c-2-18 34-24 40-4" fill="#d99a5b" />
      <path d="M96 90l4 6M106 86l3 7M116 87l2 6" class="ln thin" />
      <Inked d="M128 98V72l8-8v-8h10v8l8 8v26" fill="var(--palm-soft)" />
      <path d="M134 84h18" class="ln thin" />
      <Inked d="M76 98h112l-10 34c-1 4-4 6-8 6H94c-4 0-7-2-8-6Z" fill="var(--saffron)" />
      <path d="M84 108h96M88 120h88" class="ln thin" />
      <path d="M100 98l4 40M122 98l1 40M144 98l-1 40M166 98l-4 40" class="ln thin" />
      <path d="M90 98c4-44 80-44 86 0" class="ln" />
      <ellipse cx="164" cy="92" rx="7" ry="4.5" fill="var(--date)" transform="rotate(-24 164 92)" />
      <ellipse cx="176" cy="90" rx="7" ry="4.5" fill="var(--date)" transform="rotate(18 176 90)" />
      <path d="M200 60l6 4M206 76l8-1" class="ln spark" />
    </g>

    <!-- Water: a tap, a large drop and ripples -->
    <g v-else-if="name === 'water'">
      <Inked d="M34 64h46v14H50v20H36Z" fill="var(--line-strong)" />
      <Inked d="M52 54h12v10H52Z" fill="var(--clay)" />
      <path
        d="M43 106c-3 5 0 8 0 8s3-3 0-8ZM43 122c-3 5 0 8 0 8s3-3 0-8Z"
        fill="var(--sky)"
        stroke="var(--ink)"
        stroke-width="1.6"
      />
      <Inked
        d="M126 34s-34 40-34 64c0 18 14 30 34 30s34-12 34-30c0-24-34-64-34-64Z"
        fill="var(--sky)"
      />
      <path
        d="M108 100c0 10 6 16 14 18"
        fill="none"
        stroke="var(--paper)"
        stroke-width="3.5"
        stroke-linecap="round"
      />
      <path d="M86 140c18-6 62-6 80 0M100 148c10-3 42-3 52 0" class="ln thin" />
      <Inked d="M180 104h26l-3 26c0 3-2 4-4 4h-12c-2 0-4-1-4-4Z" fill="var(--surface)" />
      <path d="M182 114h22" fill="none" stroke="var(--sky)" stroke-width="5" />
      <path d="M188 70l4-8M202 76l8-4M196 56v-8" class="ln spark" />
    </g>

    <!-- Debt relief: a rent bill stamped paid, with a stack of coins -->
    <g v-else>
      <Inked
        d="M64 32h82l12 12v86l-8-5-8 5-8-5-8 5-8-5-8 5-8-5-8 5-8-5-8 5-8-5-6 4Z"
        fill="var(--surface)"
      />
      <path d="M146 32v12h12" class="ln thin" />
      <path d="M76 50h40M76 62h60M76 74h52M76 86h58M76 98h30" class="ln thin" />
      <path d="M112 112h30" class="ln" />
      <g transform="rotate(-14 118 84)">
        <Inked
          d="M90 70h56a6 6 0 0 1 6 6v18a6 6 0 0 1-6 6H90a6 6 0 0 1-6-6V76a6 6 0 0 1 6-6Z"
          fill="var(--palm-soft)"
          stroke="var(--palm)"
          :offset="1.5"
        />
        <path
          d="M98 89c-4-2.6-6-4.6-6-6.6a2.8 2.8 0 0 1 6-1.1 2.8 2.8 0 0 1 6 1.1c0 2-2 4-6 6.6Z"
          fill="var(--palm)"
        />
        <text x="110" y="90" class="stamp-text">PAID</text>
      </g>
      <Inked d="M170 124h36v10h-36Z" fill="var(--saffron)" :offset="2" />
      <Inked d="M172 114h32v10h-32Z" fill="var(--honey)" :offset="2" />
      <Inked d="M170 104h34v10h-34Z" fill="var(--saffron)" :offset="2" />
      <Inked d="M186 80a10 10 0 1 1 0 .1Z" fill="var(--honey)" :offset="2" />
      <path d="M182 80h8" class="ln thin" />
      <path d="M44 56l8 4M40 80h9M196 52l4-8M212 66l8-3" class="ln spark" />
    </g>
  </svg>
</template>

<style scoped>
.case-art {
  width: 100%;
  height: auto;
}

.blob {
  fill: var(--art-tint, var(--paper-deep));
}

.case-art--medical {
  --art-tint: var(--tint-medical);
}
.case-art--education {
  --art-tint: var(--tint-education);
}
.case-art--housing {
  --art-tint: var(--tint-housing);
}
.case-art--food {
  --art-tint: var(--tint-food);
}
.case-art--water {
  --art-tint: var(--tint-water);
}
.case-art--debt {
  --art-tint: var(--tint-debt);
}

.ln {
  fill: none;
  stroke: var(--ink);
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.thin {
  stroke-width: 1.6;
}

.ground {
  stroke-width: 2;
  opacity: 0.55;
}

.spark {
  stroke: var(--clay);
  stroke-width: 2.2;
}

.stamp-text {
  font-family: var(--font-body);
  font-weight: 800;
  font-size: 15px;
  letter-spacing: 0.12em;
  fill: var(--palm);
}

.cloud {
  stroke: var(--ink-muted);
  stroke-width: 2;
}
</style>
