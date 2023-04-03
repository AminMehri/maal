<template>
  <router-view/>
</template>


<script>
import { useStore } from 'vuex'
import { onMounted } from "vue";

export default {
	setup() {
		const store = useStore()

		onMounted(() => {
			store.dispatch('onStart')
    })

    
		return {
			
		}

    },
	watch: {
		$route() {
			this.$store.dispatch('onStart')
		},

	},

}

</script>

<style>
@font-face {
  font-family: 'Vazir';
  src: url('@/assets/fonts/Vazir.woff2') format('woff2'),
         url('@/assets/fonts/Vazir.woff') format('woff'),
         url('@/assets/fonts/Vazir.ttf') format('truetype');
}

#app {
  font-family: Vazir;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

a{
  text-decoration: none !important;
}

.hover-underline {
  display: inline-block;
  position: relative;
  color: #0087ca;
}

.hover-underline:after {
  content: '';
  position: absolute;
  width: 100%;
  transform: scaleX(0);
  height: 2px;
  bottom: 0;
  left: 0;
  background-color: black;
  transform-origin: bottom right;
  transition: transform 0.25s ease-out;
}

.hover-underline:hover:after {
  transform: scaleX(1);
  transform-origin: bottom left;
}
</style>
