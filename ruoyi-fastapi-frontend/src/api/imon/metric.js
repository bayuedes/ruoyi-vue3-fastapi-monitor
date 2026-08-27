import request from '@/utils/request'

// 查询指标列表
export function listMetric(query) {
  return request({
    url: '/monitor/index/list',
    method: 'get',
    params: query
  })
}

// 查询指标详情
export function getMetric(id) {
  return request({
    url: '/monitor/index/' + id,
    method: 'get'
  })
}

// 新增指标
export function addMetric(data) {
  return request({
    url: '/monitor/index',
    method: 'post',
    data
  })
}

// 修改指标
export function updateMetric(data) {
  return request({
    url: '/monitor/index',
    method: 'put',
    data
  })
}

// 删除指标
export function delMetric(id) {
  return request({
    url: '/monitor/index/' + id,
    method: 'delete'
  })
}
