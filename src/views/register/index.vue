<template>
  <div class="register-container">
    <el-form ref="registerForm" :model="registerForm" :rules="rules" label-width="120px">
      <el-form-item label="用户名" prop="volunteer_name">
        <el-input v-model="registerForm.volunteer_name" autocomplete="off" />
      </el-form-item>
      <el-form-item label="电话号码" prop="volunteer_phone_number">
        <el-input v-model="registerForm.volunteer_phone_number" autocomplete="off" />
      </el-form-item>
      <el-form-item label="密码" prop="volunteer_login_pwd">
        <el-input v-model="registerForm.volunteer_login_pwd" type="password" autocomplete="new-password" />
      </el-form-item>
      <el-form-item label="确认密码" prop="confirm_password">
        <el-input v-model="registerForm.confirm_password" type="password" autocomplete="new-password" />
      </el-form-item>
      <el-form-item label="标识码" prop="volunteer_id">
        <el-input v-model="registerForm.volunteer_id" autocomplete="off" />
      </el-form-item>
      <el-form-item>
        <el-button type="primary" @click="submitForm('registerForm')">注册</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Register',
  data() {
    var validatePhone = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('电话号码不能为空'))
      } else {
        const phoneRegex = /^1[3-9]\d{9}$/
        if (!phoneRegex.test(value)) {
          return callback(new Error('请输入正确的电话号码'))
        }
        callback()
      }
    }
    var validatePassword = (rule, value, callback) => {
      if (value.length < 6) {
        return callback(new Error('密码长度不能小于6位'))
      }
      callback()
    }
    var validateConfirmPassword = (rule, value, callback) => {
      if (value !== this.registerForm.volunteer_login_pwd) {
        return callback(new Error('两次输入的密码不一致'))
      }
      callback()
    }
    return {
      registerForm: {
        volunteer_name: '',
        volunteer_phone_number: '',
        volunteer_login_pwd: '',
        confirm_password: '',
        volunteer_id: ''
      },
      rules: {
        volunteer_name: [
          { required: true, message: '请输入用户名', trigger: 'blur' }
        ],
        volunteer_phone_number: [
          { validator: validatePhone, trigger: 'blur' }
        ],
        volunteer_login_pwd: [
          { validator: validatePassword, trigger: 'blur' }
        ],
        confirm_password: [
          { validator: validateConfirmPassword, trigger: 'blur' }
        ],
        volunteer_id: [
          { required: true, message: '请输入标识码', trigger: 'blur' }
        ]
      }
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios.post('/user/register', this.registerForm)
            .then(response => {
              this.$message({
                message: '注册成功',
                type: 'success'
              })
              // 处理注册成功后的逻辑，例如跳转到登录页面
              this.$router.push('/login')
            })
            .catch(error => {
              this.$message.error('注册失败: ' + error.response.data.message)
            })
        } else {
          console.log('表单验证失败')
          return false
        }
      })
    }
  }
}
</script>

<style scoped>
.register-container {
  max-width: 500px;
  margin: 50px auto;
}
</style>
