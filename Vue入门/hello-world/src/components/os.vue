<template>
  <div>
    <el-container>
      <el-header>{{ msg }}</el-header>
      <!-- 上半部分 -->
      <el-container style="height: 380px">
        <!-- 左边   用于创建进程   占5成，间隔20px -->
        <el-aside width="50%" style="padding: 20px ">
          <el-container>
            <!-- 表单1  负责创建进程 -->
            <el-aside width="70%" >             
              <div class="bg">
                <el-form ref="form" :model="form" label-width="80px" style="height: 300px">
                <el-form-item label="所需时间">
                    <el-input v-model="form.time" style="width: 200px"></el-input>
                </el-form-item>
                <el-form-item label="所需内存">
                    <el-input v-model="form.ram" style="width: 200px"></el-input>
                </el-form-item>
                <el-form-item label="优先级" style="width: 400px">
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
                <el-form-item label="前驱进程" style="width: 400px">
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
                <el-button type="primary" @click="createPCB" style="margin-bottom: 20px">立即创建</el-button>
              </div>
            </el-aside>
            <!-- 表单2  负责进程挂起和解挂 -->
            <el-main width="30%">
              <div class="bg">
                <el-form ref="form" :model="form2" label-width="40px" style="height: 330px">
                  <el-form-item label="pid">
                      <el-input v-model="form2.pid" style="width: 80px"></el-input>
                  </el-form-item>
                  <el-button type="primary" @click="suspend" style="margin-top: 10px">挂起或解挂</el-button>
                </el-form>
              </div>             
            </el-main>
          </el-container>
            
            
        </el-aside>
        <!-- 右边   展示内存和四个队列    占5成 -->
        <el-main width="50%" style="padding: 20px">
          <el-tabs v-model="displayName" type="border-card">
            <el-tab-pane label="内存空间" name="tab_first" style="height: 380px">
              <el-table :data="mainMemory" :row-class-name="tableRowClassName" border style="width: 100%" height="380">
                <el-table-column fixed prop="memory_PCB" label="进程号" width="125" align="center"></el-table-column>
                <el-table-column prop="start" label="起址" width="125" align="center"></el-table-column>
                <el-table-column prop="length" label="长度" width="130" align="center"></el-table-column>
                <el-table-column prop="memory_state" label="分配情况" width="130" align="center"></el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="就绪队列" name="tab_second" style="height: 380px">
              <el-table :data="readyQueue" border style="width: 100%" height="380">
                <el-table-column fixed prop="pid" label="进程号" align="center"></el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="后备队列" name="tab_third" style="height: 380px">
              <el-table :data="backupQueue" border style="width: 100%" height="380">
                <el-table-column fixed prop="pid" label="进程号" align="center"></el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="挂起队列" name="tab_forth" style="height: 380px">
              <el-table :data="suspendQueue" border style="width: 100%" height="380">
                <el-table-column fixed prop="pid" label="进程号" align="center"></el-table-column>
              </el-table>
            </el-tab-pane>
            <el-tab-pane label="阻塞队列" name="tab_fifth" style="height: 380px">
              <el-table :data="blockQueue" border style="width: 100%" height="380">
                <el-table-column fixed prop="pid" label="进程号" align="center"></el-table-column>
              </el-table>
            </el-tab-pane>
          </el-tabs>
        </el-main>
      </el-container>

      <!-- 下半部分 -->
      <el-container>
        <el-main >
          <el-table :data="pcb_display" border style="width: 100%" height="320">
            <el-table-column fixed prop="pid" label="进程号" width="130" align="center"></el-table-column>
            <el-table-column prop="time" label="进程所需时间" width="130" align="center"></el-table-column>
            <el-table-column prop="ram" label="进程所需内存" width="130" align="center"></el-table-column>
            <el-table-column prop="priority" label="进程优先级" width="130" align="center"></el-table-column>
            <el-table-column prop="state" label="进程状态" width="130" align="center"></el-table-column>
            <el-table-column prop="property" label="进程属性" width="130" align="center"></el-table-column>
            <el-table-column prop="precursor" label="进程前驱" width="250" align="center"></el-table-column>
            <el-table-column prop="successor" label="进程后继" width="250" align="center"></el-table-column>
          </el-table>
          <el-button type="primary" @click="run" style="margin-top: 10px">运行一步</el-button>
          <el-button type="primary" @click="refresh" style="margin-top: 10px">刷新界面</el-button>
        </el-main>


      </el-container>

    </el-container>
  </div>
</template>

<script>

