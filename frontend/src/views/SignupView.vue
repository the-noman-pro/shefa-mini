<script setup>
import { reactive, ref } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import AuthShell from '@/components/AuthShell.vue'
import Icon from '@/components/Icon.vue'
import { safeNext, useAuthForm } from '@/composables/useAuthForm'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const { fieldErrors, generalError, submitting, run } = useAuthForm()

const form = reactive({ name: '', email: '', password: '' })
const local = reactive({ name: '', email: '', password: '' })
const showPassword = ref(false)

function check() {
  local.name = form.name.trim().length >= 2 ? '' : 'Please enter your full name.'
  local.email = /^\S+@\S+\.\S+$/.test(form.email.trim()) ? '' : 'Enter a valid email address.'
  local.password =
    form.password.length < 8
      ? 'Use at least 8 characters.'
      : /^\d+$/.test(form.password)
        ? 'Use letters as well as numbers.'
        : ''
  return !local.name && !local.email && !local.password
}

function err(field) {
  return local[field] || fieldErrors[field] || ''
}

async function submit() {
  if (!check()) return
  const ok = await run(() =>
    auth.signup({ name: form.name.trim(), email: form.email.trim(), password: form.password }),
  )
  if (ok) router.replace(safeNext(route.query.next))
}
</script>

<template>
  <AuthShell
    title="Create your account"
    subtitle="Your wallet is ready the moment you sign up. Top up and give in minutes."
  >
    <form novalidate @submit.prevent="submit">
      <p v-if="generalError" class="alert alert-error" role="alert">
        <Icon name="alert" /> {{ generalError }}
      </p>
      <div class="field">
        <label class="field-label" for="su-name">Full name</label>
        <input
          id="su-name"
          v-model="form.name"
          class="input"
          autocomplete="name"
          :aria-invalid="err('name') ? 'true' : undefined"
          aria-describedby="su-name-error"
        />
        <p v-if="err('name')" id="su-name-error" class="field-error">{{ err('name') }}</p>
      </div>
      <div class="field">
        <label class="field-label" for="su-email">Email</label>
        <input
          id="su-email"
          v-model="form.email"
          class="input"
          type="email"
          autocomplete="email"
          :aria-invalid="err('email') ? 'true' : undefined"
          aria-describedby="su-email-error"
        />
        <p v-if="err('email')" id="su-email-error" class="field-error">{{ err('email') }}</p>
      </div>
      <div class="field">
        <label class="field-label" for="su-password">Password</label>
        <div class="pw">
          <input
            id="su-password"
            v-model="form.password"
            class="input"
            :type="showPassword ? 'text' : 'password'"
            autocomplete="new-password"
            :aria-invalid="err('password') ? 'true' : undefined"
            aria-describedby="su-password-hint su-password-error"
          />
          <button
            type="button"
            class="pw-toggle"
            :aria-label="showPassword ? 'Hide password' : 'Show password'"
            :aria-pressed="showPassword"
            @click="showPassword = !showPassword"
          >
            <Icon :name="showPassword ? 'eye-off' : 'eye'" :size="19" />
          </button>
        </div>
        <p id="su-password-hint" class="field-hint">
          At least 8 characters, not only numbers, not a common password.
        </p>
        <p v-if="err('password')" id="su-password-error" class="field-error">
          {{ err('password') }}
        </p>
      </div>
      <button type="submit" class="btn btn-block submit" :disabled="submitting">
        {{ submitting ? 'Creating your account…' : 'Create account' }}
      </button>
    </form>
    <template #below>
      Already have an account?
      <RouterLink :to="{ name: 'login', query: route.query }">Log in</RouterLink>
    </template>
  </AuthShell>
</template>

<style scoped>
.alert {
  margin-bottom: 16px;
}

.pw {
  position: relative;
}

.pw .input {
  padding-right: 52px;
}

.pw-toggle {
  position: absolute;
  right: 6px;
  top: 50%;
  transform: translateY(-50%);
  display: grid;
  place-items: center;
  width: 40px;
  height: 40px;
  border: 0;
  border-radius: 8px;
  background: none;
  color: var(--ink-soft);
  cursor: pointer;
}

.pw-toggle:hover {
  color: var(--ink);
  background: var(--paper-deep);
}

.submit {
  margin-top: 22px;
}
</style>
