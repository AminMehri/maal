<template>
  <div class="home">

    <div v-if="fullScreenLoading" class="fullscreen-loading">Loading&#8230;</div>

    <div class="container">
      <p class="text-danger">Welcome to the city of lie!</p>
      <div class="card mx-auto" style="width: 25rem;">
        <img src="@/assets/groot.jpg" class="card-img-top" alt="...">
        <div class="card-body">
          <!-- login form -->
          <form @submit.prevent="doLogin()">
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

            <div class="form-floating position-relative" lang="en">
              <input 
                v-model="password" 
                type="password" 
                class="form-control" 
                id="floatingPassword" 
                placeholder="رمز عبور"
                :class="{'is-invalid':passwordE===true, 'is-valid':passwordE===false}"
              >

              <button type="button" @click="showPassword()" class="btn position-absolute top-50 end-0 translate-middle-y"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-eye-fill" viewBox="0 0 16 16"><path d="M10.5 8a2.5 2.5 0 1 1-5 0 2.5 2.5 0 0 1 5 0z"/><path d="M0 8s3-5.5 8-5.5S16 8 16 8s-3 5.5-8 5.5S0 8 0 8zm8 3.5a3.5 3.5 0 1 0 0-7 3.5 3.5 0 0 0 0 7z"/></svg></button>

              <label for="floatingPassword">Password</label>
              <div class="invalid-feedback">
                {{ passwordEM }}
              </div>
            </div>

            <button type="submit" class="btn btn-outline-dark mt-2 mb-4">ورود به حساب کاربری</button>

          </form>
          <!-- end login form -->

          <!-- Modal -->
          <div class="modal fade" id="exampleModal" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true">
            <div class="modal-dialog">
              <div class="modal-content">
                <div class="modal-header">
                  <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" id="close-modal"></button>
                </div>
                <div class="modal-body">
                  <input v-model="email" class="w-100 form-control" type="text" placeholder="لطفا ایمیل خود را وارد کنید">
                </div>
                <div class="modal-footer">
                  <button @click="doForgetPassword()" type="button" class="btn btn-outline-primary">تایید ایمیل</button>
                </div>
              </div>
            </div>
          </div>

          <div class="d-flex justify-content-between">

            <!-- Button trigger modal -->
            <a href="#" class="text-dark hover-underline" data-bs-toggle="modal" data-bs-target="#exampleModal">
                رمزعبورمو فراموش کردم
            </a>
            <router-link to="/register" class="text-dark hover-underline">!عضو سایت نیستم</router-link>

          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref } from "vue";
import { useStore } from 'vuex'
import { useRouter } from 'vue-router'
import Swal from 'sweetalert2'
import axios from 'axios'

export default {
  name: 'HomeView',
  setup() {
    const store = useStore()
    const router = useRouter()

    let username = ref('')
    let password = ref('')
    let usernameE = ref()
    let passwordE = ref()
    let usernameEM = ref('')
    let passwordEM = ref('')

    let email = ref('')
    let resetPasswordEM = ref('')

    let fullScreenLoading = ref(false)

    // function isAuthenticated(){
    //   if(store.state.isAuthenticated){
    //     router.push('/about')
    //   }
    // }
    // isAuthenticated()

    function doLogin() {
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

      if(password.value.length < 8){
          passwordE.value = true
          access = false
          if(password.value.length == 0){
              passwordEM.value = 'رمز اجباری است'
          } else {
              passwordEM.value = 'رمز باید بالای ۷ کاراکتر باشد'
          }
      } else {
          passwordE.value = false
          passwordEM.value = ''
      }

      if(access){
        fullScreenLoading.value = true
        axios
        .post('account/login/', {
            username: username.value,
            password: password.value
        })
        .then(response => {
          fullScreenLoading.value = false
          store.commit('login', response.data.access)
          router.push('/profile')
        })
        .catch(error => {
          fullScreenLoading.value = false
          if (error.response.data.detail == "No active account found with the given credentials"){
              usernameEM.value = "نام کاربری یا رمزعبورتو اشتباه زدی. دقت کن!"
          }
          usernameE.value = true
          passwordE.value = true
        })

      }
    }   

    function doForgetPassword(){
      fullScreenLoading.value = true
      document.getElementById('close-modal').click()
      axios
      .post('account/forgetPassword/', {
        email: email.value,
      })
      .then(response => {
        Swal.fire({
            icon: 'success',
            title: 'هورا!!!',
            text: 'ایمیل برای شما ارسال شد.',
        })
        fullScreenLoading.value = false
      })
      .catch(error => {
        resetPasswordEM.value = error.response.data.message
        // if(error.response.statusText == 'Bad Request'){
        //     resetPasswordEM.value = 'ایمیلی که وارد کردی اشتباهه. تصحیحش کن.'
        // } else{
        //     resetPasswordEM.value = 'یه جای کار میلنگه'
        // }
        Swal.fire({
            icon: 'error',
            title: 'وای!!!',
            text: resetPasswordEM.value,
        })
        fullScreenLoading.value = false
      })
      email.value = ''
    }
    
    function showPassword() {
      let x = document.querySelector("#floatingPassword");
      if (x.type === "password") {
          x.type = "text";
      } else {
          x.type = "password";
      }
    }

    return{
      username,
      password,
      usernameE,
      passwordE,
      usernameEM,
      passwordEM,
      fullScreenLoading,
      email,
      doLogin,
      showPassword,
      doForgetPassword,
    }
  }
}
</script>


<style scoped>
*{
  text-align: center;
}
</style>
