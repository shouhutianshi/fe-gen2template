export interface ApiResponse<T = unknown> {
  code: number
  data: T
  message: string
}

export interface ApiError {
  code: number
  message: string
  details?: unknown
}

export interface RequestConfig {
  skipErrorHandler?: boolean
  skipRetry?: boolean
  retryCount?: number
  retryDelay?: number
}
