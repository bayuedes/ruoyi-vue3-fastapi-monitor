import request from '@/utils/request'

// Q1: 监控设备总数
export function getDeviceCount() {
  return request({
    url: '/monitor/dashboard/deviceCount',
    method: 'get'
  })
}

// Q2: CPU 利用率 Top N 设备
export function getTopCpuDevices(limit = 10) {
  return request({
    url: '/monitor/dashboard/topCpu',
    method: 'get',
    params: { limit }
  })
}

// Q3: 指定 IP 资源最近 N 次 Ping 响应时间
export function getRecentPing(ip, limit = 10) {
  return request({
    url: '/monitor/dashboard/recentPing',
    method: 'get',
    params: { ip, limit }
  })
}
