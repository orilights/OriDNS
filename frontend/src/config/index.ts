export const appVersion = '0.0.1'

export const apiBaseUrl = 'http://localhost:3000'

export const providerConfig: {
  [provider: string]: {
    displayName: string
    bandageColor: string
    bandageTextColor: string
  }
} = {
  cloudflare: {
    displayName: 'Cloudflare',
    bandageColor: '#f38020',
    bandageTextColor: '#fff',
  },
  dnspod: {
    displayName: 'DNSPod',
    bandageColor: '#2a8bff',
    bandageTextColor: '#fff',
  },
}

export const RECORD_TYPES = [
  'A',
  'AAAA',
  'CNAME',
  'MX',
  'TXT',
]

export const RECORD_TYPES_SORT = [
  'NS',
  'CNAME',
  'A',
  'AAAA',
  'MX',
  'TXT',
]
