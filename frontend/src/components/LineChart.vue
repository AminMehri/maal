<template>
	<Line :data="data" :options="options"/>
</template>

<script>
import {
	Chart as ChartJS,
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend
} from 'chart.js'
import { Line } from 'vue-chartjs'

ChartJS.register(
	CategoryScale,
	LinearScale,
	PointElement,
	LineElement,
	Title,
	Tooltip,
	Legend
)

export default {
	components: {
		Line
	},
	data() {
		return{
			data: {
				labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
				datasets: [
						{
						label: 'Women',
						backgroundColor: 'red',
						data: [50, 48, 15, 46, 52, 73, 32]
						},
						{
						label: 'Man',
						backgroundColor: 'blue',
						data: [40, 39, 10, 40, 39, 80, 40]
						}
				]
			},
			options: {
				responsive: true,
 			 	maintainAspectRatio: false
			}
		}
	}
}
</script>
