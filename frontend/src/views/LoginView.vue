<script setup>
import { reactive } from 'vue'
import { RouterLink, useRoute, useRouter } from 'vue-router'
import AuthShell from '@/components/AuthShell.vue'
import Icon from '@/components/Icon.vue'
import { safeNext, useAuthForm } from '@/composables/useAuthForm'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const { fieldErrors, generalError, submitting, run } = useAuthForm()

const form = reactive({ email: '', password: '' })
const local = reactive({ email: '', password: '' })

function check() {
  local.email = /^\S+@\S+\.\S+$/.test(form.email.trim())
    ? ''
    : 'Enter the email you signed up with.'
  local.password = form.password ? '' : 'Enter your password.'
  return !local.email && !local.password
}

async function submit() {
  if (!check()) return
  const ok = await run(() => auth.login({ email: form.email.trim(), password: form.password }))
  if (ok) router.replace(safeNext(route.query.next))
}
</script>

<template>
  <AuthShell title="Welcome back" subtitle="Log in to give from your wallet and see your receipts.">
    <form novalidate @submit.prevent="submit">
      <p v-if="generalError" class="alert alert-error" role="alert">
        <Icon name="alert" /> {{ generalError }}
      </p>
      <div class="field">
        <label class="field-label" for="login-email">Email</label>
        <input
          id="login-email"
          v-model="form.email"
          class="input"
          type="email"
          autocomplete="email"
          :aria-invalid="local.email || fieldErrors.email ? 'true' : undefined"
          aria-describedby="login-email-error"
        />
        <p v-if="local.email || fieldErrors.email" id="login-email-error" class="field-error">
          {{ local.email || fieldErrors.email }}
        </p>
      </div>
      <div class="field">
        <label class="field-label" for="login-password">Password</label>
        <input
          id="login-password"
          v-model="form.password"
          class="input"
          type="password"
          autocomplete="current-password"
          :aria-invalid="local.password || fieldErrors.password ? 'true' : undefined"
          aria-describedby="login-password-error"
        />
        <p
          v-if="local.password || fieldErrors.password"
          id="login-password-error"
          class="field-error"
        >
          {{ local.password || fieldErrors.password }}
        </p>
      </div>
      <button type="submit" class="btn btn-block submit" :disabled="submitting">
        {{ submitting ? 'Logging in…' : 'Log in' }}
      </button>
    </form>
    <template #below>
      New to Shefa mini?
      <RouterLink :to="{ name: 'signup', query: route.query }">Create an account</RouterLink>
    </template>
  </AuthShell>
</template>

<style scoped>
.alert {
  margin-bottom: 16px;
}

.submit {
  margin-top: 22px;
}
</style>
