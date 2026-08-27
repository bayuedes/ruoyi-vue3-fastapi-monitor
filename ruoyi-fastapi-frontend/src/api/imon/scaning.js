import request from '@/utils/request'

// 查询子资源实例列表
export function listScaning(query) {
  return request({
    url: '/monitor/scaning/list',
    method: 'get',
    params: query
  })
}

// 查询子资源实例详情
export function getScaning(id) {
  return request({
    url: '/monitor/scaning/' + id,
    method: 'get'
  })
}

// 新增子资源实例
export function addScaning(data) {
  return request({
    url: '/monitor/scaning',
    method: 'post',
    data
  })
}

// 修改子资源实例
export function updateScaning(data) {
  return request({
    url: '/monitor/scaning',
    method: 'put',
    data
  })
}

// 删除子资源实例
export function delScaning(id) {
  return request({
    url: '/monitor/scaning/' + id,
    method: 'delete'
  })
}
