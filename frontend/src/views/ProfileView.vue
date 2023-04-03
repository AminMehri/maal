<template>
	<div class="Profile" dir="rtl">
		<SideBar />
		<div class="content">
			<h1>PROFILE</h1>
			<p>ایمیل:‌ {{ email }}</p>
			<p>نام کاربری: {{ username }}</p>
			<p v-if="emailVerified" class="text-danger">ایمیل شما تایید شده است.</p>
			<button v-if="!emailVerified" @click="sendVerifyEmail()" class="btn btn-outline-danger">برای تایید ایمیل خود کلیک کنید.</button>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
import { ref } from "vue";
import Swal from 'sweetalert2'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'
import SideBar from '@/components/SideBar.vue'
export default{
	components: {
		SideBar,
	},
	setup() {
		let username = ref('')
		let email = ref('')
		let emailVerified = ref()

		axios
		.get('account/')
		.then(response => {
			username.value = response.data.data.username
			email.value = response.data.data.email
			emailVerified.value = response.data.data.email_verified
		})
		.catch(error => {
			console.log(error.data);
		})

		function sendVerifyEmail(){
      axios
      .post('account/sendVerifyEmail/')
      .then(response => {
        Swal.fire({
          icon: 'success',
          title: 'ایمیل تایید برای شما فرستاده شد.',
          text: '',
          backdrop: false,
          timer: 2000,
          showConfirmButton: false,
        })
      })
      .catch(error => {
        Swal.fire({
          icon: 'error',
          title: error.response.data.message,
          text: '',
          backdrop: false,
          showConfirmButton: true,
        })
      })
    }

		return{
		username,
		email,
		emailVerified,
		sendVerifyEmail,
		}
	}
}
</script>