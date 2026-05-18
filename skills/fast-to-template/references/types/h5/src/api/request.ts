import axios, {
  type AxiosInstance,
  type AxiosRequestConfig,
  type InternalAxiosRequestConfig,
} from 'axios'
import type { ApiResponse, RequestConfig } from './types'

const DEFAULT_RETRY_COUNT = 2
const DEFAULT_RETRY_DELAY = 1000

function createRequest(): AxiosInstance {
  const instance = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL,
    timeout: 15000,
    headers: { 'Content-Type': 'application/json' },
  })

  let retryCount = 0

  instance.interceptors.request.use(
    (config: InternalAxiosRequestConfig) => {
      const token = localStorage.getItem('token')
      if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`
      }
      return config
    },
    (error) => Promise.reject(error),
  )

  instance.interceptors.response.use(
    (response) => {
      const data = response.data as ApiResponse
      if (data.code !== 0 && data.code !== 200) {
        return Promise.reject(data)
      }
      return response
    },
    (error) => {
      const config = error.config as AxiosRequestConfig & RequestConfig

      if (error.response?.status === 401) {
        localStorage.removeItem('token')
        window.location.href = '/login'
        return Promise.reject(error)
      }

      if (
        !error.response &&
        !config?.skipRetry &&
        retryCount < (config?.retryCount ?? DEFAULT_RETRY_COUNT)
      ) {
        retryCount++
        return new Promise((resolve) =>
          setTimeout(
            () => resolve(instance.request(config)),
            config?.retryDelay ?? DEFAULT_RETRY_DELAY,
          ),
        )
      }

      retryCount = 0
      return Promise.reject(error)
    },
  )

  return instance
}

export const request = createRequest()
