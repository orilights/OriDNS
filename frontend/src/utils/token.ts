export function getTokenExpTime(token: string): number {
  try {
    const payload = JSON.parse(window.atob(token.split('.')[0]))
    return payload.exp * 1000 - Date.now()
  }
  catch (err) {
    return 0
  }
}
