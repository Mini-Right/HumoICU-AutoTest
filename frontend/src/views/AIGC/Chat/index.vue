<script setup lang="ts">
import { onMounted } from 'vue';
import { foldMeun } from '/@/utils/other';
import { Splitpanes, Pane } from 'splitpanes';
import 'splitpanes/dist/splitpanes.css';
onMounted(() => {
	// 折叠菜单
	foldMeun();
});
</script>
<template>
	<div class="template-container layout-pd">
		<el-card>
			<splitpanes class="panes">
				<pane :size="15"> 1</pane>
				<!-- <el-divider direction="vertical" style="height: 100%" /> -->
				<pane :size="70">2 </pane>
				<pane :size="15">3 </pane>
			</splitpanes>
		</el-card>
	</div>
</template>
<style lang="scss" scoped>
:deep(.splitpanes--vertical) {
	.splitpanes__splitter {
		background-color: rgb(204, 204, 204, 0.5);
		width: 1px;
	}
}
</style>
