const API_URL = import.meta.env.VITE_API_BASE_URL ?? '/api'

let csrfToken = ''

type RequestOptions = Omit<RequestInit, 'body'> & { body?: unknown }

type ValidationError = {
  loc?: Array<string | number>
  msg?: string
}

type ErrorResponse = {
  detail?: string | ValidationError[]
  message?: string
}

function formatErrorDetail(detail: ErrorResponse['detail']): string | undefined {
  if (typeof detail === 'string') return detail
  if (!Array.isArray(detail)) return undefined

  const messages = detail
    .map((item) => {
      if (!item.msg) return undefined
      const location = item.loc
        ?.filter((part) => part !== 'body')
        .join('.')
      return location ? `${location}: ${item.msg}` : item.msg
    })
    .filter((message): message is string => Boolean(message))

  return messages.length ? messages.join('\n') : undefined
}

async function request<T>(path: string, options: RequestOptions = {}): Promise<T> {
  const { body, ...requestOptions } = options
  const headers = new Headers(options.headers)
  headers.set('Content-Type', 'application/json')
  if (csrfToken && options.method && options.method !== 'GET') {
    headers.set('X-CSRF-Token', csrfToken)
  }
  const response = await fetch(`${API_URL}${path}`, {
    ...requestOptions,
    headers,
    credentials: 'include',
    body: body === undefined ? undefined : JSON.stringify(body),
  })
  if (!response.ok) {
    let data: ErrorResponse | undefined
    try {
      data = await response.json() as ErrorResponse
    } catch {
      data = undefined
    }

    const message = formatErrorDetail(data?.detail) ?? data?.message ?? `Request gagal (${response.status})`
    throw new Error(message)
  }
  if (response.status === 204) return undefined as T
  return response.json() as Promise<T>
}

export function setCsrfToken(token: string) {
  csrfToken = token
}

export const api = {
  get: <T>(path: string, params?: Record<string, string | number | undefined | null>) => {
    const query = params
      ? new URLSearchParams(Object.entries(params).filter((entry): entry is [string, string | number] => entry[1] !== undefined && entry[1] !== null && entry[1] !== '')).toString()
      : ''
    return request<T>(query ? `${path}?${query}` : path)
  },
  post: <T>(path: string, body?: unknown) => request<T>(path, { method: 'POST', body }),
  put: <T>(path: string, body?: unknown) => request<T>(path, { method: 'PUT', body }),
  delete: <T>(path: string) => request<T>(path, { method: 'DELETE' }),
}
