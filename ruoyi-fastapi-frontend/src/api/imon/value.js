import request from '@/utils/request'

// 查询最新取值列表
export function listValue(query) {
  return request({
    url: '/monitor/value/list',
    method: 'get',
    params: query
  })
}

// 查询最新取值详情
export function getValue(id) {
  return request({
    url: '/monitor/value/' + id,
    method: 'get'
  })
}

// 新增最新取值
export function addValue(data) {
  return request({
    url: '/monitor/value',
    method: 'post',
    data
  })
}

// 修改最新取值
export function updateValue(data) {
  return request({
    url: '/monitor/value',
    method: 'put',
    data
  })
}

// 删除最新取值
export function delValue(id) {
  return request({
    url: '/monitor/value/' + id,
    method: 'delete'
  })
}
