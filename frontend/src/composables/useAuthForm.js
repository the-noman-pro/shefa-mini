import { reactive, ref } from 'vue'

/** Field errors from the API plus one general message, for small auth forms. */
export function useAuthForm() {
  const fieldErrors = reactive({})
  const generalError = ref('')
  const submitting = ref(false)

  function reset() {
    for (const key of Object.keys(fieldErrors)) delete fieldErrors[key]
    generalError.value = ''
  }

  async function run(action) {
    reset()
    submitting.value = true
    try {
      await action()
      return true
    } catch (e) {
      Object.assign(fieldErrors, e.fields || {})
      if (!Object.keys(e.fields || {}).length || e.body?.non_field_errors || e.body?.detail) {
        generalError.value = e.message
      }
      return false
    } finally {
      submitting.value = false
    }
  }

  return { fieldErrors, generalError, submitting, run, reset }
}

/** Only follow in-app paths after login, never an outside URL. */
export function safeNext(value) {
  return typeof value === 'string' && value.startsWith('/') && !value.startsWith('//') ? value : '/'
}
