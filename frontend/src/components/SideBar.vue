<template>
	<!-- The sidebar -->
	<div class="sidebar">
		<router-link class="hover-underline" to="/dashboard/username">داشبورد</router-link>
		<router-link class="hover-underline" to="/dashboard/overview">نمای کلی</router-link>
		<router-link class="hover-underline" to="/">مالی</router-link>
		<router-link class="hover-underline" to="/">جانی</router-link>
		<div class="dropdown hover-underline" id="username-dropdown">
			<a class="dropdown-toggle" href="#" data-bs-toggle="dropdown" aria-expanded="false">
				{{username}}
			</a>
			<ul class="dropdown-menu bg-dark">
				<li><router-link to="/profile" class="dropdown-item" href="#">پروفایل</router-link></li>
				<li><a class="dropdown-item" hreaf="#">Another action</a></li>
				<li><a @click="doLogout()" href="#" class="dropdown-item">خروج</a></li>
			</ul>
		</div>
	</div>
</template>

<script>
import axios from 'axios'
import { ref } from "vue";
import Swal from 'sweetalert2'
import { useStore } from 'vuex'
import { useRoute, useRouter } from 'vue-router'

export default {
	setup() {
		let username = ref('')

		axios
		.get('account/')
		.then(response => {
			username.value = response.data.data.username
		})
		.catch(error => {
			console.log(error.data);
		})
		const store = useStore()
    const router = useRouter()

		function doLogout(){
      store.commit('logout')
      router.push('/')
    }

		return{
			username,
			doLogout,
		}

	}
}
</script>

<style>
 .sidebar {
  margin: 0;
  padding: 0;
  width: 200px;
  background-color: #00095c;
  position: fixed;
  height: 100%;
  overflow: auprofileto;
}

.sidebar a {
  display: block;
  color: rgb(255, 255, 255);
  padding: 8px 16px;
}
#username-dropdown{
	display: block;
}
.sidebar a.router-link-exact-active {
  color: cyan;
}

.content {
  margin-right: 200px;
  padding: 1px 16px;
  height: 1000px;
}

@media screen and (max-width: 700px) {
  .sidebar {
    width: 100%;
    height: auto;
    /* position: relative; */
		z-index: 5;
  }
  .sidebar a {float: right;}
  .content {margin-right: 0;}
	.top-container{margin-top: 4rem;}
}

@media screen and (max-width: 400px) {
  .sidebar a {
    text-align: center;
    float: none;
  }
	.top-container{margin-top: 11rem;}
} 

</style>