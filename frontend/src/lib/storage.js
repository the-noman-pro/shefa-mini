// localStorage can throw (private windows, blocked storage); the app must keep working without it.
export function readStorage(key) {
  try {
    return window.localStorage.getItem(key)
  } catch {
    return null
  }
}

export function writeStorage(key, value) {
  try {
    if (value === null || value === undefined) window.localStorage.removeItem(key)
    else window.localStorage.setItem(key, value)
  } catch {
    // ignore: the session simply will not survive a reload
  }
}
