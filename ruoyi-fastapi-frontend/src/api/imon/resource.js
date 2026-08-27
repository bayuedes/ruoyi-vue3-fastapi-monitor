import request from '@/utils/request'

// 查询资源列表
export function listResource(query) {
  return request({
    url: '/monitor/resource/list',
    method: 'get',
    params: query
  })
}

// 查询资源详情
export function getResource(id) {
  return request({
    url: '/monitor/resource/' + id,
    method: 'get'
  })
}

// 新增资源
export function addResource(data) {
  return request({
    url: '/monitor/resource',
    method: 'post',
    data
  })
}

// 修改资源
export function updateResource(data) {
  return request({
    url: '/monitor/resource',
    method: 'put',
    data
  })
}

// 删除资源
export function delResource(id) {
  return request({
    url: '/monitor/resource/' + id,
    method: 'delete'
  })
}
