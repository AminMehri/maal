<template>

	<div class="Password-reset-confirm">
		<div class="container">
			<div class="row">
				<div class="col-md-8 mx-auto border-start border-end p-5 my-4 shadow-lg" style="text-align: justify;">

					<div class="row border p-2">

						<div class="col-md-12">
							<label for="inputResetPassword1" class="form-label">رمزعبور جدید</label>
							<input v-model="resetPassword1" type="password" class="form-control" id="inputResetPassword1" >
						</div>

						<div class="col-md-12">
							<label for="inputResetPassword2" class="form-label my-2">تایید رمزعبور</label>
							<input v-model="resetPassword2" type="password" class="form-control" id="inputResetPassword2" >
						</div>
							
					</div>
					<button @click="resetPasswordConfirm()" class="btn btn-outline-success fw-bold mt-3 w-25">Submit</button>

				</div>
			</div>
		</div>
	</div>
</template>

<script>
import { useRoute, useRouter } from 'vue-router'
import { ref } from "vue";
import axios from 'axios'
import Swal from 'sweetalert2'



export default {
	setup() {
		const route = useRoute()
		const router = useRouter()

		let resetPassword1 = ref()
		let resetPassword2 = ref()

		let id = ref(route.params.id)
		let token = ref(route.params.token)

		let access = ref(true)


		function resetPasswordConfirm(){
			access.value = true
			if(resetPassword1.value != resetPassword2.value){
				access.value = false
				Swal.fire({
					text: "رمز عبور و تکرار آن با هم مطابقت ندارد.",
					icon: 'error',
				});
			}
			if(access.value){
				console.log(id.value);
				console.log(token.value);
				axios
				.post(`account/setPassword/`, {
					password: resetPassword1.value,
					id: id.value,
					token: token.value
				})
				.then(response => {
					Swal.fire({
							title: 'YEEY',
							text:   "رمزعبور شما با موفقیت تغییر یافت.",
							icon: 'success',
					});
					router.push('/')
				})
				.catch(error => {
					Swal.fire({
							title: 'OPPS',
							text:   "لطفا اطلاعات خود را به درستی وارد کنید. همچنین ممکن است توکن شما منقضی شده باشد.",
							icon: 'warning',
					});
				})
			}
		}


		return {
				resetPasswordConfirm,
				resetPassword1,
				resetPassword2,
		}
	},
}

</script>

<style scoped>

</style>