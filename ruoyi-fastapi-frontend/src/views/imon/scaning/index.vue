<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="实例名称" prop="scaningName">
        <el-input v-model="queryParams.scaningName" placeholder="请输入实例名称" clearable style="width: 200px" @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="所属资源 ID" prop="scaningResource">
        <el-input v-model="queryParams.scaningResource" placeholder="请输入资源 ID" clearable style="width: 220px" @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5"><el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['monitor:scaning:add']">新增</el-button></el-col>
      <el-col :span="1.5"><el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate" v-hasPermi="['monitor:scaning:edit']">修改</el-button></el-col>
      <el-col :span="1.5"><el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete" v-hasPermi="['monitor:scaning:remove']">删除</el-button></el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="list" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" prop="scaningSort" align="center" width="70" />
      <el-table-column label="实例名称" prop="scaningName" align="center" min-width="200" show-overflow-tooltip />
      <el-table-column label="所属资源 ID" prop="scaningResource" align="center" min-width="220" show-overflow-tooltip />
      <el-table-column label="监控指标" prop="scaningIndex" align="center" min-width="200" show-overflow-tooltip />
      <el-table-column label="管理状态" prop="scaningManage" align="center" width="100" />
      <el-table-column label="关键状态" prop="scaningCrux" align="center" width="100" />
      <el-table-column label="操作" width="180" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['monitor:scaning:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['monitor:scaning:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize" @pagination="getList" />

    <el-dialog :title="title" v-model="open" width="600px" append-to-body>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="实例名称" prop="scaningName"><el-input v-model="form.scaningName" placeholder="请输入" /></el-form-item>
        <el-form-item label="所属资源 ID" prop="scaningResource"><el-input v-model="form.scaningResource" placeholder="请输入" /></el-form-item>
        <el-form-item label="监控指标" prop="scaningIndex"><el-input v-model="form.scaningIndex" type="textarea" :rows="2" placeholder="请输入" /></el-form-item>
        <el-form-item label="管理状态" prop="scaningManage"><el-input v-model="form.scaningManage" placeholder="请输入" /></el-form-item>
        <el-form-item label="关键状态" prop="scaningCrux"><el-input v-model="form.scaningCrux" placeholder="请输入" /></el-form-item>
        <el-form-item label="实例类型" prop="scaningType"><el-input v-model="form.scaningType" placeholder="请输入" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="ImonScaning">
import { listScaning, getScaning, addScaning, updateScaning, delScaning } from '@/api/imon/scaning'

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
  queryParams: { pageNum: 1, pageSize: 10, scaningName: undefined, scaningResource: undefined },
  rules: { scaningName: [{ required: true, message: '实例名称不能为空', trigger: 'blur' }] }
})
const { queryParams, form, rules } = toRefs(data)

function getList() {
  loading.value = true
  listScaning(queryParams.value).then(res => {
    list.value = res.rows
    total.value = res.total
    loading.value = false
  })
}
function cancel() { open.value = false; reset() }
function reset() {
  form.value = { id: undefined, scaningName: undefined, scaningResource: undefined, scaningIndex: undefined, scaningManage: undefined, scaningCrux: undefined, scaningType: undefined }
  proxy.resetForm('formRef')
}
function handleQuery() { queryParams.value.pageNum = 1; getList() }
function resetQuery() { proxy.resetForm('queryRef'); handleQuery() }
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id)
  single.value = selection.length !== 1
  multiple.value = !selection.length
}
function handleAdd() { reset(); open.value = true; title.value = '新增子资源实例' }
function handleUpdate(row) {
  reset()
  const id = row.id || ids.value[0]
  getScaning(id).then(res => { form.value = res.data; open.value = true; title.value = '修改子资源实例' })
}
function submitForm() {
  proxy.$refs['formRef'].validate(valid => {
    if (!valid) return
    if (form.value.id != undefined) {
      updateScaning(form.value).then(() => { proxy.$modal.msgSuccess('修改成功'); open.value = false; getList() })
    } else {
      addScaning(form.value).then(() => { proxy.$modal.msgSuccess('新增成功'); open.value = false; getList() })
    }
  })
}
function handleDelete(row) {
  const delIds = row.id || ids.value.join(',')
  proxy.$modal.confirm('是否确认删除子资源实例 ID 为"' + delIds + '"的数据项？').then(() => delScaning(delIds)).then(() => {
    getList(); proxy.$modal.msgSuccess('删除成功')
  }).catch(() => {})
}

getList()
</script>
