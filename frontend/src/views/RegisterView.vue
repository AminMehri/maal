<template>
  <div class="register">

    <div v-if="fullScreenLoading" class="fullscreen-loading">Loading&#8230;</div>

    <div class="container">
      <p class="text-danger">Welcome to the city of lie!</p>
      <div class="card mx-auto" style="width: 25rem;">
        <img src="@/assets/groot.jpg" class="card-img-top" alt="...">
        <div class="card-body">
          <!-- register form -->
          <form @submit.prevent="doRegister()">
            <div class="form-floating mb-3" lang="en">
              <input 
                v-model="username" 
                type="text" 
                class="form-control" 
                id="floatingUsername" 
                placeholder="نام کاربری"
                :class="{'is-invalid':usernameE===true, 'is-valid':usernameE===false}"
              >

              <label for="floatingUsername">Username</label>
              <div class="invalid-feedback">
                {{ usernameEM }}
              </div>
            </div>

						<div class="form-floating mb-3" lang="en">
              <input 
                v-model="email" 
                type="text" 
                class="form-control" 
                id="floatingEmail" 
                placeholder="ایمیل"
                :class="{'is-invalid':emailE===true, 'is-valid':emailE===false}"
              >

              <label for="floatingEmail">Email</label>
              <div class="invalid-feedback">
                {{ emailEM }}
              </div>
            </div>

            <div class="form-floating position-relative mb-3" lang="en">
              <input 
                v-model="password" 
                type="password" 
                class="form-control" 
                id="floatingPassword1" 
                placeholder="رمز عبور"
                :class="{'is-invalid':passwordE===true, 'is-valid':passwordE===false}"
              >

              <button type="button" @click="showPassword('floatingPassword1')" class="btn position-absolute top-50 end-0 translate-middle-y"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16"><path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/><path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/></svg></button>

              <label for="floatingPassword1">Password</label>
              <div class="invalid-feedback">
                {{ passwordEM }}
              </div>
            </div>

						<div class="form-floating position-relative" lang="en">
              <input 
                v-model="passwordConfirm" 
                type="password" 
                class="form-control" 
                id="floatingPassword2" 
                placeholder="تکرار رمز عبور"
                :class="{'is-invalid':passwordConfirmE===true, 'is-valid':passwordConfirmE===false}"
              >

              <button type="button" @click="showPassword('floatingPassword2')" class="btn position-absolute top-50 end-0 translate-middle-y"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16"><path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/><path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/></svg></button>

              <label for="floatingPassword2">Confirm password</label>
              <div class="invalid-feedback">
                {{ passwordConfirmEM }}
              </div>
            </div>

            <button type="submit" class="btn btn-outline-dark mt-2 mb-4">ثبت نام</button>

          </form>
          <!-- end register form -->

          <div class="d-flex" dir="rtl">

            <router-link to="/" class="text-dark hover-underline">کاربر سایت هستم</router-link>

          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useStore } from 'vuex'
import { useRouter } from 'vue-router';
import axios from 'axios'
import Swal from 'sweetalert2'


export default {
  name: 'RegisterView',
  setup() {
    const store = useStore()
    const router = useRouter();

    let username = ref('')
    let password = ref('')
    let passwordConfirm = ref('')
    let email = ref('')

    let usernameE = ref()
    let usernameEM = ref('')
    let passwordE = ref()
    let passwordEM = ref('')
    let passwordConfirmE = ref()
    let passwordConfirmEM = ref('')
    let emailE = ref()
    let emailEM = ref('')

    let fullScreenLoading = ref(false)


    function doRegister() {
      let access = true

      if(username.value.length < 5){
        usernameE.value = true
        access = false
        if(username.value.length == 0){
            usernameEM.value = 'نام کاربری اجباری است'
        } else {
            usernameEM.value = 'نام کاربری باید بالای ۴ کاراکتر باشد'
        }
      } else {
        usernameE.value = false
        usernameEM.value = ''
      }

      
      if(email.value.indexOf('@') == -1 || email.value.indexOf('.') == -1){
        emailE.value = true
        access = false
        if(email.value.length == 0){
          emailEM.value = 'ایمیل اجباری است'
        } else{
          emailEM.value = 'لطفا ایمیل خود را به صورت صحیح وارد کنید'
        }
      } else if(email.value.length < 6){
          emailE.value = true
          access = false
          emailEM.value = 'لطفا ایمیل خود را به صورت صحیح وارد کنید'
      } else {
          emailE.value = false
          emailEM.value = ''
      }


      if(password.value.length < 8){
        passwordE.value = true
        access = false
        if(password.value.length == 0){
          passwordEM.value = 'رمزعبور اجباری است'
        } else {
          passwordEM.value = 'رمزعبور باید بیشتر از ۷ کاراکتر باشد'
        }
      } else {
        passwordE.value = false
        passwordEM.value = ''
      }


      if(passwordConfirm.value.length < 8){
        passwordConfirmE.value = true
        access = false
        if(passwordConfirm.value.length == 0){
          passwordConfirmEM.value = 'تکرار رمزعبور اجباری است'
        } else {
          passwordConfirmEM.value = 'تکراررمزعبور باید بیشتر از ۷ کاراکتر باشد'
        }
      } else {
          passwordConfirmE.value = false
          passwordConfirmEM.value = ''
      }


      if(password.value != passwordConfirm.value){
        access = false
        passwordE.value = true
        passwordConfirmE.value = true
        passwordEM.value = 'رمزعبور و تکرار آن با هم مطابقت ندارد'
      } else {
          if(!passwordE.value && passwordConfirmE.value) {
            access = true
          }
      }

      if(access){
        fullScreenLoading.value = true
        axios
        .post('account/signup/', {
          username: username.value,
          password: password.value,
          email: email.value,
        })
        .then(response => {
          fullScreenLoading.value = false
          // store.commit('login', response.data.access_token)
          Swal.fire({
            icon: 'success',
            title: 'ایمیل تایید برای شما فرستاده شد.',
            text: '',
            backdrop: false,
            timer: 2000,
            showConfirmButton: false,
          })
          router.push('/')
        })
        .catch(error => {
          fullScreenLoading.value = false
          Swal.fire({
            icon: 'error',
            title: error.response.data.message,
            text: '',
            backdrop: false,
            showConfirmButton: true,
          })
        })

      }
      
    }


    function showPassword(id) {
      let x = document.querySelector(`#${id}`);
      if (x.type === "password") {
          x.type = "text";
      } else {
          x.type = "password";
      }
    }

    return{
      username,
      password,
      passwordConfirm,
      email,
      usernameE,
      usernameEM,
      passwordE,
      passwordEM,
      passwordConfirmE,
      passwordConfirmEM,
      emailE,
      emailEM,
      fullScreenLoading,
      doRegister,
      showPassword,
    }
  }
}
</script>


<style scoped>
*{
  text-align: center;
}
</style>
