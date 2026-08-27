<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="类型名称" prop="scanName">
        <el-input v-model="queryParams.scanName" placeholder="请输入类型名称" clearable style="width: 200px" @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5"><el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['monitor:scan:add']">新增</el-button></el-col>
      <el-col :span="1.5"><el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate" v-hasPermi="['monitor:scan:edit']">修改</el-button></el-col>
      <el-col :span="1.5"><el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete" v-hasPermi="['monitor:scan:remove']">删除</el-button></el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="list" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" prop="scanSort" align="center" width="70" />
      <el-table-column label="类型名称" prop="scanName" align="center" min-width="180" show-overflow-tooltip />
      <el-table-column label="指标集合" prop="scanGather" align="center" min-width="200" show-overflow-tooltip />
      <el-table-column label="扫描脚本" prop="scanScript" align="center" min-width="200" show-overflow-tooltip />
      <el-table-column label="名称脚本" prop="nameScript" align="center" min-width="200" show-overflow-tooltip />
      <el-table-column label="操作" width="180" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['monitor:scan:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['monitor:scan:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize" @pagination="getList" />

    <el-dialog :title="title" v-model="open" width="600px" append-to-body>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="类型名称" prop="scanName"><el-input v-model="form.scanName" placeholder="请输入" /></el-form-item>
        <el-form-item label="指标集合" prop="scanGather"><el-input v-model="form.scanGather" type="textarea" :rows="2" placeholder="请输入" /></el-form-item>
        <el-form-item label="扫描脚本" prop="scanScript"><el-input v-model="form.scanScript" type="textarea" :rows="3" placeholder="请输入" /></el-form-item>
        <el-form-item label="名称脚本" prop="nameScript"><el-input v-model="form.nameScript" type="textarea" :rows="3" placeholder="请输入" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="ImonScan">
import { listScan, getScan, addScan, updateScan, delScan } from '@/api/imon/scan'

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
  queryParams: { pageNum: 1, pageSize: 10, scanName: undefined },
  rules: { scanName: [{ required: true, message: '类型名称不能为空', trigger: 'blur' }] }
})
const { queryParams, form, rules } = toRefs(data)

function getList() {
  loading.value = true
  listScan(queryParams.value).then(res => {
    list.value = res.rows
    total.value = res.total
    loading.value = false
  })
}
function cancel() { open.value = false; reset() }
function reset() {
  form.value = { id: undefined, scanName: undefined, scanGather: undefined, scanScript: undefined, nameScript: undefined }
  proxy.resetForm('formRef')
}
function handleQuery() { queryParams.value.pageNum = 1; getList() }
function resetQuery() { proxy.resetForm('queryRef'); handleQuery() }
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id)
  single.value = selection.length !== 1
  multiple.value = !selection.length
}
function handleAdd() { reset(); open.value = true; title.value = '新增子资源类型' }
function handleUpdate(row) {
  reset()
  const id = row.id || ids.value[0]
  getScan(id).then(res => { form.value = res.data; open.value = true; title.value = '修改子资源类型' })
}
function submitForm() {
  proxy.$refs['formRef'].validate(valid => {
    if (!valid) return
    if (form.value.id != undefined) {
      updateScan(form.value).then(() => { proxy.$modal.msgSuccess('修改成功'); open.value = false; getList() })
    } else {
      addScan(form.value).then(() => { proxy.$modal.msgSuccess('新增成功'); open.value = false; getList() })
    }
  })
}
function handleDelete(row) {
  const delIds = row.id || ids.value.join(',')
  proxy.$modal.confirm('是否确认删除子资源类型 ID 为"' + delIds + '"的数据项？').then(() => delScan(delIds)).then(() => {
    getList(); proxy.$modal.msgSuccess('删除成功')
  }).catch(() => {})
}

getList()
</script>