export default {
  name: "os",
  //传参
  props: {
    msg: String
  },
  data() {
    return {
      operationName: 'tab_first',
      displayName: 'tab_first',
      //PCB内存状态表
      pcbState: [
        {
          "id": 0,
          "name": "进程创建",
        }, {
          "id": 1,
          "name": "活动就绪",
        }, {
          "id": 2,
          "name": "静止就绪",
        }, {
          "id": 3,
          "name": "阻塞状态",
        },{
          "id": 4,
          "name": "进程运行",
        }, {
          "id": 5,
          "name": "进程挂起",
        }, {
          "id": 6,
          "name": "进程结束",
        },
      ],
      totalMemory: 100, //内存总容量
      //创建PCB表单内容
      form: {
        time: '',
        ram: '',
        priority: '',
        property: '',
        precursor: [],
      },
      // 挂起解挂表单内容
      form2:{
        pid:'',
      },
      pcbData: [],      //创建PCB的数据
      mainMemory: [],   //主存分区表信息
      processors: [],   //处理器信息
      readyQueue: [],   //就绪队列
      blockQueue: [],   //阻塞队列
      backupQueue: [],  //后备队列
      suspendQueue: [], //挂起队列
    };
  },
  computed: {
    //OS内存标志
    os_memory: function () {
      for (var i = 0; i < this.mainMemory.length; i++) {
        var partition = this.mainMemory[i];
        if (partition.memory_state === '操作系统') {
          return parseInt(partition.length);
        }
      }
      return 20;
    },
    //前驱标志
    precursor_flag: function () {
      // eslint-disable-next-line vue/no-side-effects-in-computed-properties
      this.form.precursor = [];
      return this.form.property === '0' || this.form.property === '';
    },
    //限制可选前驱
    precursor_options: function () {
      // 提取可选前驱进程
      var options = [];
      for (var i = 0; i < this.pcbData.length; i++) {
        options.push({
          'value': this.pcbData[i].pid,
          'label': this.pcbData[i].pid,
        });
      }
      return options;
    },
    //展示所有PCB数据
    pcb_display: function () {
      // 将返回的数据转换为用于在表格中显示的形式
      var PCB_display = JSON.parse(JSON.stringify(this.pcbData));
      for (var i = 0; i < PCB_display.length; i++) {
        var pcb = PCB_display[i];
        if (pcb.precursor.length === 0) {
          pcb.precursor = '无';
        } else {
          pcb.precursor = pcb.precursor.join(',');
        }
        if (pcb.successor.length === 0) {
          pcb.successor = '无';
        } else {
          pcb.successor = pcb.successor.join(',');
        }
      }
      return PCB_display;
    },
  },
  watch: {
    pcbData: function () {
      this.getMainMemory();
      this.getQueue();
    },
  },
  methods: {
    // eslint-disable-next-line no-unused-vars
    tableRowClassName({row, rowIndex}) {
      if (row.memory_state === '操作系统') {
        return 'warning-row';
      } else if (row.memory_state === '未分配') {
        return 'success-row';
      }
      return '';
    },
    //发起请求，获取pcb_list刷新界面
    refresh() {
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:5000/os/get_PCB_list", // 接口地址
      }).then(response => {
        console.log(response);   // 成功的返回
        this.pcbData = response.data['pcb_list']; // 将返回的数据转换为用于在表格中显示的形式
      }).catch(error => console.log(error, "error")); // 失败的返回
    },
    //发送请求，运行一步并接收新的PCB信息队列更新页面
    run() {
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:5000/os/run",
      }).then(response => {
        console.log(response);
        this.pcbData = response.data['pcb_list'];
      }).catch(error => {
        console.log(error.response, "error");
        this.$message({
          message: error.response.data.errMsg,
          type: 'error'
        });
      });
    },
    //发送请求，创建新的PCB块
    createPCB() {
      if (this.form.time === '' || this.form.ram === '' || this.form.property === '' || this.form.priority === '') {
        this.$message({
          message: '表单未填写完整，无法创建进程！',
          type: 'error'
        });
        return;
      }
      if (this.form.ram > this.totalMemory - this.os_memory) {
        this.$message({
          message: '进程所需内存大于系统内存容量，无法创建进程！',
          type: 'error'
        });
        return;
      }
      if (this.form.property === 1 && this.form.precursor.length === 0) {
        this.form.property = 0;
        this.$message({
          message: '未选择前驱进程，已切换为独立进程！',
          type: 'warning'
        });
      }
      this.$axios({
        method: "post",
        url: "http://127.0.0.1:5000/os/create_PCB", // 接口地址
        data: {'form': this.form,}
      }).then(response => {
        console.log(response);   // 成功的返回
        this.pcbData = response.data['pcb_list']; // 将返回的数据转换为用于在表格中显示的形式
      }).catch(error => {
        console.log(error.response, "error");
        this.$message({
          message: error.response.data.errMsg,
          type: 'error'
        });
      }); // 失败的返回
    },
    //发送请求，获取主存分区表
    getMainMemory() {
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:5000/os/get_main_memory",
      }).then(response => {
        console.log(response);
        this.mainMemory = response.data['main_memory'];
      }).catch(error => console.log(error, "error"));
    },
    //发送请求，获取四个队列
    getQueue(){
      this.$axios({
        method: "get",
        url: "http://127.0.0.1:5000/os/get_queue",
      }).then(response => {
        console.log(response);
        this.readyQueue = response.data['ready_queue'];
        this.blockQueue = response.data['block_queue'];
        this.suspendQueue = response.data['suspend_queue'];
        this.backupQueue = response.data['backup_queue'];
      }).catch(error => console.log(error, "error"));
    },
    //挂起或解挂操作
    suspend(){
      // 没处理错误输入，只能输入整数
      if (this.form2.pid === '' ) {
        this.$message({
          message: '表单未填写完整，无法创建进程！',
          type: 'error'
        });
        return;
      }
      this.$axios({
        method: "post",
        url: "http://127.0.0.1:5000/os/suspend", // 接口地址
        data: {'form': this.form2,}
      }).then(response => {
        console.log(response);   // 成功的返回
        this.pcbData = response.data['pcb_list']; // 将返回的数据转换为用于在表格中显示的形式
      }).catch(error => {
        console.log(error.response, "error");
        this.$message({
          message: error.response.data.errMsg,
          type: 'error'
        });
      }); // 失败的返回
    },
  },
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
.bg{
  background-color: #FFFFFF;
  padding: 20px;
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