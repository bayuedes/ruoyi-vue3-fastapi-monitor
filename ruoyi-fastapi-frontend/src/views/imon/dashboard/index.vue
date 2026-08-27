<template>
  <div class="app-container">
    <el-row :gutter="16">
      <!-- Q1: 监控设备总数 -->
      <el-col :xs="24" :sm="12" :md="8">
        <el-card shadow="hover" class="dashboard-card">
          <template #header>
            <el-icon><Monitor /></el-icon>
            <span class="card-title">监控设备总数</span>
          </template>
          <div class="metric-value" v-loading="loading.q1">
            <span class="big-number">{{ deviceCount }}</span>
            <span class="unit">台</span>
          </div>
          <div class="metric-desc">当前监控的设备总数 (it_resource_list 表中 delete_time 为空)</div>
        </el-card>
      </el-col>

      <!-- Q3: Ping 响应时间查询 -->
      <el-col :xs="24" :sm="12" :md="16">
        <el-card shadow="hover" class="dashboard-card">
          <template #header>
            <el-icon><Connection /></el-icon>
            <span class="card-title">指定 IP 资源最近 10 次 Ping 响应时间</span>
          </template>
          <el-form :inline="true" @submit.prevent>
            <el-form-item label="资源 IP">
              <el-input
                v-model="pingIp"
                placeholder="如 192.168.145.253"
                clearable
                style="width: 220px"
                @keyup.enter="loadRecentPing"
              />
            </el-form-item>
            <el-form-item>
              <el-button type="primary" icon="Search" @click="loadRecentPing" :loading="loading.q3">查询</el-button>
            </el-form-item>
          </el-form>
          <el-table :data="pingList" v-loading="loading.q3" size="small" border max-height="320">
            <el-table-column type="index" label="#" width="50" align="center" />
            <el-table-column label="取值时间" prop="scanTime" align="center" min-width="180" />
            <el-table-column label="Ping 响应时间 (ms)" prop="indexValue" align="center" min-width="180" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>

    <!-- Q2: CPU 利用率 Top 10 -->
    <el-card shadow="hover" class="dashboard-card" style="margin-top: 16px">
      <template #header>
        <el-icon><Cpu /></el-icon>
        <span class="card-title">当前平均 CPU 利用率最高的 10 台设备</span>
      </template>
      <el-table :data="cpuTopList" v-loading="loading.q2" border size="default">
        <el-table-column type="index" label="排名" width="80" align="center" />
        <el-table-column label="资源名称" prop="resourceName" align="center" min-width="200" show-overflow-tooltip />
        <el-table-column label="资源 IP" prop="resourceIp" align="center" min-width="160" />
        <el-table-column label="资源 ID" prop="resourceId" align="center" min-width="240" show-overflow-tooltip />
        <el-table-column label="CPU 利用率" prop="valueWord" align="center" min-width="160">
          <template #default="scope">
            <el-tag :type="getCpuTagType(scope.row.valueWord)">{{ scope.row.valueWord }}</el-tag>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup name="ImonDashboard">
import { getDeviceCount, getTopCpuDevices, getRecentPing } from '@/api/imon/dashboard'

const { proxy } = getCurrentInstance()

const deviceCount = ref(0)
const cpuTopList = ref([])
const pingList = ref([])
const pingIp = ref('192.168.145.253')

const loading = reactive({ q1: false, q2: false, q3: false })

function loadDeviceCount() {
  loading.q1 = true
  getDeviceCount()
    .then(res => {
      deviceCount.value = res.deviceCount ?? 0
    })
    .finally(() => (loading.q1 = false))
}

function loadTopCpu() {
  loading.q2 = true
  getTopCpuDevices(10)
    .then(res => {
      cpuTopList.value = res.data ?? []
    })
    .finally(() => (loading.q2 = false))
}

function loadRecentPing() {
  if (!pingIp.value) {
    proxy.$modal.msgWarning('请输入资源 IP')
    return
  }
  loading.q3 = true
  getRecentPing(pingIp.value, 10)
    .then(res => {
      pingList.value = res.data ?? []
      if (pingList.value.length === 0) {
        proxy.$modal.msg(`未查询到 ${pingIp.value} 的 Ping 记录`)
      }
    })
    .finally(() => (loading.q3 = false))
}

function getCpuTagType(value) {
  const num = parseFloat(value)
  if (isNaN(num)) return 'info'
  if (num >= 80) return 'danger'
  if (num >= 50) return 'warning'
  return 'success'
}

loadDeviceCount()
loadTopCpu()
loadRecentPing()
</script>

<style scoped>
.dashboard-card {
  margin-bottom: 8px;
}
.card-title {
  margin-left: 6px;
  font-weight: 600;
}
.metric-value {
  display: flex;
  align-items: baseline;
  gap: 8px;
  padding: 8px 0;
}
.big-number {
  font-size: 36px;
  font-weight: 700;
  color: #409eff;
}
.unit {
  font-size: 16px;
  color: #909399;
}
.metric-desc {
  color: #909399;
  font-size: 12px;
  margin-top: 4px;
}
</style>
