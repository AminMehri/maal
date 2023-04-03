<template>
	<div class="user-dashboard" dir="rtl">
		<SideBar />
		<div class="content">
			<h1>USER DASHBOARD</h1>
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

export default {
  components:{
    SideBar,
  },
	setup() {
    const store = useStore()
    const router = useRouter()



    return{

    }
    
  }
}
</script>