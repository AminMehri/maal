<template>
	<div v-if="fullScreenLoading" class="fullscreen-loading">Loading&#8230;</div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'
import { useStore } from 'vuex'
import { ref } from "vue";
import axios from 'axios'
import Swal from 'sweetalert2'

export default {
	setup() {   
		const store = useStore()
		const route = useRoute()
		const router = useRouter()

		let id = ref(route.params.id)
		let token = ref(route.params.token)

		let fullScreenLoading = ref(true)

		function confirmEmail(){
			axios
			.post(`account/submitVerifyEmail/`, {
				id: id.value,
				token: token.value
			})
			.then(response => {
				fullScreenLoading.value = false
				Swal.fire({
						title: 'YEEY',
						text:   "ایمیل شما تایید شد",
						icon: 'success',
				});
				if(store.state.isAuthenticated){
					router.push('/profile')
				} else{
					router.push('/')
				}
			})
			.catch(error => {
				fullScreenLoading.value = false
				Swal.fire({
						title: 'OPPS',
						text:   error.response.data.message,
						icon: 'warning',
				});

				if(store.state.isAuthenticated){
					router.push('/profile')
				} else{
					router.push('/')
				}
			})
		}
		confirmEmail()


		return {
			fullScreenLoading
		}
	},
}

</script>

<style scoped>
</style>