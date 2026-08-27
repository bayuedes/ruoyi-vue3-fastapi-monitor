<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="资源名称" prop="resourceName">
        <el-input v-model="queryParams.resourceName" placeholder="请输入资源名称" clearable style="width: 200px" @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="管理 IP" prop="resourceIp">
        <el-input v-model="queryParams.resourceIp" placeholder="请输入管理 IP" clearable style="width: 200px" @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5">
        <el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['monitor:resource:add']">新增</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate" v-hasPermi="['monitor:resource:edit']">修改</el-button>
      </el-col>
      <el-col :span="1.5">
        <el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete" v-hasPermi="['monitor:resource:remove']">删除</el-button>
      </el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="list" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" prop="resourceSort" align="center" width="70" />
      <el-table-column label="资源名称" prop="resourceName" align="center" min-width="180" show-overflow-tooltip />
      <el-table-column label="管理 IP" prop="resourceIp" align="center" min-width="160" />
      <el-table-column label="资源类型" prop="resourceType" align="center" min-width="120" show-overflow-tooltip />
      <el-table-column label="健康度" prop="resourceHealth" align="center" width="100" />
      <el-table-column label="可用度" prop="resourceUsable" align="center" width="100" />
      <el-table-column label="采集节点" prop="resourceCollector" align="center" min-width="120" show-overflow-tooltip />
      <el-table-column label="操作" width="180" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['monitor:resource:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['monitor:resource:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize" @pagination="getList" />

    <el-dialog :title="title" v-model="open" width="680px" append-to-body>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-row>
          <el-col :span="12"><el-form-item label="资源名称" prop="resourceName"><el-input v-model="form.resourceName" placeholder="请输入" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="管理 IP" prop="resourceIp"><el-input v-model="form.resourceIp" placeholder="请输入" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="资源类型" prop="resourceType"><el-input v-model="form.resourceType" placeholder="请输入" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="资源地域" prop="resourceRegion"><el-input v-model="form.resourceRegion" placeholder="请输入" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="采集节点" prop="resourceCollector"><el-input v-model="form.resourceCollector" placeholder="请输入" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="系统 IP" prop="resourceSystemIp"><el-input v-model="form.resourceSystemIp" placeholder="请输入" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="系统名称" prop="resourceSystemName"><el-input v-model="form.resourceSystemName" placeholder="请输入" /></el-form-item></el-col>
          <el-col :span="12"><el-form-item label="系统 MAC" prop="resourceSystemMac"><el-input v-model="form.resourceSystemMac" placeholder="请输入" /></el-form-item></el-col>
          <el-col :span="24"><el-form-item label="系统描述" prop="resourceSystemDescribe"><el-input v-model="form.resourceSystemDescribe" type="textarea" :rows="2" /></el-form-item></el-col>
        </el-row>
      </el-form>
      <template #footer>
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="ImonResource">
import { listResource, getResource, addResource, updateResource, delResource } from '@/api/imon/resource'

const { proxy } = getCurrentInstance()

const list = ref([])
const open = ref(false)
const loading = ref(true)
const showSearch = ref(true)
const ids = ref([])
const single = ref(true)
const multiple = ref(true)
const total = ref(0)
const title = ref('')

const data = reactive({
  form: {},
  queryParams: { pageNum: 1, pageSize: 10, resourceName: undefined, resourceIp: undefined },
  rules: {
    resourceName: [{ required: true, message: '资源名称不能为空', trigger: 'blur' }],
    resourceIp: [{ required: true, message: '管理 IP 不能为空', trigger: 'blur' }]
  }
})
const { queryParams, form, rules } = toRefs(data)

function getList() {
  loading.value = true
  listResource(queryParams.value).then(res => {
    list.value = res.rows
    total.value = res.total
    loading.value = false
  })
}
function cancel() { open.value = false; reset() }
function reset() {
  form.value = {
    id: undefined,
    resourceName: undefined,
    resourceIp: undefined,
    resourceType: undefined,
    resourceRegion: undefined,
    resourceCollector: undefined,
    resourceSystemIp: undefined,
    resourceSystemName: undefined,
    resourceSystemMac: undefined,
    resourceSystemDescribe: undefined
  }
  proxy.resetForm('formRef')
}
function handleQuery() { queryParams.value.pageNum = 1; getList() }
function resetQuery() { proxy.resetForm('queryRef'); handleQuery() }
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id)
  single.value = selection.length !== 1
  multiple.value = !selection.length
}
function handleAdd() { reset(); open.value = true; title.value = '新增资源' }
function handleUpdate(row) {
  reset()
  const id = row.id || ids.value[0]
  getResource(id).then(res => {
    form.value = res.data
    open.value = true
    title.value = '修改资源'
  })
}
function submitForm() {
  proxy.$refs['formRef'].validate(valid => {
    if (!valid) return
    if (form.value.id != undefined) {
      updateResource(form.value).then(() => { proxy.$modal.msgSuccess('修改成功'); open.value = false; getList() })
    } else {
      addResource(form.value).then(() => { proxy.$modal.msgSuccess('新增成功'); open.value = false; getList() })
    }
  })
}
function handleDelete(row) {
  const delIds = row.id || ids.value.join(',')
  proxy.$modal.confirm('是否确认删除资源 ID 为"' + delIds + '"的数据项？').then(() => delResource(delIds)).then(() => {
    getList(); proxy.$modal.msgSuccess('删除成功')
  }).catch(() => {})
}

getList()
</script>
