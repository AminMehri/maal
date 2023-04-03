import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'
import Swal from 'sweetalert2'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'jquery/src/jquery.js'
import 'popper.js/dist/popper.min.js'
import 'bootstrap/dist/js/bootstrap.bundle'

createApp(App).use(store).use(router).mount('#app')


axios.defaults.baseURL = 'http://127.0.0.1:8000';
// let base_url = "https://api.getarz.com"



setTimeout(() => {
    Swal.fire("تست هدر سوییت الرت", "تست برای دیتیل سوییت الرت", "success")
}, 1000);


axios.interceptors.response.use(
    (success) =>{
        if(success.data.detail){
            Swal.fire(success.data.message, success.data.detail, 'success')
        }else if(success.data.message){
            Swal.fire(success.data.message, '', 'success')
        }
    return success
}, (error) => {
    try{
        if(error.response.status == 500){
            Swal.fire("خطا داخلی سرور", "این مورد جهت بررسی به پشتیبانی ارسال شد.", 'error')
            return Promise.reject(error);
        }
        if(error.response.data.detail){
            Swal.fire(error.response.data.message, error.response.data.detail, 'error')
        }
        else{
            Swal.fire(error.response.data.message, "", 'error')
        }

        return Promise.reject(error);
    }catch (error) {
        Swal.fire("خطا در ارتباط با سرور", "لطفا از اتصال اینترنت خود اطمینان حاصل کرده و صفحه را رفرش کنید.", 'error')
      }
})

