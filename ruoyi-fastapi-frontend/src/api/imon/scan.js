import request from '@/utils/request'

// 查询子资源类型列表
export function listScan(query) {
  return request({
    url: '/monitor/scan/list',
    method: 'get',
    params: query
  })
}

// 查询子资源类型详情
export function getScan(id) {
  return request({
    url: '/monitor/scan/' + id,
    method: 'get'
  })
}

// 新增子资源类型
export function addScan(data) {
  return request({
    url: '/monitor/scan',
    method: 'post',
    data
  })
}

// 修改子资源类型
export function updateScan(data) {
  return request({
    url: '/monitor/scan',
    method: 'put',
    data
  })
}

// 删除子资源类型
export function delScan(id) {
  return request({
    url: '/monitor/scan/' + id,
    method: 'delete'
  })
}
