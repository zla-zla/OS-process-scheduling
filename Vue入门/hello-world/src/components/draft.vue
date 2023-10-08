<template>
  <div>
    <el-container>
      <el-header>{{ msg }}</el-header>
      <el-container style="height: 500px">

        <el-aside width="40%" style="padding: 20px">
          <el-tabs v-model="operationName" type="border-card">
            <el-tab-pane label="创建进程" name="tab_first" style="height: 380px">
              <el-form ref="form" :model="form" label-width="80px">
                <el-form-item label="所需时间">
                  <el-input v-model="form.time"></el-input>
                </el-form-item>
                <el-form-item label="所需内存">
                  <el-input v-model="form.ram"></el-input>
                </el-form-item>
                <el-form-item label="优先级">
                  <el-select v-model="form.priority" placeholder="请选择进程优先级">
                    <el-option label="1" value="1"></el-option>
                    <el-option label="2" value="2"></el-option>
                    <el-option label="3" value="3"></el-option>
                    <el-option label="4" value="4"></el-option>
                    <el-option label="5" value="5"></el-option>
                    <el-option label="6" value="6"></el-option>
                    <el-option label="7" value="7"></el-option>
                    <el-option label="8" value="8"></el-option>
                    <el-option label="9" value="9"></el-option>
                  </el-select>
                </el-form-item>
                <el-form-item label="进程属性">
                  <el-radio-group v-model="form.property">
                    <el-radio label="0">独立进程</el-radio>
                    <el-radio label="1">同步进程</el-radio>
                  </el-radio-group>
                </el-form-item>
                <el-form-item label="前驱进程">
                  <el-select v-model="form.precursor" multiple placeholder="请选择前驱进程" :disabled="precursor_flag">
                    <el-option
                        v-for="item in precursor_options"
                        :key="item.value"
                        :label="item.label"
                        :value="item.value">
                    </el-option>
                  </el-select>
                </el-form-item>
              </el-form>
              <el-button type="primary" @click="createPCB" style="margin-top: 10px">立即创建</el-button>
            </el-tab-pane>
            <el-tab-pane label="挂起 / 解挂进程" name="tab_second" style="height: 380px">
              <div style="text-align: center; padding-top: 40px">
                <el-transfer
                    style="text-align: left; display: inline-block"
                    v-model="hanging_value"
                    :titles="['未挂起', '挂起']"
                    :format="{
                      noChecked: '0/${total}',
                      hasChecked: '${checked}/${total}'
                    }"
                    @change="hangingDataChange"
                    :data="non_hanging_pcb_value">
                  <span slot-scope="{ option }">{{ option.key }}</span>
                </el-transfer>
              </div>
            </el-tab-pane>
            <el-tab-pane label="运行" name="tab_forth" style="height: 380px">
              <div style="padding-top: 160px">
                <el-button type="primary" @click="refresh">刷新</el-button>
                <el-button type="primary" @click="run">运行</el-button>
              </div>
            </el-tab-pane>
          </el-tabs>
        </el-aside>
        
        <el-main width="60%">
          <el-table :data="pcb_display" border style="width: 100%" height="450">
            <el-table-column fixed prop="pid" label="进程号" width="80" align="center"></el-table-column>
            <el-table-column prop="time" label="进程所需时间" width="120" align="center"></el-table-column>
            <el-table-column prop="ram" label="进程所需内存" width="120" align="center"></el-table-column>
            <el-table-column prop="priority" label="进程优先级" width="120" align="center"></el-table-column>
            <el-table-column prop="state" label="进程状态" width="120" align="center"></el-table-column>
            <el-table-column prop="property" label="进程属性" width="120" align="center"></el-table-column>
            <el-table-column prop="precursor" label="进程前驱" width="200" align="center"></el-table-column>
            <el-table-column prop="successor" label="进程后继" width="200" align="center"></el-table-column>
          </el-table>
        </el-main>
      </el-container>
      <el-container>
        <el-aside width="40%" style="padding: 20px">
          <el-tabs v-model="displayName" type="border-card">
            <el-tab-pane label="内存空间" name="tab_first" style="height: 380px">
              <el-table :data="mainMemory" :row-class-name="tableRowClassName" border style="width: 100%" height="380">
                <el-table-column fixed prop="memory_PCB" label="进程号" width="125" align="center"></el-table-column>
                <el-table-column prop="start" label="起址" width="125" align="center"></el-table-column>
                <el-table-column prop="length" label="长度" width="130" align="center"></el-table-column>
                <el-table-column prop="memory_state" label="分配情况" width="130" align="center"></el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="处理机" name="tab_second" style="height: 380px">
              <div v-for="processor in processors" :key="processor.id" style="float: left">
                <el-table :data="processor.pid_list" border style="width: 100%" height="380">
                  <el-table-column v-bind:label="processor.id" style="margin-bottom: 10px" align="center">
                    <el-table-column fixed prop="pid" label="进程号" width="120" align="center"></el-table-column>
                  </el-table-column>
                </el-table>
              </div>
            </el-tab-pane>
            <el-tab-pane label="后备队列" name="tab_third" style="height: 380px">
              <el-table :data="backupQueue" border style="width: 100%" height="380">
                <el-table-column fixed prop="pid" label="进程号" align="center"></el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="挂起队列" name="tab_forth" style="height: 380px">
              <el-table :data="hangingQueue" border style="width: 100%" height="380">
                <el-table-column fixed prop="pid" label="进程号" align="center"></el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-aside>
        <el-main width="60%">
          <div class="echarts">
            <div id="echarts" style="height: 450px;"></div>
          </div>
        </el-main>
      </el-container>
    </el-container>
  </div>
</template>

<script>

export default {
  name: "os",
  props: {
    msg: String
  },
  // 存放数据
  data() {
    return {

    };
  },
  // 
  computed: {

  },
  watch: {
    pcbData: function () {
      this.getMainMemory();
      this.getProcessors();
      this.getBackupQueue();
      this.getHangingQueue();
      this.getNodes();
      this.getEdges();
    },
    nodes: function () {
      this.myEcharts();
    },
    edges: function () {
      this.myEcharts();
    }
  },
  methods: {

  },
  mounted() {

  }
}
</script>

<style>
.el-header, .el-footer {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 60px;
  font-size: 18px;
  font-weight: bold;
}

.el-aside {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
}

.el-main {
  background-color: #E9EEF3;
  color: #333;
  text-align: center;
}

.el-transfer-panel {
  width: 150px !important;
}

.el-select {
  width: 430px !important;
}

.el-table .warning-row {
  background: oldlace;
}

.el-table .success-row {
  background: #f0f9eb;
}

.echarts {
  background-color: #FFFFFF;
}
</style>

