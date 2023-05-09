import { apiBaseUrl } from '@/config'

export function tokenVerify(token: string) {
  return fetch(`${apiBaseUrl}/verify`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export function tokenRefresh(token: string) {
  return fetch(`${apiBaseUrl}/refresh_token`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export function userLogin(username: string, password: string) {
  const formData = new FormData()
  formData.append('username', username)
  formData.append('password', password)
  return fetch(`${apiBaseUrl}/login`, {
    method: 'POST',
    body: formData,
  })
}

export function domainList(token: string, forceRefresh = false) {
  const query = forceRefresh ? '?force_refresh=1' : '?force_refresh=0'
  return fetch(`${apiBaseUrl}/domain/list${query}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export function domainInfoGet(token: string, domainId: string) {
  return fetch(`${apiBaseUrl}/domain/${domainId}/info`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export function recordList(token: string, domainId: string) {
  return fetch(`${apiBaseUrl}/domain/${domainId}/record/list`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}

export function recordCreate(token: string, domainId: string, data: FormData) {
  return fetch(`${apiBaseUrl}/domain/${domainId}/record/create`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: data,
  })
}

export function recordUpdate(token: string, domainId: string, recordId: string, data: FormData) {
  return fetch(`${apiBaseUrl}/domain/${domainId}/record/${recordId}/update`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${token}`,
    },
    body: data,
  })
}

export function recordDelete(token: string, domainId: string, recordId: string) {
  return fetch(`${apiBaseUrl}/domain/${domainId}/record/${recordId}/delete`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })
}
