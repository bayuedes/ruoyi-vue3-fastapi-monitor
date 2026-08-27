<template>
  <div class="app-container">
    <el-form :model="queryParams" ref="queryRef" :inline="true" v-show="showSearch">
      <el-form-item label="指标名称" prop="indexName">
        <el-input v-model="queryParams.indexName" placeholder="请输入指标名称" clearable style="width: 200px" @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item label="指标种类" prop="indexClass">
        <el-input v-model="queryParams.indexClass" placeholder="请输入指标种类" clearable style="width: 200px" @keyup.enter="handleQuery" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" icon="Search" @click="handleQuery">搜索</el-button>
        <el-button icon="Refresh" @click="resetQuery">重置</el-button>
      </el-form-item>
    </el-form>

    <el-row :gutter="10" class="mb8">
      <el-col :span="1.5"><el-button type="primary" plain icon="Plus" @click="handleAdd" v-hasPermi="['monitor:index:add']">新增</el-button></el-col>
      <el-col :span="1.5"><el-button type="success" plain icon="Edit" :disabled="single" @click="handleUpdate" v-hasPermi="['monitor:index:edit']">修改</el-button></el-col>
      <el-col :span="1.5"><el-button type="danger" plain icon="Delete" :disabled="multiple" @click="handleDelete" v-hasPermi="['monitor:index:remove']">删除</el-button></el-col>
      <right-toolbar v-model:showSearch="showSearch" @queryTable="getList"></right-toolbar>
    </el-row>

    <el-table v-loading="loading" :data="list" @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55" align="center" />
      <el-table-column label="序号" prop="indexSort" align="center" width="70" />
      <el-table-column label="指标名称" prop="indexName" align="center" min-width="180" show-overflow-tooltip />
      <el-table-column label="指标种类" prop="indexClass" align="center" min-width="120" />
      <el-table-column label="指标类型" prop="indexType" align="center" min-width="120" />
      <el-table-column label="单位" prop="indexOmpany" align="center" width="100" />
      <el-table-column label="取值脚本" prop="indexScript" align="center" min-width="200" show-overflow-tooltip />
      <el-table-column label="操作" width="180" align="center" class-name="small-padding fixed-width">
        <template #default="scope">
          <el-button link type="primary" icon="Edit" @click="handleUpdate(scope.row)" v-hasPermi="['monitor:index:edit']">修改</el-button>
          <el-button link type="primary" icon="Delete" @click="handleDelete(scope.row)" v-hasPermi="['monitor:index:remove']">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <pagination v-show="total > 0" :total="total" v-model:page="queryParams.pageNum" v-model:limit="queryParams.pageSize" @pagination="getList" />

    <el-dialog :title="title" v-model="open" width="600px" append-to-body>
      <el-form ref="formRef" :model="form" :rules="rules" label-width="100px">
        <el-form-item label="指标名称" prop="indexName"><el-input v-model="form.indexName" placeholder="请输入" /></el-form-item>
        <el-form-item label="指标种类" prop="indexClass"><el-input v-model="form.indexClass" placeholder="请输入" /></el-form-item>
        <el-form-item label="指标类型" prop="indexType"><el-input v-model="form.indexType" placeholder="请输入" /></el-form-item>
        <el-form-item label="单位" prop="indexOmpany"><el-input v-model="form.indexOmpany" placeholder="请输入" /></el-form-item>
        <el-form-item label="取值脚本" prop="indexScript"><el-input v-model="form.indexScript" type="textarea" :rows="3" placeholder="请输入" /></el-form-item>
        <el-form-item label="特殊取值" prop="indexSpecial"><el-input v-model="form.indexSpecial" placeholder="请输入" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button type="primary" @click="submitForm">确 定</el-button>
        <el-button @click="cancel">取 消</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup name="ImonMetric">
import { listMetric, getMetric, addMetric, updateMetric, delMetric } from '@/api/imon/metric'

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
  queryParams: { pageNum: 1, pageSize: 10, indexName: undefined, indexClass: undefined },
  rules: { indexName: [{ required: true, message: '指标名称不能为空', trigger: 'blur' }] }
})
const { queryParams, form, rules } = toRefs(data)

function getList() {
  loading.value = true
  listMetric(queryParams.value).then(res => {
    list.value = res.rows
    total.value = res.total
    loading.value = false
  })
}
function cancel() { open.value = false; reset() }
function reset() {
  form.value = { id: undefined, indexName: undefined, indexClass: undefined, indexType: undefined, indexOmpany: undefined, indexScript: undefined, indexSpecial: undefined }
  proxy.resetForm('formRef')
}
function handleQuery() { queryParams.value.pageNum = 1; getList() }
function resetQuery() { proxy.resetForm('queryRef'); handleQuery() }
function handleSelectionChange(selection) {
  ids.value = selection.map(item => item.id)
  single.value = selection.length !== 1
  multiple.value = !selection.length
}
function handleAdd() { reset(); open.value = true; title.value = '新增指标' }
function handleUpdate(row) {
  reset()
  const id = row.id || ids.value[0]
  getMetric(id).then(res => { form.value = res.data; open.value = true; title.value = '修改指标' })
}
function submitForm() {
  proxy.$refs['formRef'].validate(valid => {
    if (!valid) return
    if (form.value.id != undefined) {
      updateMetric(form.value).then(() => { proxy.$modal.msgSuccess('修改成功'); open.value = false; getList() })
    } else {
      addMetric(form.value).then(() => { proxy.$modal.msgSuccess('新增成功'); open.value = false; getList() })
    }
  })
}
function handleDelete(row) {
  const delIds = row.id || ids.value.join(',')
  proxy.$modal.confirm('是否确认删除指标 ID 为"' + delIds + '"的数据项？').then(() => delMetric(delIds)).then(() => {
    getList(); proxy.$modal.msgSuccess('删除成功')
  }).catch(() => {})
}

getList()
</script>
